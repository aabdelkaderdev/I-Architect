"""Unit tests for RAA parallel subgraphs — Send routing, LLM injection,
strategy reference manifests, parent-link validation, relationship scope
validation, typed ArchFragment output, and merge_batch_outputs reducer."""

from __future__ import annotations

from dataclasses import asdict
from unittest.mock import MagicMock

import pytest

from raa.state.channels import merge_batch_outputs
from raa.state.types import (
    ArchComponent,
    ArchContainer,
    ArchExternalSystem,
    ArchFragment,
    ArchPattern,
    ArchPerson,
    ArchRelationship,
    ArchSystem,
)


# ============================================================================
# Shared fixtures (T015)
# ============================================================================


@pytest.fixture
def fake_batch() -> dict:
    """A normal (non-reduced-confidence) batch dict."""
    return {
        "batch_id": 0,
        "group_id": 1,
        "requirement_ids": ["R1", "R2"],
        "requirements": [
            {"id": "R1", "text": "The system shall authenticate users."},
            {"id": "R2", "text": "The system shall log all access."},
        ],
        "reduced_confidence": False,
    }


@pytest.fixture
def fake_reduced_batch() -> dict:
    """A reduced-confidence batch dict."""
    return {
        "batch_id": 1,
        "group_id": 2,
        "requirement_ids": ["R3"],
        "requirements": [{"id": "R3", "text": "Unclear requirement."}],
        "reduced_confidence": True,
    }


@pytest.fixture
def fake_quality_weights() -> dict[str, int]:
    return {"security": 5, "performance": 3, "maintainability": 2}


@pytest.fixture
def fake_running_arch_model() -> dict:
    """Existing running architecture model for parent-link resolution."""
    return {
        "systems": [
            {"id": "SYS_EXISTING", "label": "Existing System", "description": "Already in model"}
        ],
        "containers": [
            {"id": "CONT_EXISTING", "label": "Existing Container", "description": "Already in model",
             "parent_system_id": "SYS_EXISTING"}
        ],
    }


@pytest.fixture
def fake_bridge_requirements() -> dict:
    return {("R1", "R2"): ["shared_auth"]}


@pytest.fixture
def fake_llm() -> MagicMock:
    """Fake LLM whose .invoke(prompt) returns a dict response."""
    llm = MagicMock()
    llm.invoke.return_value = {
        "systems": [
            {"id": "SYS_A", "label": "System A", "description": "Primary system"}
        ],
        "containers": [],
        "components": [],
        "persons": [],
        "external_systems": [],
        "relationships": [],
        "patterns": [{"name": "Layered", "rationale": "Separation of concerns"}],
        "rationale": {"summary": "test"},
    }
    return llm


@pytest.fixture
def fake_config(fake_llm: MagicMock) -> dict:
    """Runtime config with LLM context."""
    return {
        "context": {
            "llm_raa_a": fake_llm,
            "llm_raa_b": MagicMock(invoke=MagicMock(return_value={
                "systems": [],
                "containers": [],
                "components": [],
                "persons": [],
                "external_systems": [],
                "relationships": [],
                "patterns": [],
                "rationale": {"summary": "b"},
            })),
            "llm_raa_c": MagicMock(invoke=MagicMock(return_value={
                "systems": [],
                "containers": [],
                "components": [],
                "persons": [],
                "external_systems": [],
                "relationships": [],
                "patterns": [],
                "rationale": {"summary": "c"},
            })),
        }
    }


@pytest.fixture
def fake_state(fake_batch, fake_quality_weights, fake_running_arch_model, fake_bridge_requirements) -> dict:
    """Minimal RAAState-like dict for routing tests."""
    return {
        "batch_queue": [fake_batch],
        "batch_cursor": 0,
        "quality_weights": fake_quality_weights,
        "running_arch_model": fake_running_arch_model,
        "bridge_requirements": fake_bridge_requirements,
        "embeddings_ready": True,
    }


