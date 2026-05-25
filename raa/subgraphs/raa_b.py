"""
RAA-B subgraph builder — Pattern-driven architectural fragment extraction.

Returns an uncompiled StateGraph. The caller is responsible for
compilation with the appropriate SQLite checkpointer.
"""
from __future__ import annotations

import logging

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph

from raa.state.models import ArchFragment
from raa.subgraphs.schemas import StrategySubgraphState
from raa.utils.c4_validator import enforce_fragment_hierarchy
from raa.utils.prompt_loader import load_prompt

logger = logging.getLogger(__name__)

_PROMPT_TEMPLATE = "pattern_matching.md"


def build_raa_b_subgraph() -> StateGraph:
    """Build an uncompiled RAA-B subgraph (pattern-driven strategy)."""
    builder = StateGraph(StrategySubgraphState)

    def extract_patterns(state: StrategySubgraphState, config: RunnableConfig) -> dict:
        configurable = config.get("configurable", {})
        llm = configurable.get("raa_b_llm")
        batch = state["batch"]
        running_model = state.get("running_model", {})

        prompt = load_prompt(_PROMPT_TEMPLATE, {
            "batch_id": batch.get("group_id", ""),
            "reduced_confidence": str(state.get("reduced_confidence", False)),
            "running_model": str(running_model),
            "requirements": str(batch.get("asr_records", []) + batch.get("non_asr_records", [])),
            "bridge_requirements": str(state.get("bridge_requirements", [])),
            "quality_weights": str(state.get("quality_weights", {})),
        })

        fragment = _extract_fragment(llm, prompt)
        cleaned, questions = enforce_fragment_hierarchy(
            fragment,
            running_model,
            batch_id=batch.get("group_id", ""),
            strategy="raa_b",
        )
        return {"arch_fragment": cleaned, "open_questions": questions}

    builder.add_node("extract_patterns", extract_patterns)
    builder.add_edge(START, "extract_patterns")
    builder.add_edge("extract_patterns", END)

    return builder


def _extract_fragment(llm, prompt: str) -> ArchFragment:
    """Run structured extraction or return a minimal fragment when no LLM is configured."""
    if llm is None:
        logger.warning("No raa_b_llm configured — returning empty ArchFragment")
        return ArchFragment(metadata={"strategy": "raa_b", "note": "no LLM configured"})

    try:
        structured = llm.with_structured_output(ArchFragment, include_raw=True)
        response = structured.invoke(prompt)
    except Exception:
        logger.exception("Structured extraction failed for RAA-B")
        return ArchFragment(metadata={"strategy": "raa_b", "error": "extraction_failed"})

    if isinstance(response, ArchFragment):
        return response

    if isinstance(response, dict):
        if response.get("parsing_error"):
            logger.warning("RAA-B parsing error: %s", response["parsing_error"])
        parsed = response.get("parsed")
        if isinstance(parsed, ArchFragment):
            return parsed

    logger.warning("RAA-B extraction returned unexpected type: %s", type(response))
    return ArchFragment(metadata={"strategy": "raa_b", "error": "malformed_response"})
