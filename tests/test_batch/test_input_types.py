"""Tests for batch input type validation. Per FG-Phase-44 §2."""

from __future__ import annotations

import pytest

from raa.validators import validate_batch_input


class TestBatchInputValidation:
    def test_concern_batch_input_validation(self):
        """Valid ConcernBatchInput passes validation."""
        batch = {
            "batch_id": "concern_batch_1",
            "batch_type": "concern",
            "asrs": [{"id": "REQ-001", "text": "Test", "quality_attributes": []}],
            "non_asrs": [],
            "quality_weights": {},
            "registry_snapshot": {"entries": {}, "snapshot_after_batch": "none"},
            "decisions": [{"selected_pattern": "Microservices"}],
            "condition": "high traffic",
        }
        result = validate_batch_input(batch)
        assert result is batch

    def test_foundation_batch_input_validation(self):
        """Valid FoundationBatchInput passes validation."""
        batch = {
            "batch_id": "foundation_batch",
            "batch_type": "foundation",
            "asrs": [{"id": "REQ-001", "text": "Test", "quality_attributes": []}],
            "non_asrs": [],
            "quality_weights": {},
            "registry_snapshot": {"entries": {}, "snapshot_after_batch": "none"},
        }
        result = validate_batch_input(batch)
        assert result is batch

    def test_batch_id_format(self):
        """Invalid batch_id format raises ValueError."""
        batch = {
            "batch_id": "bad_id",
            "batch_type": "concern",
            "asrs": [{"id": "REQ-001", "text": "Test", "quality_attributes": []}],
            "non_asrs": [],
            "quality_weights": {},
            "registry_snapshot": {"entries": {}, "snapshot_after_batch": "none"},
            "decisions": [],
            "condition": "",
        }
        with pytest.raises(ValueError):
            validate_batch_input(batch)
