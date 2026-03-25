"""
Line-by-Line Extraction Strategy (Strategy A — Deterministic).

Implements: FR-ING-007. Splits text by newline, filters noise lines.
No LLM cost incurred.
"""

from typing import Any
from core.interfaces.base_extraction_strategy import BaseExtractionStrategy


class LineByLineStrategy(BaseExtractionStrategy):
    """Deterministic line-by-line extraction for pre-formatted text."""

    @property
    def strategy_name(self) -> str:
        return "Line-by-Line"

    def extract(self, text: str, file_hash_prefix: str, **kwargs: Any) -> list[dict[str, Any]]:
        """Split text by newline, filter empty/short lines, assign UIDs.

        Args:
            text: Raw document text.
            file_hash_prefix: SHA-256 prefix for UID generation.

        Returns:
            List of ExtractedRequirement dictionaries.
        """
        raise NotImplementedError

    def supports_auto_correction(self) -> bool:
        return False