@pytest.fixture
def arch_fragment_dict() -> dict:
    """Dict fixture parseable into an ArchFragment."""
    return {
        "systems": [
            {"id": "S1", "label": "Sys One", "description": "First system"}
        ],
        "containers": [
            {"id": "C1", "label": "Cont One", "description": "First container", "parent_system_id": "S1"}
        ],
        "components": [
            {"id": "COMP1", "label": "Comp One", "description": "First component", "parent_container_id": "C1"}
        ],
        "persons": [
            {"id": "P1", "label": "User", "description": "End user"}
        ],
        "external_systems": [
            {"id": "EXT1", "label": "Payment Gateway", "description": "External payment provider"}
        ],
        "relationships": [
            {
                "source_id": "P1", "target_id": "S1",
                "interaction_type": "uses",
                "technology": "HTTPS",
                "diagram_scope": "context",
            }
        ],
        "patterns": [
            {"name": "Layered", "rationale": "Separation of concerns", "quality_attributes": ["maintainability"]}
        ],
        "rationale": {"summary": "Standard layered architecture"},
    }


# ============================================================================
# T016 — fan_out_subgraphs returns 3 Send objects for normal batch
# ============================================================================


def test_fan_out_three_sends_for_normal_batch(fake_state: dict, fake_config: dict):
    """Normal batch emits 3 Send objects targeting raa_a, raa_b, raa_c."""
    from langgraph.types import Send

    from raa.graphs.subgraphs.routing import fan_out_subgraphs

    sends = fan_out_subgraphs(fake_state, fake_config)
    assert len(sends) == 3
    assert all(isinstance(s, Send) for s in sends)
    targets = [s.node for s in sends]
    assert "raa_a" in targets
    assert "raa_b" in targets
    assert "raa_c" in targets


# ============================================================================
# T017 — fan_out_subgraphs returns 1 Send for reduced_confidence batches
# ============================================================================


def test_fan_out_single_send_for_reduced_confidence(fake_quality_weights, fake_running_arch_model,
                                                     fake_bridge_requirements, fake_config, fake_reduced_batch):
    """Reduced-confidence batch emits 1 Send targeting raa_a."""
    from langgraph.types import Send

    from raa.graphs.subgraphs.routing import fan_out_subgraphs

    state = {
        "batch_queue": [fake_reduced_batch],
        "batch_cursor": 0,
        "quality_weights": fake_quality_weights,
        "running_arch_model": fake_running_arch_model,
        "bridge_requirements": fake_bridge_requirements,
        "embeddings_ready": True,
    }
    sends = fan_out_subgraphs(state, fake_config)
    assert len(sends) == 1
    assert sends[0].node == "raa_a"


# ============================================================================
# T018 — Send payload contains all required keys
# ============================================================================


def test_send_payload_contains_required_keys(fake_state: dict, fake_config: dict):
    """Each Send arg must include batch, batch_index, quality_weights,
    running_arch_model, bridge_requirements, strategy, and llm."""
    from raa.graphs.subgraphs.routing import fan_out_subgraphs

    sends = fan_out_subgraphs(fake_state, fake_config)
    required = {"batch", "batch_index", "quality_weights", "running_arch_model",
                "bridge_requirements", "strategy", "llm"}

    for i, s in enumerate(sends):
        missing = required - set(s.arg.keys())
        assert not missing, f"Send[{i}] missing keys: {missing}"
        assert s.arg["batch_index"] == 0
        assert s.arg["strategy"] in ("saam_first", "pattern_driven", "entity_driven")
        assert s.arg["llm"] is not None


# ============================================================================
# T019 — Missing LLM context keys raise configuration error
# ============================================================================


def test_fan_out_raises_on_missing_llm_key(fake_state: dict):
    """fan_out_subgraphs raises when a required llm_raa_* key is missing."""
    from raa.graphs.subgraphs.routing import fan_out_subgraphs

    config_empty = {"context": {}}  # no LLM keys
    with pytest.raises((KeyError, ValueError, RuntimeError)):
        fan_out_subgraphs(fake_state, config_empty)


def test_fan_out_raises_on_missing_llm_raa_b(fake_state: dict, fake_llm: MagicMock):
    """Raises when llm_raa_b is missing (needed for 3-target fan-out)."""
    from raa.graphs.subgraphs.routing import fan_out_subgraphs

    config = {"context": {"llm_raa_a": fake_llm, "llm_raa_c": fake_llm}}
    with pytest.raises((KeyError, ValueError, RuntimeError)):
        fan_out_subgraphs(fake_state, config)


# ============================================================================
# T020 — run_raa_a consumes payload["llm"], returns batch_outputs
# ============================================================================


