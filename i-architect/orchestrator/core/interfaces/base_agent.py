"""
BaseAgent — Abstract Base Class for all LangGraph agent nodes.

Every agent in the I-Architect pipeline (FilteringAgent, ARLO, RAA, AGA, SA,
MCP Aggregator) MUST inherit from this class and implement the `invoke` and
`validate_output` methods.

Design Pattern: Template Method — `run()` orchestrates the sequence of
pre-processing, invocation, validation, and post-processing.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Abstract base class for all LangGraph pipeline agent nodes.

    Attributes:
        agent_name: Unique identifier for this agent (e.g., "raa", "aga").
        llm_instance_name: Name of the LLM instance assigned to this agent.
    """

    def __init__(self, agent_name: str, llm_instance_name: str | None = None) -> None:
        """Initialize the base agent.

        Args:
            agent_name: Unique identifier for this agent.
            llm_instance_name: Optional LLM instance name for parallel workflows.
        """
        self.agent_name = agent_name
        self.llm_instance_name = llm_instance_name

    @abstractmethod
    def invoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute the agent's core logic on the pipeline state.

        This is the primary entry point called by the LangGraph node.

        Args:
            state: The current LangGraph pipeline state dictionary.

        Returns:
            Updated state dictionary with this agent's outputs.

        Raises:
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_output(self, output: Any) -> bool:
        """Validate the agent's output against its expected schema.

        Args:
            output: The raw output produced by this agent.

        Returns:
            True if the output is valid, False otherwise.

        Raises:
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError

    def check_cancellation(self, state: dict[str, Any]) -> bool:
        """Check whether the pipeline run has been cancelled.

        Reads the cancellation token from the state. Every agent node
        SHOULD call this at the start of each execution cycle (FR-TASK-008).

        Args:
            state: The current LangGraph pipeline state dictionary.

        Returns:
            True if the run has been cancelled, False otherwise.
        """
        raise NotImplementedError

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        """Template method orchestrating the agent execution lifecycle.

        Sequence: check cancellation → pre-process → invoke → validate → post-process.

        Args:
            state: The current LangGraph pipeline state dictionary.

        Returns:
            Updated state dictionary.
        """
        raise NotImplementedError
