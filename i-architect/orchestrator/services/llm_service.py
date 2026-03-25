"""
LLM Service — Factory for LangChain Chat Model clients.

Implements: BaseLLMClient interface, FR-UI-011 (preflight health check), FR-UI-026.
"""

from typing import Any
from core.interfaces.base_llm_client import BaseLLMClient


class LLMService(BaseLLMClient):
    """Concrete factory for creating LangChain Chat Model instances.

    Supports: Ollama, Deepseek, Google Gemini, Groq.
    """

    def create_client(
        self,
        provider: str,
        model_name: str,
        api_endpoint: str,
        api_key: str | None = None,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> Any:
        """Create a provider-specific LangChain chat model client.

        Args:
            provider: "ollama", "deepseek", "gemini", or "groq".
            model_name: Model identifier.
            api_endpoint: Base URL.
            api_key: Optional API key.
            temperature: Sampling temperature (0.0–1.0).

        Returns:
            Configured LangChain BaseChatModel instance.
        """
        raise NotImplementedError

    def health_check(
        self,
        provider: str,
        model_name: str,
        api_endpoint: str,
        api_key: str | None = None,
    ) -> bool:
        """Pre-flight connectivity and model availability check (FR-UI-011).

        Args:
            provider: Provider type.
            model_name: Model identifier.
            api_endpoint: Base URL.
            api_key: Optional API key.

        Returns:
            True if reachable and model available.
        """
        raise NotImplementedError
