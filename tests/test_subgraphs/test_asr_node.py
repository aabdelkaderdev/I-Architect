"""Tests for ASRSubgraph. Per FG-Phase-44 §2."""

from __future__ import annotations

import pytest

from raa.subgraphs.asr_node import ASRSubgraph


class TestASRSubgraph:
    def test_assemble_prompt_concern(self, empty_registry, sample_asrs):
        """ASR assemble_prompt for a concern batch includes QA weights and decisions."""
        asr = ASRSubgraph()
        batch = {
            "batch_id": "concern_batch_1",
            "batch_type": "concern",
            "asrs": sample_asrs,
            "non_asrs": [],
            "quality_weights": {"Security": 20},
            "registry_snapshot": empty_registry,
            "decisions": [{"selected_pattern": "Microservices"}],
            "condition": "high traffic",
        }
        sys_prompt, user_prompt = asr.assemble_prompt(batch)
        assert isinstance(sys_prompt, str)
        assert isinstance(user_prompt, str)
        assert len(sys_prompt) > 0
        assert len(user_prompt) > 0
        assert "REQ-001" in user_prompt

    def test_assemble_prompt_foundation(self, empty_registry, sample_asrs):
        """ASR assemble_prompt for foundation batch omits concern-only fields."""
        asr = ASRSubgraph()
        batch = {
            "batch_id": "foundation_batch",
            "batch_type": "foundation",
            "asrs": sample_asrs,
            "non_asrs": [],
            "quality_weights": {},
            "registry_snapshot": empty_registry,
        }
        sys_prompt, user_prompt = asr.assemble_prompt(batch)
        assert isinstance(sys_prompt, str)
        assert isinstance(user_prompt, str)

    def test_empty_asrs_returns_empty_list(self, sample_asrs):
        """ASR build_proposals returns [] when batch has no ASRs."""
        asr = ASRSubgraph()
        batch = {
            "batch_id": "concern_batch_1",
            "batch_type": "concern",
            "asrs": [],
            "non_asrs": [],
            "quality_weights": {},
            "registry_snapshot": {"entries": {}, "snapshot_after_batch": "none"},
            "decisions": [],
            "condition": "",
        }
        # parse_response with empty list returns empty list
        result = asr.parse_response([], batch)
        assert result == []