def test_run_raa_a_consumes_payload_llm(fake_llm: MagicMock):
    """RAA-A subgraph reads llm from payload, not state/globals."""
    from raa.graphs.subgraphs.raa_a import run_raa_a

    payload = {
        "batch": {"batch_id": 0},
        "batch_index": 5,
        "quality_weights": {},
        "running_arch_model": None,
        "bridge_requirements": {},
        "strategy": "saam_first",
        "llm": fake_llm,
    }
    result = run_raa_a(payload)
    assert "batch_outputs" in result
    batch_outputs = result["batch_outputs"]
    assert 5 in batch_outputs
    assert isinstance(batch_outputs[5], list)
    assert all(isinstance(f, ArchFragment) for f in batch_outputs[5])
    fake_llm.invoke.assert_called_once()


# ============================================================================
# T021 — run_raa_b consumes payload["llm"], includes patterns
# ============================================================================


def test_run_raa_b_consumes_payload_llm(fake_config: dict):
    """RAA-B subgraph reads llm from payload and returns batch_outputs."""
    from raa.graphs.subgraphs.raa_b import run_raa_b

    llm_b = fake_config["context"]["llm_raa_b"]
    payload = {
        "batch": {"batch_id": 0},
        "batch_index": 1,
        "quality_weights": {},
        "running_arch_model": None,
        "bridge_requirements": {},
        "strategy": "pattern_driven",
        "llm": llm_b,
    }
    result = run_raa_b(payload)
    assert "batch_outputs" in result
    assert 1 in result["batch_outputs"]
    assert len(result["batch_outputs"][1]) == 1
    llm_b.invoke.assert_called_once()


# ============================================================================
# T022 — run_raa_c consumes payload["llm"], entity/relationship-driven
# ============================================================================


def test_run_raa_c_consumes_payload_llm(fake_config: dict):
    """RAA-C subgraph reads llm from payload and returns batch_outputs."""
    from raa.graphs.subgraphs.raa_c import run_raa_c

    llm_c = fake_config["context"]["llm_raa_c"]
    payload = {
        "batch": {"batch_id": 0},
        "batch_index": 2,
        "quality_weights": {},
        "running_arch_model": None,
        "bridge_requirements": {},
        "strategy": "entity_driven",
        "llm": llm_c,
    }
    result = run_raa_c(payload)
    assert "batch_outputs" in result
    assert 2 in result["batch_outputs"]
    llm_c.invoke.assert_called_once()


# ============================================================================
# T023 — RAA-A reference manifest verification
# ============================================================================


def test_raa_a_references_include_saam():
    """RAA-A references include SAAM.md, Quality_Attributes.md, and others."""
    from raa.graphs.subgraphs.common import RAA_A_REFERENCES

    assert "SAAM.md" in RAA_A_REFERENCES
    assert "Quality_Attributes.md" in RAA_A_REFERENCES
    assert "Entity_Extraction.md" in RAA_A_REFERENCES
    assert "Relationship_Extraction.md" in RAA_A_REFERENCES
    assert "Technology_Inference.md" in RAA_A_REFERENCES
    assert "C4.md" in RAA_A_REFERENCES
    assert "C4_Level_Mapping.md" in RAA_A_REFERENCES
    assert "Pattern_Selection.md" not in RAA_A_REFERENCES


# ============================================================================
# T024 — RAA-B reference manifest verification
# ============================================================================


def test_raa_b_references_include_pattern_selection():
    """RAA-B references include Pattern_Selection.md."""
    from raa.graphs.subgraphs.common import RAA_B_REFERENCES

    assert "Pattern_Selection.md" in RAA_B_REFERENCES
    assert "Quality_Attributes.md" in RAA_B_REFERENCES
    assert "Entity_Extraction.md" in RAA_B_REFERENCES
    assert "Relationship_Extraction.md" in RAA_B_REFERENCES
    assert "Technology_Inference.md" in RAA_B_REFERENCES
    assert "C4.md" in RAA_B_REFERENCES
    assert "C4_Level_Mapping.md" in RAA_B_REFERENCES
    assert "SAAM.md" not in RAA_B_REFERENCES


# ============================================================================
# T025 — RAA-C reference manifest verification (excludes SAAM, Pattern_Selection)
# ============================================================================


