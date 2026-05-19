"""Integration tests for RAA workflow: overlap bridging and judge non-contradiction."""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock

from raa.nodes.overlap_bridging import apply_overlap_bridging
from raa.nodes.judge import judge_batch, LLM_JUDGE_KEY
from raa.state.types import (
    ArchFragment,
    ArchModel,
    ArchSystem,
    ArchContainer,
    ArchComponent,
    OpenQuestion,
)


def _centroid(active_idx: int) -> list[float]:
    """1024-dim unit vector active on a single index."""
    arr = [0.0] * 1024
    arr[active_idx] = 1.0
    return arr


def _bridge_vec(idx1: int, idx2: int) -> list[float]:
    """1024-dim vector halfway between two indices."""
    arr = [0.0] * 1024
    arr[idx1] = 0.707
    arr[idx2] = 0.707
    return arr


def test_end_to_end_3_batch_bridge_overlap():
    """T022: Simulates a 3-batch sequence with adjacent centroids and bridge overlap injection."""
    # Centroids: Batch 0 active at index 0, Batch 1 at index 1, Batch 2 at index 2
    # They are adjacent because cosine is 0 (orthogonal) but we can set cluster label "C1" to trigger adjacency.
    b0 = {
        "batch_id": 0,
        "group_id": 10,
        "requirement_ids": ["R1"],
        "requirements": [{"id": "R1", "text": "Requirement 1"}],
        "group_centroid": _centroid(0),
        "cluster": ["C1"],
        "similarity_scores": {"R1": 1.0},
        "non_asr_candidates": [
            {"id": "R_bridge12", "text": "Bridge between 0 and 1", "embedding": _bridge_vec(0, 1)}
        ],
    }

    b1 = {
        "batch_id": 1,
        "group_id": 11,
        "requirement_ids": ["R2"],
        "requirements": [{"id": "R2", "text": "Requirement 2"}],
        "group_centroid": _centroid(1),
        "cluster": ["C1"],
        "similarity_scores": {"R2": 1.0},
        "non_asr_candidates": [
            {"id": "R_bridge12", "text": "Bridge between 0 and 1", "embedding": _bridge_vec(0, 1)},
            {"id": "R_bridge23", "text": "Bridge between 1 and 2", "embedding": _bridge_vec(1, 2)},
        ],
    }

    b2 = {
        "batch_id": 2,
        "group_id": 12,
        "requirement_ids": ["R3"],
        "requirements": [{"id": "R3", "text": "Requirement 3"}],
        "group_centroid": _centroid(2),
        "cluster": ["C1"],
        "similarity_scores": {"R3": 1.0},
        "non_asr_candidates": [
            {"id": "R_bridge23", "text": "Bridge between 1 and 2", "embedding": _bridge_vec(1, 2)}
        ],
    }

    state = {
        "batch_queue": [b0, b1, b2],
        "bridge_requirements": {},
    }

    result = apply_overlap_bridging(state)
    bq = result["batch_queue"]
    br = result["bridge_requirements"]

    # Verify bridge requirement IDs generated
    assert (10, 11) in br
    assert (11, 12) in br
    assert "R_bridge12" in br[(10, 11)]
    assert "R_bridge23" in br[(11, 12)]

    # Verify both adjacent batches contain the bridge requirement IDs
    # Batch 0 and Batch 1 share R_bridge12
    assert "R_bridge12" in bq[0]["requirement_ids"]
    assert "R_bridge12" in bq[1]["requirement_ids"]

    # Batch 1 and Batch 2 share R_bridge23
    assert "R_bridge23" in bq[1]["requirement_ids"]
    assert "R_bridge23" in bq[2]["requirement_ids"]


def test_judge_running_arch_model_non_contradiction():
    """T023: Run the judge node with a new batch containing conflicting hierarchy parent IDs."""
    # Build a running_arch_model containing a container and system
    running_model = ArchModel(
        systems=[
            ArchSystem(id="sys_a", label="System A", description="System A"),
            ArchSystem(id="sys_b", label="System B", description="System B"),
        ]
    )
    # The existing container is parented by sys_a
    running_model.systems[0].containers = [
        ArchContainer(id="cont_a", label="Container A", description="Standard API", parent_system_id="sys_a")
    ]

    # Primary fragment (raa_a) matches the running model
    primary_fragment = ArchFragment(
        systems=[],
        containers=[
            ArchContainer(id="cont_a", label="Container A", description="Standard API", parent_system_id="sys_a", source_fragment="raa_a")
        ],
    )

    # Conflicting fragment (raa_b) has a different parent for cont_a
    conflict_fragment = ArchFragment(
        systems=[],
        containers=[
            ArchContainer(id="cont_a", label="Container A", description="Conflicting parent", parent_system_id="sys_b", source_fragment="raa_b")
        ],
    )

    state = {
        "batch_outputs": {0: [primary_fragment, conflict_fragment]},
        "batch_cursor": 0,
        "batch_queue": [{"batch_id": 0, "requirements": [{"id": "R1"}], "reduced_confidence": False}],
        "quality_weights": {},
        "running_arch_model": running_model,
        "open_questions": [],
    }

    # Mock llm_judge to score primary_fragment higher than conflict_fragment
    llm = MagicMock()
    llm.invoke.return_value = {
        "scores": [
            {
                "source_fragment": "raa_a",
                "base_score": 9.5,
                "covered_entity_ids": ["cont_a"],
                "covered_relationship_keys": [],
            },
            {
                "source_fragment": "raa_b",
                "base_score": 5.0,
                "covered_entity_ids": ["cont_a"],
                "covered_relationship_keys": [],
            }
        ]
    }

    config = {"context": {LLM_JUDGE_KEY: llm}}

    # Run the judge node
    result = judge_batch(state, config)

    # Assert that a hierarchy conflict was appended to open_questions
    assert "open_questions" in result
    questions = result["open_questions"]
    assert len(questions) > 0
    assert any(oq.type == "hierarchy_conflict" for oq in questions)
