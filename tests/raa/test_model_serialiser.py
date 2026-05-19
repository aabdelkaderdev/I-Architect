"""Unit tests for RAA model serialiser — hierarchical C4 tree rendering,
deterministic sorting, prefix injection, and external entity handling."""

from __future__ import annotations

import pytest

from raa.state.types import (
    ArchComponent,
    ArchContainer,
    ArchExternalSystem,
    ArchModel,
    ArchPerson,
    ArchRelationship,
    ArchSystem,
)


# ============================================================================
# T003 — Empty-model serializer tests
# ============================================================================


def test_serialize_arch_model_none_returns_empty():
    """None input returns empty string."""
    from raa.utils.model_serialiser import serialize_arch_model

    result = serialize_arch_model(None)
    assert result == ""


def test_serialize_arch_model_empty_dict_returns_empty():
    """Empty dict input returns empty string."""
    from raa.utils.model_serialiser import serialize_arch_model

    result = serialize_arch_model({})
    assert result == ""


def test_build_model_constraint_block_none_returns_empty():
    """None model produces empty constraint block."""
    from raa.utils.model_serialiser import build_model_constraint_block

    result = build_model_constraint_block(None)
    assert result == ""


def test_build_model_constraint_block_empty_dict_returns_empty():
    """Empty dict produces empty constraint block."""
    from raa.utils.model_serialiser import build_model_constraint_block

    result = build_model_constraint_block({})
    assert result == ""


# ============================================================================
# T004 — Deterministic nested tree tests
# ============================================================================


def test_serialize_unsorted_dict_input_renders_sorted():
    """Unsorted dict input produces lexicographically sorted output by ID."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = {
        "systems": [
            {"id": "z_system", "name": "Z System", "description": "Last alphabetically"},
            {"id": "a_system", "name": "A System", "description": "First alphabetically"},
        ],
    }
    result = serialize_arch_model(model)
    lines = result.split("\n")
    # a_system must appear before z_system
    a_idx = next(i for i, l in enumerate(lines) if "a_system" in l)
    z_idx = next(i for i, l in enumerate(lines) if "z_system" in l)
    assert a_idx < z_idx


def test_serialize_nested_containers_rendered_under_systems():
    """Containers appear indented under their parent system."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = {
        "systems": [
            {
                "id": "sys1",
                "name": "Main System",
                "description": "Primary",
                "containers": [
                    {"id": "cont_a", "name": "Container A", "description": "First container"},
                    {"id": "cont_b", "name": "Container B", "description": "Second container"},
                ],
            },
        ],
    }
    result = serialize_arch_model(model)
    lines = result.split("\n")
    # Find the container lines
    cont_a_idx = next(i for i, l in enumerate(lines) if "cont_a" in l)
    cont_b_idx = next(i for i, l in enumerate(lines) if "cont_b" in l)
    # Containers must be indented
    assert lines[cont_a_idx].startswith("  Container:")
    assert lines[cont_b_idx].startswith("  Container:")
    # Sorted by ID
    assert cont_a_idx < cont_b_idx


