"""Shared invoke_llm helper — used by all three LLM-calling nodes.

Per FG-Phase-41 §4: resolves LLM from config["configurable"], binds structured output,
renders Mustache prompts, invokes, and returns the Pydantic-validated response.

Error contract: provider errors (HTTP 5xx, rate limits) are caught by LangGraph's
retry_policy on the calling node. NodeTimeoutError fires at 120s. Deterministic
errors (ValueError, TypeError) are not retried.
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Literal

from langchain_core.messages import HumanMessage, SystemMessage

if TYPE_CHECKING:
    from langgraph.types import RunnableConfig
    from pydantic import BaseModel

logger = logging.getLogger(__name__)


async def invoke_llm(
    config: RunnableConfig,
    llm_key: Literal["asr_llm", "non_asr_llm", "judge_llm"],
    output_model: type[BaseModel],
    system_template: str,
    user_template: str,
    template_vars: dict,
    *,
    thread_id: str = "",
    batch_id: str = "",
    role: str = "",
    step: str | None = None,
    attempt: int = 1,
) -> BaseModel:
    """Shared LLM invocation pattern per FG-Phase-41 §4.

    Args:
        config: RunnableConfig with configurable LLM instances.
        llm_key: Which configurable key to resolve ("asr_llm", "non_asr_llm", "judge_llm").
        output_model: Pydantic model for with_structured_output binding.
        system_template: Mustache template name for the system prompt.
        user_template: Mustache template name for the user prompt.
        template_vars: Variables rendered into both templates.
        thread_id: Correlation ID for logging.
        batch_id: Current batch ID for logging.
        role: "asr", "non_asr", or "judge" for observability.
        step: SAAM step name for Judge calls (e.g. "classify", "evaluate", "interact").
        attempt: Current retry attempt number.

    Returns:
        Pydantic-validated structured response.

    Raises:
        Provider errors bubble to LangGraph retry_policy.
        Deterministic errors (ValueError, TypeError) are not retried.
    """
    from raa.utils.rendering import render_system_user

    # 1. Resolve LLM from configurable
    llm = config["configurable"][llm_key]

    # 2. Bind structured output
    structured_llm = llm.with_structured_output(output_model)

    # 3. Render prompts
    system_prompt, user_prompt = render_system_user(
        system_template, user_template, template_vars,
    )

    # 4. Invoke
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    start = time.monotonic()
    try:
        response = await structured_llm.ainvoke(messages)
        elapsed_ms = (time.monotonic() - start) * 1000

        # Collect token counts if available
        input_tokens = _extract_tokens(response, "input")
        output_tokens = _extract_tokens(response, "output")

        logger.info(
            "LLM call complete",
            extra={
                "thread_id": thread_id,
                "batch_id": batch_id,
                "role": role,
                "step": step,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "latency_ms": round(elapsed_ms, 1),
                "status": "success",
                "attempt": attempt,
            },
        )
        return response

    except Exception:
        elapsed_ms = (time.monotonic() - start) * 1000
        logger.warning(
            "LLM call failed",
            extra={
                "thread_id": thread_id,
                "batch_id": batch_id,
                "role": role,
                "step": step,
                "latency_ms": round(elapsed_ms, 1),
                "status": "retrying" if attempt > 1 else "failed",
                "attempt": attempt,
            },
        )
        raise


def _extract_tokens(response: object, kind: str) -> int:
    """Best-effort extraction of token counts from the LLM response metadata."""
    try:
        if hasattr(response, "response_metadata"):
            meta = response.response_metadata
            if kind == "input":
                return meta.get("token_usage", {}).get("prompt_tokens", 0)
            return meta.get("token_usage", {}).get("completion_tokens", 0)
    except Exception:
        pass
    return 0
