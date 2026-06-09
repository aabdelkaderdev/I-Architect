"""Non-ASR Subgraph node — proposes entities from functional requirements.

Processing responsibility (Phase 1 §8.3): propose entities implied by functional
requirements — user types, external systems, feature-bearing services — absent from
the ASR-driven proposals. These proposals fill coverage gaps.

LLM resolved from config["configurable"]["non_asr_llm"] per FG-Phase-10 §3.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from raa.utils.rendering import render_system_user
from raa.validators import validate_entity_proposal

if TYPE_CHECKING:
    from langgraph.types import RunnableConfig

    from raa.types import BatchInput, EntityProposal

logger = logging.getLogger(__name__)

NON_ASR_SYSTEM_TEMPLATE = "non_asr_subgraph_system.md"
NON_ASR_USER_TEMPLATE = "non_asr_subgraph_user.md"


class NonASRSubgraph:
    """Proposes entities implied by functional requirements — user types, external
    systems, feature-bearing services. Does not reference quality attributes or
    architectural decisions — those are the ASR Subgraph's domain."""

    def assemble_prompt(self, batch: BatchInput) -> tuple[str, str]:
        """Pre:
            - batch.non_asrs is the functional requirement set assigned to this batch.
            - batch.registry_snapshot is read-only.

        Post:
            - Returns (system_prompt, user_prompt) rendered from Non-ASR templates
              and the naming partial. Prompt content excludes QA-weighted reasoning
              and ARLO decisions.

        Side effects: Reads prompt template files from raa/prompts/.
        """
        variables: dict = {
            "non_asrs": batch.get("non_asrs", []),
            "registry_snapshot": batch.get("registry_snapshot", {}),
        }
        return render_system_user(NON_ASR_SYSTEM_TEMPLATE, NON_ASR_USER_TEMPLATE, variables)

    async def invoke_llm(
        self,
        prompt: tuple[str, str],
        config: RunnableConfig,
    ) -> object:
        """Pre:
            - config["configurable"]["non_asr_llm"] exists per FG-Phase-10 §1.

        Post:
            - Returns the raw structured-output response object from the Non-ASR LLM.

        Side effects: Calls the configured Non-ASR LLM.
        """
        from langchain_core.messages import HumanMessage, SystemMessage

        from raa.schemas.structured_output import EntityProposalListOutput

        llm = config["configurable"]["non_asr_llm"]

        model = llm.with_structured_output(EntityProposalListOutput)

        messages = [
            SystemMessage(content=prompt[0]),
            HumanMessage(content=prompt[1]),
        ]
        return await model.ainvoke(messages)

    def parse_response(
        self,
        response: object,
        batch: BatchInput,
    ) -> list[EntityProposal]:
        """Pre:
            - `response` is the raw Non-ASR LLM structured response.

        Post:
            - Returns validated EntityProposal records.
            - Every returned proposal has proposing_subgraph == "non_asr".
            - Empty source_requirements, invalid names, and invalid C4 suffixes
              are rejected per validate_entity_proposal().

        Side effects: Logs rejected proposals and validation reasons.
        """
        from raa.schemas.structured_output import dump_structured_response
        from raa.utils.naming import normalize_name

        response = dump_structured_response(response)
        if isinstance(response, dict) and "proposals" in response:
            response = response["proposals"]

        if not isinstance(response, list):
            logger.warning(
                "Non-ASR Subgraph response is not a list (batch %s). Got %s. Returning empty.",
                batch["batch_id"],
                type(response).__name__,
            )
            return []

        valid_proposals: list[EntityProposal] = []
        for i, raw in enumerate(response):
            try:
                raw = dump_structured_response(raw)
                if not isinstance(raw, dict):
                    raise TypeError(f"proposal must be a dict, got {type(raw).__name__}")

                proposal: EntityProposal = {
                    "proposed_name": str(raw.get("proposed_name", "")),
                    "c4_level": raw.get("c4_level", "container"),
                    "c4_type": raw.get("c4_type", "service"),
                    "description": str(raw.get("description", "")),
                    "responsibilities": [
                        str(r) for r in raw.get("responsibilities", [])
                    ],
                    "source_requirements": [
                        str(r) for r in raw.get("source_requirements", [])
                    ],
                    "proposing_subgraph": "non_asr",
                    "justification": str(raw.get("justification", "")),
                }
                # Non-ASR subgraph never sets concern_technology

                try:
                    proposal["proposed_name"] = normalize_name(
                        proposal["proposed_name"], proposal["c4_type"]
                    )
                except ValueError:
                    pass

                validate_entity_proposal(proposal)
                valid_proposals.append(proposal)

            except (ValueError, TypeError, KeyError) as exc:
                logger.warning(
                    "Non-ASR proposal %d rejected in batch %s: %s",
                    i,
                    batch["batch_id"],
                    exc,
                )

        return valid_proposals

    async def build_proposals(
        self,
        batch: BatchInput,
        config: RunnableConfig,
    ) -> list[EntityProposal]:
        """Pre:
            - `batch` is ready for Non-ASR processing.

        Post:
            - Returns Non-ASR-derived proposals for the Judge.
            - Returns an empty list when batch.non_asrs is empty.

        Side effects:
            - Loads prompts, invokes the Non-ASR LLM, validates output, and logs metrics.
            - Does not write to the registry.
        """
        if not batch.get("non_asrs"):
            logger.info(
                "Non-ASR batch %s has no non-ASRs; returning empty proposals.",
                batch["batch_id"],
            )
            return []

        prompt = self.assemble_prompt(batch)
        response = await self.invoke_llm(prompt, config)
        return self.parse_response(response, batch)
