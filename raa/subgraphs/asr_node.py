"""ASR Subgraph node — proposes entities from architecturally significant requirements.

Processing responsibility (Phase 1 §8.2): propose entities directly implied by quality
attributes and concern-level architectural decisions. These proposals are high-confidence
and architecturally load-bearing — they define the structural core of the C4 diagrams.

LLM resolved from config["configurable"]["asr_llm"] per FG-Phase-10 §3.
with_structured_output is called inside the node body, not at injection time.
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

ASR_SYSTEM_TEMPLATE = "asr_subgraph_system.md"
ASR_USER_TEMPLATE = "asr_subgraph_user.md"


class ASRSubgraph:
    """Proposes entities directly implied by quality attributes and architectural decisions."""

    def assemble_prompt(self, batch: BatchInput) -> tuple[str, str]:
        """Pre:
            - `batch` is the current ConcernBatchInput or FoundationBatchInput.
            - `batch.registry_snapshot` is read-only.

        Post:
            - Returns (system_prompt, user_prompt) rendered from ASR templates and
              the naming partial. Concern batches include ASRs, quality weights,
              decisions, condition, and registry snapshot. Foundation batches omit
              concern-only fields.

        Side effects: Reads prompt template files from raa/prompts/.
        """
        # Pre-join quality_attributes for Mustache (Chevron has no -last support)
        asr_entries = []
        for asr in batch.get("asrs", []):
            qa_list = asr.get("quality_attributes", [])
            asr_entries.append({
                "id": asr.get("id", ""),
                "text": asr.get("text", ""),
                "quality_attributes_joined": ", ".join(qa_list) if qa_list else "",
            })

        variables: dict = {
            "quality_weights": [
                {"@key": k, ".": v} for k, v in batch.get("quality_weights", {}).items()
            ],
            "asrs": asr_entries,
            "registry_snapshot": batch.get("registry_snapshot", {}),
        }

        if batch["batch_type"] == "concern":
            variables["condition"] = batch.get("condition", "")
            variables["decisions"] = batch.get("decisions", [])

        return render_system_user(ASR_SYSTEM_TEMPLATE, ASR_USER_TEMPLATE, variables)

    async def invoke_llm(
        self,
        prompt: tuple[str, str],
        config: RunnableConfig,
    ) -> object:
        """Pre:
            - `prompt` is the rendered system/user prompt pair.
            - config["configurable"]["asr_llm"] exists per FG-Phase-10 §1.

        Post:
            - Returns the raw structured-output response object from the ASR LLM.
            - The response is not trusted until parse_response() validates it.

        Side effects: Calls the configured ASR LLM.
        """
        from langchain_core.messages import HumanMessage, SystemMessage

        from raa.schemas.structured_output import EntityProposalListOutput

        llm = config["configurable"]["asr_llm"]

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
            - `response` is the raw ASR LLM structured response.
            - batch.batch_id is available for traceability logging.

        Post:
            - Returns validated EntityProposal records.
            - Every returned proposal has proposing_subgraph == "asr".
            - Proposals violating validate_entity_proposal() are rejected
              (reject-and-continue policy).

        Side effects: Logs rejected proposals and validation reasons.
        """
        from raa.schemas.structured_output import dump_structured_response
        from raa.utils.naming import normalize_name

        response = dump_structured_response(response)
        if isinstance(response, dict) and "proposals" in response:
            response = response["proposals"]

        if not isinstance(response, list):
            logger.warning(
                "ASR Subgraph response is not a list (batch %s). Got %s. Returning empty.",
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

                # Enforce proposing_subgraph
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
                    "proposing_subgraph": "asr",
                    "justification": str(raw.get("justification", "")),
                }

                # Concern technology is optional
                if "concern_technology" in raw and raw["concern_technology"]:
                    proposal["concern_technology"] = str(raw["concern_technology"])

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
                    "ASR proposal %d rejected in batch %s: %s",
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
            - `batch` is ready for ASR processing.
            - config satisfies RAAConfigSchema (FG-Phase-10 §1).

        Post:
            - Returns ASR-derived entity proposals for the Judge.
            - Returns an empty list when no ASRs exist in the batch.

        Side effects:
            - Loads prompts, invokes the ASR LLM, validates output, and logs metrics.
            - Does not write to the registry.
        """
        if not batch.get("asrs"):
            logger.info("ASR batch %s has no ASRs; returning empty proposals.", batch["batch_id"])
            return []

        prompt = self.assemble_prompt(batch)
        response = await self.invoke_llm(prompt, config)
        return self.parse_response(response, batch)
