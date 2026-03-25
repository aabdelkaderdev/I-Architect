"""
Filtering Agent Node — Regex pre-filtering + LLM noise classification.

Implements: FR-FILT-001–008.
"""

from typing import Any
from core.interfaces.base_agent import BaseAgent


class FilteringAgentNode(BaseAgent):
    """LangGraph node for noise classification and requirement filtering.

    Two-pass filtering:
      Pass 1: Deterministic regex pattern matching (FR-FILT-003).
      Pass 2: LLM-based batch classification for ambiguous items (FR-FILT-005).
    """

    def __init__(self, llm_instance_name: str | None = None) -> None:
        super().__init__(agent_name="filtering", llm_instance_name=llm_instance_name)

    def invoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute filtering on extracted requirements.

        Reads: state['raw_requirements']
        Writes: state['filtered_requirements'], state['filtering_stats']

        Args:
            state: LangGraph pipeline state.

        Returns:
            Updated state with filtered requirements.
        """
        raise NotImplementedError

    def validate_output(self, output: Any) -> bool:
        """Validate filtering output matches FilteringBatchResult schema.

        Args:
            output: Raw filtering output.

        Returns:
            True if valid.
        """
        raise NotImplementedError

    def _regex_prefilter(self, requirements: list[dict]) -> tuple[list[dict], list[dict]]:
        """Pass 1: Regex pattern matching (FR-FILT-003).

        Args:
            requirements: Raw requirement list.

        Returns:
            Tuple of (clear_noise_items, ambiguous_items).
        """
        raise NotImplementedError

    def _llm_classify_batch(self, ambiguous: list[dict]) -> list[dict]:
        """Pass 2: LLM batch classification (FR-FILT-005).

        Args:
            ambiguous: Requirements that passed regex but need LLM classification.

        Returns:
            Classified requirement list.
        """
        raise NotImplementedError
