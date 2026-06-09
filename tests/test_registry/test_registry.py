"""Tests for EntityRegistry. Per FG-Phase-44 §2."""

from __future__ import annotations

import pytest

from raa.registry.registry import EntityRegistry


class TestEntityRegistry:
    def test_snapshot_empty(self):
        """Empty registry snapshot has no entries and last_batch_id='none'."""
        reg = EntityRegistry()
        snap = reg.snapshot()
        assert snap["entries"] == {}
        assert snap["snapshot_after_batch"] == "none"

    def test_snapshot_after_register(self):
        """Snapshot after register reflects the registered entry."""
        reg = EntityRegistry()
        entry = {
            "canonical_id": "ENT-001",
            "canonical_name": "TestService",
            "c4_level": "container",
            "c4_type": "service",
            "source_requirements": ["REQ-001"],
            "authority": "asr",
            "variants": {},
            "description": "Test service.",
        }
        reg.register(entry)
        snap = reg.snapshot()
        assert "ENT-001" in snap["entries"]

    def test_register_new_entry(self):
        """Register adds an entry and makes it retrievable."""
        reg = EntityRegistry()
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
        reg.register(entry)
        found = reg.lookup(canonical_id="ENT-001")
        assert found is not None
        assert found["canonical_name"] == "TestService"

    def test_register_duplicate_raises(self):
        """Registering the same canonical_id twice raises ValueError."""
        reg = EntityRegistry()
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
        reg.register(entry)
        with pytest.raises(ValueError):
            reg.register(entry)

    def test_enrich_appends_requirements(self):
        """Enrich appends source_requirements with append_unique semantics."""
        reg = EntityRegistry()
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
        reg.register(entry)
        reg.enrich("ENT-001", {
            "canonical_id": "ENT-001",
            "canonical_name": "TestService",
            "c4_level": "container",
            "c4_type": "service",
            "source_requirements": ["REQ-002"],
            "authority": "asr",
            "variants": {},
            "description": "Test.",
        })
        found = reg.lookup(canonical_id="ENT-001")
        assert "REQ-001" in found["source_requirements"]
        assert "REQ-002" in found["source_requirements"]

    def test_enrich_rejects_name_overwrite(self):
        """Enrich raises ValueError when caller attempts to change canonical_name."""
        reg = EntityRegistry()
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
        reg.register(entry)
        with pytest.raises(ValueError):
            reg.enrich("ENT-001", {
                "canonical_id": "ENT-001",
                "canonical_name": "DifferentName",
                "c4_level": "container",
                "c4_type": "service",
                "source_requirements": [],
                "authority": "asr",
                "variants": {},
                "description": "Test.",
            })

    def test_lookup_by_id(self):
        """Lookup by canonical_id returns the correct entry."""
        reg = EntityRegistry()
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
        reg.register(entry)
        assert reg.lookup(canonical_id="ENT-001") is not None
        assert reg.lookup(canonical_id="ENT-999") is None

    def test_lookup_by_name(self):
        """Lookup by canonical_name returns the correct entry."""
        reg = EntityRegistry()
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
        reg.register(entry)
        found = reg.lookup(canonical_name="TestService")
        assert found is not None
        assert found["canonical_id"] == "ENT-001"
