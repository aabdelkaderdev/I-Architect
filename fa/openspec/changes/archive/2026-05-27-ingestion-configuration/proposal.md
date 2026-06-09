# Proposal: Ingestion Configuration Dataclasses (Phase 2)

## What
Implement two configuration dataclasses — `IngestionConfig` and `FilterConfig` — that
control every tunable behaviour in the ingestion pipeline. These live as state channels
in the LangGraph `IngestionState` TypedDict so that every node (extractors, normaliser,
RFA) can read them from state without hardcoding defaults.

## Why
1. **Auditable & testable** — all tunables are explicit and inspectable.
2. **No hidden globals** — configuration flows one-way through LangGraph state channels;
   no node creates, modifies, or reaches around state to find configuration.
3. **User-configurable without code changes** — the orchestrator deserialises user
   config (or applies defaults), injects it into the graph invocation, and every node
   reads from the state dict.

## LangGraph alignment
Per the current LangGraph docs the pipeline state is a `TypedDict`
(`IngestionState`), while the LLM instance lives in a `@dataclass` runtime context
(`IngestionContext`) accessed via `Runtime[IngestionContext]` in node signatures.

Configuration fields belong in the **state** (serialisable TypedDict), not in the
runtime context, because:
- State must remain serialisable — dataclasses used as `context_schema` are for
  non-serialisable dependencies (DB connections, LLM instances).
- Config values are plain primitives (`str`, `int`, `float`, `bool`) and should be
  checkpointable.

The existing `IngestionContext` dataclass (holding `llm: BaseChatModel`) is passed via
`StateGraph(IngestionState, context_schema=IngestionContext)` and accessed in nodes as
`runtime.context.llm`. This remains unchanged.
