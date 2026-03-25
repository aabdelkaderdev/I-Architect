"""
Regex Extraction Strategy (Strategy B — Agent-Assisted).

Implements: FR-ING-008. Uses LLM to identify repeating patterns,
then executes regex over entire document.
"""

from typing import Any
from core.interfaces.base_extraction_strategy import BaseExtractionStrategy


class RegexStrategy(BaseExtractionStrategy):
    """Agent-assisted regex extraction for formatted documents."""

    @property
    def strategy_name(self) -> str:
        return "Regex"

    def extract(self, text: str, file_hash_prefix: str, **kwargs: Any) -> list[dict[str, Any]]:
        """Send first 1000 tokens to LLM for pattern identification, then regex.

        Args:
            text: Raw document text.
            file_hash_prefix: SHA-256 prefix for UID generation.
            **kwargs: Must include 'llm_client' for pattern identification.

        Returns:
            List of ExtractedRequirement dictionaries.
        """
        raise NotImplementedError

    def supports_auto_correction(self) -> bool:
        return False