def test_raa_c_references_exclude_saam_and_patterns():
    """RAA-C references exclude SAAM.md and Pattern_Selection.md."""
    from raa.graphs.subgraphs.common import RAA_C_REFERENCES

    assert "SAAM.md" not in RAA_C_REFERENCES
    assert "Pattern_Selection.md" not in RAA_C_REFERENCES
    assert "Entity_Extraction.md" in RAA_C_REFERENCES
    assert "Relationship_Extraction.md" in RAA_C_REFERENCES
    assert "Technology_Inference.md" in RAA_C_REFERENCES
    assert "C4.md" in RAA_C_REFERENCES
    assert "C4_Level_Mapping.md" in RAA_C_REFERENCES


# ============================================================================
# T026 — validate_parent_links accepts valid container parents
# ============================================================================


def test_validate_parent_links_accepts_valid_container():
    """Container with parent_system_id in same fragment passes."""
    from raa.graphs.subgraphs.common import validate_parent_links

    container = ArchContainer(
        id="C1", label="Web App", description="Web application", parent_system_id="S1"
    )
    fragment = ArchFragment(systems=[ArchSystem(id="S1", label="Sys", description="A system")],
                            containers=[container])
    validate_parent_links(fragment, None)  # should not raise


# ============================================================================
# T027 — validate_parent_links rejects unresolved parent_system_id
# ============================================================================


def test_validate_parent_links_rejects_orphan_container():
    """Container with unresolved parent_system_id raises ValueError."""
    from raa.graphs.subgraphs.common import validate_parent_links

    container = ArchContainer(
        id="C1", label="Web App", description="Web app", parent_system_id="MISSING_SYS"
    )
    fragment = ArchFragment(containers=[container])
    with pytest.raises(ValueError, match="parent_system_id"):
        validate_parent_links(fragment, None)


# ============================================================================
# T028 — validate_parent_links accepts valid component parents
# ============================================================================


def test_validate_parent_links_accepts_valid_component():
    """Component with parent_container_id in same fragment passes."""
    from raa.graphs.subgraphs.common import validate_parent_links

    component = ArchComponent(
        id="COMP1", label="Service", description="A service", parent_container_id="C1"
    )
    fragment = ArchFragment(containers=[ArchContainer(id="C1", label="Web App", description="Web",
                                                       parent_system_id="S1")],
                            systems=[ArchSystem(id="S1", label="Sys", description="System")],
                            components=[component])
    validate_parent_links(fragment, None)


# ============================================================================
# T029 — validate_parent_links rejects unresolved parent_container_id
# ============================================================================


def test_validate_parent_links_rejects_orphan_component():
    """Component with unresolved parent_container_id raises ValueError."""
    from raa.graphs.subgraphs.common import validate_parent_links

    component = ArchComponent(
        id="COMP1", label="Service", description="A service", parent_container_id="MISSING_CONT"
    )
    fragment = ArchFragment(components=[component])
    with pytest.raises(ValueError, match="parent_container_id"):
        validate_parent_links(fragment, None)


# ============================================================================
# T026+ — validate_parent_links resolves parents from running_arch_model
# ============================================================================


def test_validate_parent_links_resolves_from_running_model():
    """Parent may also resolve from running_arch_model."""
    from raa.graphs.subgraphs.common import validate_parent_links

    container = ArchContainer(
        id="C_NEW", label="New Container", description="desc", parent_system_id="SYS_EXISTING"
    )
    fragment = ArchFragment(containers=[container])
    running = {"systems": [{"id": "SYS_EXISTING", "label": "Existing", "description": "Already there"}]}
    validate_parent_links(fragment, running)  # should not raise


# ============================================================================
# T030 — validate_relationship_scopes accepts valid diagram_scope
# ============================================================================


def test_validate_relationship_scopes_accepts_valid_scopes():
    """Relationships with valid diagram_scope matching endpoint types pass."""
    from raa.graphs.subgraphs.common import validate_relationship_scopes

    rel = ArchRelationship(
        source_id="P1", target_id="S1",
        interaction_type="uses", technology="HTTPS",
        diagram_scope="context",
    )
    fragment = ArchFragment(
        persons=[ArchPerson(id="P1", label="User", description="End user")],
        systems=[ArchSystem(id="S1", label="System", description="A system")],
        relationships=[rel],
    )
    # Person → System should have context scope
    validate_relationship_scopes(fragment, None)  # should not raise


# ============================================================================
# T031 — validate_relationship_scopes rejects mismatched scope
# ============================================================================


