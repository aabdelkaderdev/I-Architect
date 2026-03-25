"""
Strategy Factory — Creates extraction strategy instances.

Factory Pattern for selecting the appropriate extraction strategy
based on user selection or auto-correction logic.
"""

from core.interfaces.base_extraction_strategy import BaseExtractionStrategy


class ExtractionStrategyFactory:
    """Factory for creating extraction strategy instances."""

    _strategies: dict[str, type] = {}

    @classmethod
    def register(cls, name: str, strategy_class: type) -> None:
        """Register a strategy class with a name.

        Args:
            name: Strategy name (e.g., "Line-by-Line").
            strategy_class: The strategy class to register.
        """
        cls._strategies[name.lower()] = strategy_class

    @classmethod
    def create(cls, strategy_name: str, **kwargs) -> BaseExtractionStrategy:
        """Create and return an extraction strategy instance.

        Args:
            strategy_name: Name of the strategy to create.
            **kwargs: Additional creation parameters.

        Returns:
            Configured BaseExtractionStrategy instance.

        Raises:
            ValueError: If the strategy name is not registered.
        """
        raise NotImplementedError

    @classmethod
    def get_auto_correction_target(cls, current_strategy: str) -> str:
        """Determine the escalation target for auto-correction (FR-ING-014).

        Escalation path: Line-by-Line → Regex → Grammar-Based → Hybrid.

        Args:
            current_strategy: Name of the currently failing strategy.

        Returns:
            Name of the strategy to escalate to.
        """
        raise NotImplementedError
