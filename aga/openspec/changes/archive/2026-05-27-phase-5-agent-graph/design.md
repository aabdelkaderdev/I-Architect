## Context

We have completed the implementation of the `AGAState` schemas, various node processors (like `server_guard` and `input_parsing`), and custom tools for PlantUML encoding and fetching. Now, we need to orchestrate these components into a seamless processing loop. This requires an agentic mechanism capable of self-correcting diagram generation errors and an overarching state graph that defines the complete pipeline lifecycle.

As of LangChain v1, the recommended way to build agents is `create_agent` from `langchain.agents`, which replaces the deprecated `langgraph.prebuilt.create_react_agent`. The new API uses middleware for customization (pre/post model hooks, tool error handling), `system_prompt` instead of `prompt`, and the `Runtime` object for dependency injection instead of `config["configurable"]`.

## Goals / Non-Goals

**Goals:**
- Assemble the `aga_graph.py` StateGraph to coordinate the complete diagram generation workflow.
- Implement an agent node using `create_agent` (from `langchain.agents`) that generates, encodes, fetches, and validates diagram code iteratively until successful or exhausted.
- Properly handle different types of failures (e.g., Syntax errors, server unavailability, HTTP errors) using agent middleware.
- Persist state via checkpoints using `SqliteSaver` from `langgraph-checkpoint-sqlite`.

**Non-Goals:**
- Modifying previously built nodes (`server_guard`, `input_parsing`) beyond ensuring they fit the graph.
- Building the frontend orchestrator or complex multi-agent architectures beyond this single agent loop.

## Decisions

1. **StateGraph framework**: We will use LangGraph's `StateGraph` because it integrates natively with LangChain agents and offers robust state management between discrete nodes. StateGraph remains the core primitive in LangGraph for defining custom graph topologies.

2. **Agent creation via `create_agent`**: We will use `langchain.agents.create_agent` (LangChain v1) instead of the deprecated `langgraph.prebuilt.create_react_agent`. Key differences:
   - Import: `from langchain.agents import create_agent` (not `from langgraph.prebuilt`)
   - Prompt: uses `system_prompt=` parameter (not `prompt=`)
   - Customization: uses middleware classes (`AgentMiddleware` subclasses) instead of `pre_model_hook`/`post_model_hook`
   - State: `TypedDict` only (Pydantic BaseModel no longer supported for `create_agent` state)
   - Streaming node name: `"model"` (not `"agent"`)

3. **Middleware for error handling**: We will implement a custom `AgentMiddleware` subclass with `wrap_tool_call` to intercept tool errors and `after_model` for output validation. This replaces the old hook-based pattern.

4. **Checkpointing**: We will use `SqliteSaver` from the separate `langgraph-checkpoint-sqlite` package. The checkpointer is passed to `graph.compile(checkpointer=...)`. Thread IDs are provided via `config={"configurable": {"thread_id": "..."}}` at invocation time.

5. **Runtime context injection**: The LLM and other runtime dependencies will be injected via the `context` argument and `Runtime` object (from `langgraph.runtime`), not via `config["configurable"]`. Node functions accept `runtime: Runtime[Context]` as a parameter. For tools, use `ToolRuntime` from `langchain.tools`.

6. **Error handling categorization**: We will classify errors and implement specific retry logic. Immediate halts for fatal errors (server down), iterative retries for generation errors (up to 5 limits).

## Risks / Trade-offs

- **Risk: Agent infinite loops** → Mitigation: Use middleware with a `state_schema` that tracks call count, and return `{"jump_to": "end"}` from `before_model` when the limit is reached.
- **Risk: Concurrency issues with SqliteSaver** → Mitigation: SqliteSaver is recommended for experimentation and local workflows. For production, consider `PostgresSaver` from `langgraph-checkpoint-postgres`.
- **Risk: Large state object** → Mitigation: Checkpointing occurs at super-step boundaries (per node completion) which is built into LangGraph. We structure the graph so that each diagram completion is a separate super-step.
- **Risk: API version mismatch** → Mitigation: Pin `langchain>=1.0` and `langgraph-checkpoint-sqlite` in dependencies to avoid using deprecated APIs.