def test_validate_relationship_scopes_rejects_mismatched_scope():
    """Relationship with wrong diagram_scope for endpoint types raises ValueError."""
    from raa.graphs.subgraphs.common import validate_relationship_scopes

    # System → System should be context, not component
    rel = ArchRelationship(
        source_id="S1", target_id="S2",
        interaction_type="uses",
        technology=None,
        diagram_scope="component",  # wrong: system→system should be context
    )
    fragment = ArchFragment(
        systems=[
            ArchSystem(id="S1", label="Sys One", description="First"),
            ArchSystem(id="S2", label="Sys Two", description="Second"),
        ],
        relationships=[rel],
    )
    with pytest.raises(ValueError, match="diagram_scope"):
        validate_relationship_scopes(fragment, None)


def test_validate_relationship_scopes_rejects_missing_scope():
    """Relationship with empty diagram_scope raises ValueError."""
    from raa.graphs.subgraphs.common import validate_relationship_scopes

    rel = ArchRelationship(
        source_id="S1", target_id="S2",
        interaction_type="uses",
        technology=None,
        diagram_scope="",  # invalid
    )
    fragment = ArchFragment(
        systems=[
            ArchSystem(id="S1", label="Sys One", description="First"),
            ArchSystem(id="S2", label="Sys Two", description="Second"),
        ],
        relationships=[rel],
    )
    with pytest.raises(ValueError, match="diagram_scope"):
        validate_relationship_scopes(fragment, None)


# ============================================================================
# T032 — arch_fragment_from_dict creates typed dataclass instances
# ============================================================================


def test_arch_fragment_from_dict_creates_dataclass_instances(arch_fragment_dict: dict):
    """Output parser creates typed ArchFragment with real dataclass instances."""
    from raa.graphs.subgraphs.common import arch_fragment_from_dict

    fragment = arch_fragment_from_dict(arch_fragment_dict, source_fragment="test")

    assert isinstance(fragment, ArchFragment)
    assert isinstance(fragment.systems[0], ArchSystem)
    assert isinstance(fragment.containers[0], ArchContainer)
    assert isinstance(fragment.components[0], ArchComponent)
    assert isinstance(fragment.persons[0], ArchPerson)
    assert isinstance(fragment.external_systems[0], ArchExternalSystem)
    assert isinstance(fragment.relationships[0], ArchRelationship)
    assert isinstance(fragment.patterns[0], ArchPattern)

    assert fragment.systems[0].id == "S1"
    assert fragment.containers[0].parent_system_id == "S1"
    assert fragment.components[0].parent_container_id == "C1"
    assert fragment.relationships[0].diagram_scope == "context"


# ============================================================================
# T033 — merge_batch_outputs appends fragments under same index
# ============================================================================


def test_merge_batch_outputs_appends_fragments():
    """merge_batch_outputs concatenates fragment lists per batch index."""
    frag_a = ArchFragment(systems=[ArchSystem(id="A", label="A", description="From A")])
    frag_b = ArchFragment(systems=[ArchSystem(id="B", label="B", description="From B")])
    frag_c = ArchFragment(containers=[ArchContainer(id="C1", label="C", description="From C",
                                                     parent_system_id="A")])

    left = {0: [frag_a]}
    right = {0: [frag_b, frag_c]}

    merged = merge_batch_outputs(left, right)
    assert 0 in merged
    assert len(merged[0]) == 3
    assert merged[0][0] is frag_a
    assert merged[0][1] is frag_b
    assert merged[0][2] is frag_c


def test_merge_batch_outputs_handles_disjoint_keys():
    """Keys in only one dict are preserved."""
    left = {0: [ArchFragment()]}
    right = {1: [ArchFragment()]}
    merged = merge_batch_outputs(left, right)
    assert len(merged) == 2
    assert 0 in merged
    assert 1 in merged


# ============================================================================
# T034 — No LLM objects in returned state updates
# ============================================================================


def test_subgraph_result_excludes_llm_keys(fake_llm: MagicMock):
    """Subgraph results must not include llm_raa_a, llm_raa_b, llm_raa_c,
    llm_judge, or any ChatModel object."""
    from raa.graphs.subgraphs.raa_a import run_raa_a

    payload = {
        "batch": {"batch_id": 0},
        "batch_index": 0,
        "quality_weights": {},
        "running_arch_model": None,
        "bridge_requirements": {},
        "strategy": "saam_first",
        "llm": fake_llm,
    }
    result = run_raa_a(payload)
    forbidden = {"llm_raa_a", "llm_raa_b", "llm_raa_c", "llm_judge", "llm"}
    for key in forbidden:
        assert key not in result, f"Forbidden key in result: {key}"

    for value in result.values():
        assert not hasattr(value, "invoke"), f"LLM-like object found in result: {value}"