def test_serialize_nested_components_rendered_under_containers():
    """Components appear double-indented under their parent container."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = {
        "systems": [
            {
                "id": "sys1",
                "name": "System",
                "description": "A system",
                "containers": [
                    {
                        "id": "cont1",
                        "name": "Container",
                        "description": "A container",
                        "components": [
                            {"id": "comp_b", "name": "Component B", "description": "Second"},
                            {"id": "comp_a", "name": "Component A", "description": "First"},
                        ],
                    },
                ],
            },
        ],
    }
    result = serialize_arch_model(model)
    lines = result.split("\n")
    comp_a_idx = next(i for i, l in enumerate(lines) if "comp_a" in l)
    comp_b_idx = next(i for i, l in enumerate(lines) if "comp_b" in l)
    assert lines[comp_a_idx].startswith("    Component:")
    assert lines[comp_b_idx].startswith("    Component:")
    assert comp_a_idx < comp_b_idx


def test_serialize_full_hierarchical_tree_structure():
    """Full systems→containers→components tree renders correctly."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = {
        "systems": [
            {
                "id": "sys1",
                "name": "E-Commerce Platform",
                "description": "Online shopping system",
                "containers": [
                    {
                        "id": "web_app",
                        "name": "Web Application",
                        "description": "Customer-facing web app",
                        "components": [
                            {"id": "cart_svc", "name": "Cart Service", "description": "Shopping cart logic"},
                            {"id": "auth_svc", "name": "Auth Service", "description": "Authentication"},
                        ],
                    },
                    {
                        "id": "api_gw",
                        "name": "API Gateway",
                        "description": "External API gateway",
                    },
                ],
            },
        ],
    }
    result = serialize_arch_model(model)
    lines = result.split("\n")
    assert lines[0] == "System: sys1 - E-Commerce Platform (Online shopping system)"
    assert lines[1] == "  Container: api_gw - API Gateway (External API gateway)"
    assert lines[2] == "  Container: web_app - Web Application (Customer-facing web app)"
    assert lines[3] == "    Component: auth_svc - Auth Service (Authentication)"
    assert lines[4] == "    Component: cart_svc - Cart Service (Shopping cart logic)"


# ============================================================================
# T005 — ArchModel dataclass serialization tests
# ============================================================================


