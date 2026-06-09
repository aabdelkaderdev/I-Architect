"""LangSmith Studio entrypoint for the RAA internal graph.

This module is intentionally separate from ``raa.graph`` so Studio can create
runtime LLM instances from environment variables instead of requiring callers to
pass Python objects through ``config["configurable"]``.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy, RunnableConfig, TimeoutPolicy

from raa.config.defaults import (
    NODE_RUN_TIMEOUT,
    RETRY_BACKOFF_FACTOR,
    RETRY_INITIAL_INTERVAL,
    RETRY_JITTER,
    RETRY_MAX_ATTEMPTS,
    RETRY_MAX_INTERVAL,
    THREAD_ID,
)
from raa.graph import (
    _assemble_output,
    _asr_node,
    _judge_node,
    _next_batch,
    _non_asr_node,
    _route_after_judge,
    _route_after_next_batch,
    _snapshot_registry,
)
from raa.state import RAAState


@lru_cache(maxsize=1)
def _studio_llm() -> ChatAnthropic:
    """Create the chat model used by Studio runs."""
    return ChatAnthropic(
        model=os.getenv("RAA_MODEL", "deepseek-v4-flash"),
        temperature=float(os.getenv("RAA_TEMPERATURE", "0.0")),
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url=os.getenv("RAA_BASE_URL", "https://api.deepseek.com/anthropic"),
        model_kwargs={"thinking": {"type": "disabled"}},
    )


def _studio_config(config: RunnableConfig | None) -> RunnableConfig:
    """Inject RAA's non-JSON runtime config for local Studio runs."""
    cfg: dict[str, Any] = dict(config or {})
    configurable = dict(cfg.get("configurable", {}))
    llm = _studio_llm()

    configurable.setdefault("asr_llm", llm)
    configurable.setdefault("non_asr_llm", llm)
    configurable.setdefault("judge_llm", llm)
    configurable.setdefault("thread_id", os.getenv("RAA_THREAD_ID", THREAD_ID))
    configurable.setdefault("db_path", os.getenv("RAA_DB_PATH", "./checkpoints/raa_studio.db"))

    cfg["configurable"] = configurable
    return cfg


async def _studio_asr_node(state: dict, config: RunnableConfig) -> dict:
    return await _asr_node(state, _studio_config(config))


async def _studio_non_asr_node(state: dict, config: RunnableConfig) -> dict:
    return await _non_asr_node(state, _studio_config(config))


async def _studio_judge_node(state: dict, config: RunnableConfig) -> dict:
    return await _judge_node(state, _studio_config(config))


async def _studio_assemble_output(state: dict, config: RunnableConfig) -> dict:
    return await _assemble_output(state, _studio_config(config))


def build_studio_graph():
    """Build the RAA graph for LangGraph Agent Server / LangSmith Studio."""
    graph = StateGraph(RAAState)

    retry_policy = RetryPolicy(
        max_attempts=RETRY_MAX_ATTEMPTS,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        initial_interval=RETRY_INITIAL_INTERVAL,
        max_interval=RETRY_MAX_INTERVAL,
        jitter=RETRY_JITTER,
    )
    timeout_policy = TimeoutPolicy(run_timeout=NODE_RUN_TIMEOUT)

    graph.add_node("snapshot_registry", _snapshot_registry)
    graph.add_node(
        "asr_node",
        _studio_asr_node,
        retry_policy=retry_policy,
        timeout=timeout_policy,
    )
    graph.add_node(
        "non_asr_node",
        _studio_non_asr_node,
        retry_policy=retry_policy,
        timeout=timeout_policy,
    )
    graph.add_node(
        "judge_node",
        _studio_judge_node,
        retry_policy=retry_policy,
        timeout=timeout_policy,
    )
    graph.add_node("next_batch", _next_batch)
    graph.add_node("assemble_output", _studio_assemble_output)

    graph.add_edge(START, "snapshot_registry")
    graph.add_edge("snapshot_registry", "asr_node")
    graph.add_edge("snapshot_registry", "non_asr_node")
    graph.add_edge("asr_node", "judge_node")
    graph.add_edge("non_asr_node", "judge_node")
    graph.add_conditional_edges(
        "judge_node",
        _route_after_judge,
        {
            "next_batch": "next_batch",
            "assemble": "assemble_output",
        },
    )
    graph.add_conditional_edges(
        "next_batch",
        _route_after_next_batch,
        {
            "snapshot": "snapshot_registry",
            "assemble": "assemble_output",
        },
    )
    graph.add_edge("assemble_output", END)

    return graph.compile()


app = build_studio_graph()
