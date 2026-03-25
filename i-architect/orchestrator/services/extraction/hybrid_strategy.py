"""
Hybrid Extraction Strategy (Strategy D — Catch-All).

Implements: FR-ING-011. Combines Regex + LLM with fuzzy deduplication.
"""

from typing import Any
from core.interfaces.base_extraction_strategy import BaseExtractionStrategy


class HybridStrategy(BaseExtractionStrategy):
    """Hybrid (Regex + LLM) extraction with fuzzy deduplication."""

    @property
    def strategy_name(self) -> str:
        return "Hybrid"

    def extract(self, text: str, file_hash_prefix: str, **kwargs: Any) -> list[dict[str, Any]]:
        """Execute Regex pass, then LLM pass, then merge with deduplication.

        Pass 1: Rigid regex matching.
        Pass 2: LLM extraction as JSON.
        Pass 3: Set union + fuzzy dedup (Levenshtein > 95% = duplicate, prefer LLM).

        Args:
            text: Raw document text.
            file_hash_prefix: SHA-256 prefix for UID generation.
            **kwargs: Must include 'llm_client'.

        Returns:
            Deduplicated list of ExtractedRequirement dictionaries.
        """
        raise NotImplementedError

    def supports_auto_correction(self) -> bool:
        return True
