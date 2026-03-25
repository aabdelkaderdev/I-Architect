"""
LLM Configuration Schemas — Pydantic DTOs for LLM provider management.

Referenced by: FR-UI-026, FR-UI-009, FR-UI-011.
"""

from enum import Enum
from pydantic import BaseModel, Field


class LLMType(str, Enum):
    """Supported LLM provider types."""

    OLLAMA = "ollama"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    GROQ = "groq"


class LLMConfig(BaseModel):
    """Configuration for a single LLM instance."""

    name: str = Field(..., description="User-assigned LLM name (e.g., 'MyGPT4').")
    provider: LLMType = Field(..., description="Provider type.")
    model_name: str = Field(..., description="Model identifier (e.g., 'llama3', 'gemini-pro').")
    api_endpoint: str = Field(..., description="Base URL of the LLM API (e.g., 'http://localhost:11434').")
    api_key: str = Field(default="", description="API key (masked in UI, never logged).")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Sampling temperature.")


class LLMHealthCheckResult(BaseModel):
    """Result of an LLM pre-flight health check (FR-UI-011)."""

    llm_name: str = Field(...)
    reachable: bool = Field(default=False)
    model_available: bool = Field(default=False)
    error_message: str = Field(default="", description="Error details if check failed.")
