"""
BaseExtractionStrategy — Abstract Base Class for extraction strategies.

Implements the Strategy Pattern for the Ingestion & Extraction layer.
Concrete strategies: LineByLine, Regex, GrammarBased, Hybrid (FR-ING-007–011).
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseExtractionStrategy(ABC):
    """Abstract interface for requirement extraction strategies.

    Each strategy converts raw document text into structured requirement
    objects. The IngestionService selects and delegates to the appropriate
    concrete strategy based on user selection or auto-correction logic.
    """

    @property
    @abstractmethod
    def strategy_name(self) -> str:
        """Return the human-readable name of this extraction strategy.

        Returns:
            Strategy name string (e.g., "Line-by-Line", "Regex").
        """
        ...

    @abstractmethod
    def extract(
        self,
        text: str,
        file_hash_prefix: str,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Extract structured requirements from raw document text.

        Args:
            text: The raw text content of the uploaded document.
            file_hash_prefix: First 6 chars of the SHA-256 file hash for UID gen.
            **kwargs: Additional strategy-specific parameters.

        Returns:
            List of extracted requirement dictionaries conforming to
            the ExtractedRequirement schema.

        Raises:
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError

    @abstractmethod
    def supports_auto_correction(self) -> bool:
        """Whether this strategy can be used as an auto-correction target.

        Returns:
            True if this strategy supports being escalated to.
        """
        raise NotImplementedError
