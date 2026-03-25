"""
SA Agent Node — Scoring Agent for architectural evaluation.

Implements: FR-SA-001–012. Evaluates diagrams on 4 pillars.
"""

from typing import Any
from core.interfaces.base_agent import BaseAgent


class SAAgentNode(BaseAgent):
    """LangGraph node for the Scoring Agent.

    4-Pillar evaluation (FR-SA-003):
    1. Syntax Health (20%): Rendering validation via PlantUML server.
    2. Traceability (20%): REQ-ID comment audit.
    3. Structural Fidelity (30%): Entity/edge parity vs TOON IR.
    4. SAAM/ATAM Alignment (30%): Quality attribute scenario analysis.

    In Workflow 3: Uses median-based scoring across parallel instances (FR-SA-011).
    """

    def __init__(self, llm_instance_name: str | None = None) -> None:
        super().__init__(agent_name="sa", llm_instance_name=llm_instance_name)

    def invoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute 4-pillar architectural evaluation.

        Reads: state['aga_plantuml_code'], state['aga_rendered_svg'],
               state['raa_toon_ir'], state['arlo_toon_payload'] (if ARLO enabled)
        Writes: state['sa_evaluation']

        Args:
            state: LangGraph pipeline state.

        Returns:
            Updated state with SA evaluation (SAEvaluation schema).
        """
        raise NotImplementedError

    def validate_output(self, output: Any) -> bool:
        """Validate output matches SAEvaluation schema.

        Args:
            output: Raw SA output.

        Returns:
            True if valid.
        """
        raise NotImplementedError

    def _evaluate_syntax_health(self, puml_code: str) -> float:
        """Pillar 1: Submit to PlantUML server and check response (FR-SA-004).

        Returns:
            Score 0–100.
        """
        raise NotImplementedError

    def _evaluate_traceability(self, puml_code: str, requirements: list[dict]) -> float:
        """Pillar 2: Count REQ-ID comments and compare against requirement list (FR-SA-005).

        Returns:
            Score 0–100.
        """
        raise NotImplementedError

    def _evaluate_structural_fidelity(self, puml_code: str, toon_ir: dict) -> float:
        """Pillar 3: Compare entities/edges in diagram vs TOON IR (FR-SA-006).

        Returns:
            Score 0–100.
        """
        raise NotImplementedError

    def _evaluate_saam_alignment(self, puml_code: str, arlo_decisions: dict | None) -> float:
        """Pillar 4: LLM-based SAAM/ATAM quality attribute scenario analysis (FR-SA-007).

        Returns:
            Score 0–100.
        """
        raise NotImplementedError
