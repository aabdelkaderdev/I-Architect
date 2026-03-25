"""
Custom domain exceptions for the I-Architect orchestrator.

Centralizes all business-rule exceptions to keep service code clean
and enable consistent error handling across the API layer.
"""


class IArchitectBaseError(Exception):
    """Base exception for all I-Architect domain errors."""

    pass


# ─────────────────────────────────────────────
# Pipeline Errors
# ─────────────────────────────────────────────

class PipelineCancelledError(IArchitectBaseError):
    """Raised when a pipeline run is cancelled by the user (FR-TASK-008)."""

    pass


class PipelineLockError(IArchitectBaseError):
    """Raised when a project is already locked by another pipeline run (FR-TASK-001)."""

    pass


# ─────────────────────────────────────────────
# Agent Errors
# ─────────────────────────────────────────────

class AgentValidationError(IArchitectBaseError):
    """Raised when an agent's output fails Pydantic schema validation."""

    pass


class AgentRetryExhaustedError(IArchitectBaseError):
    """Raised when an agent has exhausted all retry attempts."""

    pass


class LLMHallucinationError(IArchitectBaseError):
    """Raised when an LLM produces invalid data (e.g., invalid QA enum)."""

    pass


# ─────────────────────────────────────────────
# Extraction Errors
# ─────────────────────────────────────────────

class ExtractionCoverageError(IArchitectBaseError):
    """Raised when extraction coverage falls below 80% (DR-ING-001)."""

    pass


class SemanticDriftError(IArchitectBaseError):
    """Raised when semantic drift is detected in extracted requirements (DR-ING-002)."""

    pass


# ─────────────────────────────────────────────
# External Service Errors
# ─────────────────────────────────────────────

class PlantUMLSyntaxError(IArchitectBaseError):
    """Raised when PlantUML server returns HTTP 400 (syntax error)."""

    pass


class PlantUMLServerCrashError(IArchitectBaseError):
    """Raised when PlantUML server returns HTTP 500 (JVM crash/OOM)."""

    pass


class RenderTimeoutError(IArchitectBaseError):
    """Raised when PlantUML rendering exceeds 300-second timeout (FR-PUML-003)."""

    pass


class ChromaDBConnectionError(IArchitectBaseError):
    """Raised when ChromaDB is unreachable (DR-CHROMA-002)."""

    pass


# ─────────────────────────────────────────────
# Project State Errors
# ─────────────────────────────────────────────

class DiskQuotaExceededError(IArchitectBaseError):
    """Raised when a project exceeds its 500MB disk quota (FR-PSM-008)."""

    pass


class FileNamingViolationError(IArchitectBaseError):
    """Raised when a file save violates the naming convention (FR-PSM-004)."""

    pass


class DataIntegrityError(IArchitectBaseError):
    """Raised when TOON/JSON handoff validation fails (FR-PSM-014)."""

    pass


# ─────────────────────────────────────────────
# ARLO Errors
# ─────────────────────────────────────────────

class ILPSolverTimeoutError(IArchitectBaseError):
    """Raised when the ILP solver exceeds its timeout (DR-ARLO-001)."""

    pass


class MemoryOverflowError(IArchitectBaseError):
    """Raised when ARLO's memory buffer exceeds context limits (DR-ARLO-003)."""

    pass
