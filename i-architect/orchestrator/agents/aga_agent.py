"""
AGA Agent Node — Architecture Generation Agent.

Implements: FR-AGA-001–013. Translates TOON IR to PlantUML code.
Has a self-correction loop with the PlantUML server.
"""

from typing import Any
from core.interfaces.base_agent import BaseAgent


class AGAAgentNode(BaseAgent):
    """LangGraph node for the Architecture Generation Agent.

    Operates with the strict 'Translator' persona (FR-AGA-002): Only
    translates TOON IR to C4/UML diagrams. Must never invent entities.

    Self-correction loop (FR-AGA-009):
    1. Generate PlantUML code
    2. Render via PlantUML server
    3. If syntax error → parse error → regenerate (max 3 retries)
    """

    MAX_RETRIES = 3

    def __init__(self, llm_instance_name: str | None = None) -> None:
        super().__init__(agent_name="aga", llm_instance_name=llm_instance_name)

    def invoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute AGA: generate diagram code, render, self-correct.

        Reads: state['raa_toon_ir'], state['arlo_toon_payload'] (optional)
        Writes: state['aga_plantuml_code'], state['aga_rendered_svg'],
                state['aga_correction_history']

        Args:
            state: LangGraph pipeline state.

        Returns:
            Updated state with AGA artifacts.
        """
        raise NotImplementedError

    def validate_output(self, output: Any) -> bool:
        """Validate AGA produces renderable PlantUML code.

        Args:
            output: Generated PlantUML code string.

        Returns:
            True if renderable (200 from PlantUML server).
        """
        raise NotImplementedError

    def _inject_traceability_comments(self, puml_code: str, toon_ir: dict) -> str:
        """Inject requirement ID comments into PlantUML source (FR-AGA-005).

        Pattern: ' REQ-<hash>-<id> above each entity definition.

        Args:
            puml_code: Raw PlantUML code.
            toon_ir: TOON IR with entity-requirement mappings.

        Returns:
            Annotated PlantUML code.
        """
        raise NotImplementedError

    def _self_correction_loop(self, puml_code: str, error_message: str, attempt: int) -> str:
        """Self-correction: feed syntax error to LLM for fix (FR-AGA-009).

        Args:
            puml_code: Previous code that failed rendering.
            error_message: PlantUML server error message.
            attempt: Current retry count.

        Returns:
            Corrected PlantUML code.
        """
        raise NotImplementedError
