"""Tests for RegistryDelta construction. Per FG-Phase-44 §2."""

from __future__ import annotations

import pytest

from raa.registry.delta import build_delta


class TestRegistryDelta:
    def test_delta_new_entries(self):
        """RegistryDelta records newly registered entries."""
        entry = {
            "canonical_id": "ENT-001",
            "canonical_name": "TestService",
            "c4_level": "container",
            "c4_type": "service",
            "source_requirements": ["REQ-001"],
            "authority": "asr",
            "variants": {},
            "description": "Test.",
        }
        delta = build_delta([entry], [])
        assert delta["new_entries"] == [entry]
        assert delta["enriched_ids"] == []

    def test_delta_enriched_ids(self):
        """RegistryDelta records enriched canonical_ids."""
        delta = build_delta([], ["ENT-001", "ENT-002"])
        assert delta["new_entries"] == []
        assert delta["enriched_ids"] == ["ENT-001", "ENT-002"]

    def test_delta_disjointness_validation(self):
        """Build_delta raises ValueError when enriched_ids overlaps with new_entries."""
        entry = {
            "canonical_id": "ENT-001",
            "canonical_name": "TestService",
            "c4_level": "container",
            "c4_type": "service",
            "source_requirements": ["REQ-001"],
            "authority": "asr",
            "variants": {},
            "description": "Test.",
        }
        with pytest.raises(ValueError):
            build_delta([entry], ["ENT-001"])