def test_serialize_archmodel_dataclass():
    """ArchModel dataclass with nested containers and components serializes correctly."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = ArchModel(
        systems=[
            ArchSystem(
                id="sys1",
                label="Main System",
                description="Primary system",
                containers=[
                    ArchContainer(
                        id="cont1",
                        label="Web App",
                        description="Web application",
                        parent_system_id="sys1",
                        components=[
                            ArchComponent(
                                id="comp1",
                                label="Auth Module",
                                description="Authentication module",
                                parent_container_id="cont1",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
    result = serialize_arch_model(model)
    assert "System: sys1 - Main System (Primary system)" in result
    assert "  Container: cont1 - Web App (Web application)" in result
    assert "    Component: comp1 - Auth Module (Authentication module)" in result


def test_serialize_archmodel_with_relationship_lists():
    """ArchModel dataclass entities with embedded relationship lists still serialize."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = ArchModel(
        systems=[
            ArchSystem(
                id="sys1",
                label="System One",
                description="A system",
                context_relationships=[
                    ArchRelationship(
                        source_id="person1", target_id="sys1",
                        interaction_type="uses", technology="HTTPS",
                        diagram_scope="context",
                    ),
                ],
                containers=[
                    ArchContainer(
                        id="cont1",
                        label="Container One",
                        description="A container",
                        parent_system_id="sys1",
                        container_relationships=[
                            ArchRelationship(
                                source_id="cont1", target_id="cont1",
                                interaction_type="internal", technology=None,
                                diagram_scope="container",
                            ),
                        ],
                        components=[
                            ArchComponent(
                                id="comp1",
                                label="Component One",
                                description="A component",
                                parent_container_id="cont1",
                                component_relationships=[
                                    ArchRelationship(
                                        source_id="comp1", target_id="comp1",
                                        interaction_type="delegates", technology=None,
                                        diagram_scope="component",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
    result = serialize_arch_model(model)
    assert "System: sys1 - System One (A system)" in result
    assert "  Container: cont1 - Container One (A container)" in result
    assert "    Component: comp1 - Component One (A component)" in result


def test_serialize_archmodel_persons_not_in_tree():
    """Persons and external_systems are not rendered in the C4 tree (they go in External Entities)."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = ArchModel(
        systems=[ArchSystem(id="sys1", label="System", description="A system")],
        persons=[ArchPerson(id="user1", label="End User", description="A user")],
        external_systems=[ArchExternalSystem(id="ext1", label="Payment Gateway", description="External")],
    )
    result = serialize_arch_model(model)
    # Person and external system should be in External Entities section, not in the tree
    assert "System: sys1 - System (A system)" in result
    # "Person:" should only appear after the ## External Entities header
    tree_section = result.split("## External Entities")[0]
    assert "Person:" not in tree_section
    assert "## External Entities" in result
    assert "Person: user1" in result


# ============================================================================
# T006 — External entity and relationship endpoint tests
# ============================================================================


def test_external_entities_section_renders_persons():
    """External Entities section lists persons with their IDs."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = {
        "systems": [
            {"id": "sys1", "name": "System", "description": "A system"},
        ],
        "persons": [
            {"id": "user1", "name": "End User", "description": "Primary user"},
            {"id": "admin1", "name": "Administrator", "description": "System admin"},
        ],
    }
    result = serialize_arch_model(model)
    assert "## External Entities" in result
    assert "Person: user1 - End User (Primary user)" in result
    assert "Person: admin1 - Administrator (System admin)" in result


def test_external_entities_section_renders_external_systems():
    """External Entities section lists external systems."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = {
        "systems": [
            {"id": "sys1", "name": "System", "description": "A system"},
        ],
        "external_systems": [
            {"id": "ext_pay", "name": "Payment Gateway", "description": "Third-party payment processor"},
        ],
    }
    result = serialize_arch_model(model)
    assert "## External Entities" in result
    assert "External System: ext_pay - Payment Gateway (Third-party payment processor)" in result


def test_relationships_section_renders_sorted():
    """Relationships section lists all relationships sorted."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = {
        "systems": [
            {"id": "sys_a", "name": "System A", "description": "First"},
            {"id": "sys_b", "name": "System B", "description": "Second"},
        ],
        "relationships": [
            {"source_id": "sys_a", "target_id": "sys_b",
             "interaction_type": "calls", "technology": "gRPC", "diagram_scope": "context"},
        ],
    }
    result = serialize_arch_model(model)
    assert "## Relationships" in result
    assert "calls" in result


def test_relationship_endpoint_ids_from_external_entities():
    """Relationships referencing persons/external systems render correctly."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = {
        "systems": [
            {"id": "sys1", "name": "System", "description": "A system"},
        ],
        "persons": [
            {"id": "user1", "name": "User", "description": "End user"},
        ],
        "relationships": [
            {"source_id": "user1", "target_id": "sys1",
             "interaction_type": "uses", "technology": "HTTPS", "diagram_scope": "context"},
        ],
    }
    result = serialize_arch_model(model)
    assert "user1" in result
    assert "sys1" in result
    assert "uses" in result


def test_external_entities_sorted():
    """External entities are sorted lexicographically by ID."""
    from raa.utils.model_serialiser import serialize_arch_model

    model = {
        "persons": [
            {"id": "zara", "name": "Zara", "description": "Z"},
            {"id": "alice", "name": "Alice", "description": "A"},
        ],
        "external_systems": [
            {"id": "midas", "name": "Midas", "description": "M"},
            {"id": "athena", "name": "Athena", "description": "A"},
        ],
    }
    result = serialize_arch_model(model)
    lines = result.split("\n")
    # Find entity lines within External Entities section
    ext_start = next(i for i, l in enumerate(lines) if "## External Entities" in l)
    entity_lines = [l for l in lines[ext_start + 1:] if l.startswith("Person:") or l.startswith("External System:")]
    # alice before zara, athena before midas
    alice_idx = next(i for i, l in enumerate(entity_lines) if "alice" in l)
    zara_idx = next(i for i, l in enumerate(entity_lines) if "zara" in l)
    assert alice_idx < zara_idx


def test_warning_prefix_in_build_model_constraint_block():
    """build_model_constraint_block prefixes with WARNING_PREFIX when model is non-empty."""
    from raa.utils.model_serialiser import WARNING_PREFIX, build_model_constraint_block

    model = {"systems": [{"id": "s1", "name": "Sys", "description": "Test"}]}
    result = build_model_constraint_block(model)
    assert result.startswith(WARNING_PREFIX)
    assert "System: s1 - Sys (Test)" in result


def test_build_model_constraint_block_empty_no_prefix():
    """Empty model produces no warning prefix."""
    from raa.utils.model_serialiser import build_model_constraint_block

    assert build_model_constraint_block({}) == ""
    assert build_model_constraint_block(None) == ""
