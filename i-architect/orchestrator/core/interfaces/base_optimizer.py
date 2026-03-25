"""
BaseOptimizer — Abstract Base Class for ARLO optimization strategies.

Implements the Strategy Pattern for ARLO's mathematical optimization layer.
Concrete strategies: ILP (OR-Tools) and Greedy (FR-ARLO-015, FR-ARLO-016).
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseOptimizer(ABC):
    """Abstract interface for ARLO optimization strategies.

    Both ILP and Greedy optimizers implement this interface, allowing
    runtime strategy selection via the UI (FR-ARLO-017).
    """

    @property
    @abstractmethod
    def strategy_name(self) -> str:
        """Return the name of this optimization strategy.

        Returns:
            Strategy name string (e.g., "ILP", "Greedy").
        """
        ...

    @abstractmethod
    def optimize(
        self,
        matrix: dict[str, dict[str, int]],
        weights: dict[str, float],
        row_groups: dict[str, str],
        timeout_seconds: int = 120,
    ) -> list[dict[str, Any]]:
        """Run the optimization algorithm on the quality-architecture matrix.

        Args:
            matrix: Pattern → QA → score mapping (from quality_archipattern_matrix.csv).
            weights: QA → weight mapping (inferred from requirement frequency).
            row_groups: Pattern → category group mapping (mutually exclusive).
            timeout_seconds: Maximum wall-clock time before aborting (ILP only).

        Returns:
            List of Decision dictionaries, one per architectural category,
            each containing selected_pattern, score, satisfied_qas, trade_offs.

        Raises:
            NotImplementedError: Subclasses must implement this method.
            TimeoutError: If the solver exceeds the timeout (ILP).
        """
        raise NotImplementedError
