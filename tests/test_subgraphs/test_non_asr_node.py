"""Tests for NonASRSubgraph. Per FG-Phase-44 §2."""

from __future__ import annotations

import pytest

from raa.subgraphs.non_asr_node import NonASRSubgraph


class TestNonASRSubgraph:
    def test_assemble_prompt(self, empty_registry, sample_non_asrs):
        """Non-ASR assemble_prompt includes functional requirements, no QA weights."""
        non_asr = NonASRSubgraph()
        batch = {
            "batch_id": "concern_batch_1",
            "batch_type": "concern",
            "asrs": [],
            "non_asrs": sample_non_asrs,
            "quality_weights": {},
            "registry_snapshot": empty_registry,
        }
        sys_prompt, user_prompt = non_asr.assemble_prompt(batch)
        assert isinstance(sys_prompt, str)
        assert isinstance(user_prompt, str)
        assert len(sys_prompt) > 0
        assert len(user_prompt) > 0
        assert "REQ-010" in user_prompt
        # Non-ASR prompt must NOT include quality_weights or architectural decisions
        assert "quality_weights" not in sys_prompt
        assert "decisions" not in user_prompt

    def test_empty_non_asrs_returns_empty_list(self, sample_non_asrs):
        """Non-ASR build_proposals returns [] when batch has no non-ASRs."""
        non_asr = NonASRSubgraph()
        batch = {
            "batch_id": "concern_batch_1",
            "batch_type": "concern",
            "asrs": [],
            "non_asrs": [],
            "quality_weights": {},
            "registry_snapshot": {"entries": {}, "snapshot_after_batch": "none"},
        }
        result = non_asr.parse_response([], batch)
        assert result == []
