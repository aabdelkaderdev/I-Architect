"""
BaseLLMClient — Abstract Base Class for LLM client creation.

Implements the Factory Pattern for instantiating LangChain Chat Model
clients across supported providers: Ollama, Deepseek, Google Gemini, Groq.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseLLMClient(ABC):
    """Abstract factory interface for creating LangChain Chat Model instances.

    Concrete implementations create provider-specific clients
    (Ollama, Deepseek, Gemini, Groq) while exposing a uniform interface.
    """

    @abstractmethod
    def create_client(
        self,
        provider: str,
        model_name: str,
        api_endpoint: str,
        api_key: str | None = None,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> Any:
        """Create and return a LangChain Chat Model client.

        Args:
            provider: LLM provider type ("ollama", "deepseek", "gemini", "groq").
            model_name: The model identifier (e.g., "llama3", "gemini-pro").
            api_endpoint: The base URL of the LLM API endpoint.
            api_key: Optional API key for authentication.
            temperature: Sampling temperature (0.0–1.0).
            **kwargs: Additional provider-specific parameters.

        Returns:
            A configured LangChain BaseChatModel instance.

        Raises:
            NotImplementedError: Subclasses must implement this method.
            ValueError: If the provider type is not supported.
        """
        raise NotImplementedError

    @abstractmethod
    def health_check(
        self,
        provider: str,
        model_name: str,
        api_endpoint: str,
        api_key: str | None = None,
    ) -> bool:
        """Perform a pre-flight connectivity and model availability check.

        FR-UI-011: Before initiating any workflow, verify LLM reachability.

        Args:
            provider: LLM provider type.
            model_name: The model identifier.
            api_endpoint: The base URL of the LLM API endpoint.
            api_key: Optional API key for authentication.

        Returns:
            True if the endpoint is reachable and the model is available.
        """
        raise NotImplementedError