# ============================================================================
# T007 — fan_out_subgraphs Send payloads contain model_constraints
# ============================================================================


def test_fan_out_payloads_contain_model_constraints(fake_state: dict, fake_config: dict):
    """All three normal fan_out_subgraphs Send payloads carry identical model_constraints."""
    from raa.graphs.subgraphs.routing import fan_out_subgraphs

    sends = fan_out_subgraphs(fake_state, fake_config)
    assert len(sends) == 3

    constraints_values = []
    for s in sends:
        assert "model_constraints" in s.arg, f"Send to {s.node} missing model_constraints key"
        constraints_values.append(s.arg["model_constraints"])

    # All three must be identical (computed once, shared across sends)
    assert all(c == constraints_values[0] for c in constraints_values), (
        f"model_constraints differ across sends: {constraints_values}"
    )


def test_fan_out_payloads_model_constraints_prefixed(fake_state: dict, fake_config: dict):
    """model_constraints in Send payloads begins with WARNING_PREFIX when running_arch_model is non-empty."""
    from raa.graphs.subgraphs.routing import fan_out_subgraphs

    sends = fan_out_subgraphs(fake_state, fake_config)
    for s in sends:
        constraints = s.arg["model_constraints"]
        assert constraints, "model_constraints should be non-empty for populated running_arch_model"
        assert "already part of the architecture model" in constraints


def test_fan_out_payloads_model_constraints_empty_when_no_model(fake_config: dict):
    """model_constraints is empty string when running_arch_model is None."""
    from raa.graphs.subgraphs.routing import fan_out_subgraphs

    state = {
        "batch_queue": [{
            "batch_id": 0, "group_id": 1,
            "requirement_ids": ["R1"],
            "requirements": [{"id": "R1", "text": "Test"}],
            "reduced_confidence": False,
        }],
        "batch_cursor": 0,
        "quality_weights": {},
        "running_arch_model": None,
        "bridge_requirements": {},
        "embeddings_ready": True,
    }
    sends = fan_out_subgraphs(state, fake_config)
    for s in sends:
        assert s.arg["model_constraints"] == ""


# ============================================================================
# T008 — build_subgraph_prompt reads payload["model_constraints"]
# ============================================================================


def test_build_subgraph_prompt_reads_model_constraints():
    """build_subgraph_prompt uses payload['model_constraints'] under ## Existing Architecture Model."""
    from raa.graphs.subgraphs.common import build_subgraph_prompt

    constraints = (
        "The following components and relationships are already part of the architecture model. "
        "You must be consistent with them. Do not rename, restructure, or contradict any listed entity or relationship.\n\n"
        "System: sys1 - Main System (Primary system)"
    )
    payload = {
        "batch": {"requirements": []},
        "batch_index": 0,
        "quality_weights": {},
        "running_arch_model": {"systems": [{"id": "sys1", "name": "Main System", "description": "Primary system"}]},
        "bridge_requirements": {},
        "strategy": "saam_first",
        "llm": object(),
        "model_constraints": constraints,
    }
    prompt = build_subgraph_prompt(payload, "saam_first", {})
    assert "## Existing Architecture Model" in prompt
    assert "System: sys1 - Main System (Primary system)" in prompt
    assert "already part of the architecture model" in prompt
    # Should NOT contain the raw flat JSON dump
    assert '"systems"' not in prompt.split("## Existing Architecture Model")[1].split("##")[0]


def test_build_subgraph_prompt_empty_model_constraints():
    """build_subgraph_prompt handles empty model_constraints gracefully."""
    from raa.graphs.subgraphs.common import build_subgraph_prompt

    payload = {
        "batch": {"requirements": []},
        "batch_index": 0,
        "quality_weights": {},
        "running_arch_model": None,
        "bridge_requirements": {},
        "strategy": "saam_first",
        "llm": object(),
        "model_constraints": "",
    }
    prompt = build_subgraph_prompt(payload, "saam_first", {})
    assert "## Existing Architecture Model" in prompt
    # When model_constraints is empty, the prompt notes no existing model
    sections = prompt.split("## Existing Architecture Model")[1].split("##")
    assert "No existing architecture model yet" in sections[0]
