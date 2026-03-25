"""
Grammar-Based Decoding Strategy (Strategy C — Constrained).

Implements: FR-ING-009. Uses LangChain PydanticOutputParser or
Outlines/Guidance to enforce structured output from LLM.
"""

from typing import Any
from core.interfaces.base_extraction_strategy import BaseExtractionStrategy


class GrammarBasedStrategy(BaseExtractionStrategy):
    """Constrained LLM extraction for unstructured prose."""

    @property
    def strategy_name(self) -> str:
        return "Grammar-Based"

    def extract(self, text: str, file_hash_prefix: str, **kwargs: Any) -> list[dict[str, Any]]:
        """Use PydanticOutputParser to constrain LLM to output valid JSON.

        Handles token budget checks (FR-ING-010) — if prompt exceeds
        max_input_tokens × 0.85, switches to map-reduce chunking.

        Args:
            text: Raw document text.
            file_hash_prefix: SHA-256 prefix for UID generation.
            **kwargs: Must include 'llm_client'.

        Returns:
            List of ExtractedRequirement dictionaries.
        """
        raise NotImplementedError

    def supports_auto_correction(self) -> bool:
        return True
