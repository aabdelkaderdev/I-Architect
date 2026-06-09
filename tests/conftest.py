"""Shared test fixtures for RAA unit tests. Per FG-Phase-44 §1.

Fixtures:
    - empty_registry: Frozen snapshot with zero entries (first batch scenario).
    - sample_asrs: 3-5 ASREntry dicts with realistic QA labels.
    - sample_non_asrs: 3-5 NonASREntry dicts.
    - sample_proposals: Mix of ASR and Non-ASR EntityProposal dicts for Judge testing.
    - mock_llm: BaseChatModel fake that returns pre-defined structured output.
    - sample_registry_snapshot: Pre-populated registry snapshot for mid-run testing.

No unittest classes — pytest functions with fixtures. No integration tests at this level.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pytest

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel
    from raa.types import (
        ASREntry,
        EntityProposal,
        NonASREntry,
        RegistrySnapshot,
    )


@pytest.fixture
def empty_registry() -> RegistrySnapshot:
    """A RegistrySnapshot with zero entries — first batch scenario."""
    return {
        "entries": {},
        "snapshot_after_batch": "none",
    }


@pytest.fixture
def sample_asrs() -> list[ASREntry]:
    """3-5 ASREntry dicts with realistic QA labels."""
    return [
        {
            "id": "REQ-001",
            "text": "The system shall handle 10,000 concurrent users.",
            "quality_attributes": ["Performance Efficiency"],
        },
        {
            "id": "REQ-002",
            "text": "All user data must be encrypted at rest and in transit.",
            "quality_attributes": ["Security"],
        },
        {
            "id": "REQ-003",
            "text": "The system must achieve 99.99% uptime.",
            "quality_attributes": ["Reliability"],
        },
        {
            "id": "REQ-004",
            "text": "New deployment must not exceed 5 minutes of downtime.",
            "quality_attributes": ["Maintainability"],
        },
    ]


@pytest.fixture
def sample_non_asrs() -> list[NonASREntry]:
    """3-5 NonASREntry dicts."""
    return [
        {"id": "REQ-010", "text": "The system should support OAuth2 and biometric login."},
        {"id": "REQ-011", "text": "Users should be able to export their data as CSV."},
        {"id": "REQ-012", "text": "The application must be accessible via mobile and desktop browsers."},
    ]


@pytest.fixture
def sample_proposals() -> list[EntityProposal]:
    """A mix of ASR and Non-ASR EntityProposal objects for Judge testing."""
    return [
        {
            "proposed_name": "AuthenticationService",
            "c4_level": "container",
            "c4_type": "service",
            "description": "Handles user authentication and session management.",
            "responsibilities": ["Verify credentials", "Issue tokens", "Manage sessions"],
            "source_requirements": ["REQ-010"],
            "proposing_subgraph": "non_asr",
            "justification": "OAuth2 and biometric login requires a dedicated auth service.",
        },
        {
            "proposed_name": "LoadBalancerService",
            "c4_level": "container",
            "c4_type": "service",
            "description": "Distributes incoming requests across service instances.",
            "responsibilities": ["Health checking", "Request routing", "TLS termination"],
            "source_requirements": ["REQ-001"],
            "proposing_subgraph": "asr",
            "justification": "10,000 concurrent users require load distribution.",
        },
        {
            "proposed_name": "UserDatabase",
            "c4_level": "container",
            "c4_type": "database",
            "description": "Persistent storage for user accounts and credentials.",
            "responsibilities": ["Store user profiles", "Store credential hashes"],
            "source_requirements": ["REQ-002", "REQ-010"],
            "proposing_subgraph": "asr",
            "justification": "Encrypted user data requires a secure database.",
        },
    ]


@pytest.fixture
def mock_llm() -> BaseChatModel:
    """A BaseChatModel fake that returns pre-defined structured output.

    Tests configure the mock's return values per test case. This fixture
    provides a consistent mock instance satisfying the BaseChatModel interface.
    """
    mock = MagicMock()
    return mock


@pytest.fixture
def sample_registry_snapshot() -> RegistrySnapshot:
    """A registry snapshot with pre-populated entries for mid-run testing."""
    return {
        "entries": {
            "ENT-001": {
                "canonical_id": "ENT-001",
                "canonical_name": "ApiGateway",
                "c4_level": "container",
                "c4_type": "gateway",
                "source_requirements": ["REQ-001"],
                "authority": "asr",
                "variants": {},
                "description": "API Gateway for external request routing.",
            },
        },
        "snapshot_after_batch": "concern_batch_1",
    }
