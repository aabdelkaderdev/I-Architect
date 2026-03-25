"""
BaseAggregationStrategy — Abstract Base Class for MCP aggregation strategies.

Implements the Strategy Pattern for merging parallel agent outputs.
Different agents use different merge strategies:
  - RAA/AGA: LLM-based semantic synthesis (FR-MCP-005, FR-MCP-006)
  - SA: Deterministic median voting (FR-MCP-007)
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseAggregationStrategy(ABC):
    """Abstract interface for MCP Aggregator merge strategies."""

    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Return the target agent type this strategy aggregates for.

        Returns:
            Agent type string (e.g., "raa", "aga", "sa").
        """
        ...

    @abstractmethod
    def aggregate(
        self,
        outputs: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Merge outputs from parallel agent instances.

        Args:
            outputs: List of output dictionaries from Alpha, Beta, Gamma instances.
            **kwargs: Additional parameters (e.g., llm_client for LLM-based merges).

        Returns:
            Aggregated output dictionary.

        Raises:
            NotImplementedError: Subclasses must implement this method.
            ValueError: If fewer than 2 outputs are provided.
        """
        raise NotImplementedError

    @abstractmethod
    def check_divergence(
        self,
        outputs: list[dict[str, Any]],
        threshold: float = 30.0,
    ) -> dict[str, Any] | None:
        """Check for significant divergence between parallel outputs.

        Args:
            outputs: List of output dictionaries from parallel instances.
            threshold: Maximum allowable score difference (percentage points).

        Returns:
            Divergence warning dictionary if threshold exceeded, else None.
        """
        raise NotImplementedError
