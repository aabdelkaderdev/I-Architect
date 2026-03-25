<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/context_editing -->

Modulev1.2.13 (latest)●Since v1.0

# context\_editing

Context editing middleware.

Mirrors Anthropic's context editing capabilities by clearing older tool results once the
conversation grows beyond a configurable token threshold.

The implementation is intentionally model-agnostic so it can be used with any LangChain
chat model.

## Attributes

[attribute

ResponseT](/python/langchain/agents/middleware/context_editing/ResponseT)[attribute

DEFAULT\_TOOL\_PLACEHOLDER: str](/python/langchain/agents/middleware/context_editing/DEFAULT_TOOL_PLACEHOLDER)[attribute

TokenCounter: Callable[[Sequence[BaseMessage]], int]](/python/langchain/agents/middleware/context_editing/TokenCounter)

## Classes

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/context_editing/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/context_editing/AgentState)[class

ModelRequest

Model request information for the agent.](/python/langchain/agents/middleware/context_editing/ModelRequest)[class

ModelResponse

Response from model execution including messages and optional structured output.

The result will usually contain a single `AIMessage`, but may include an additional
`ToolMessage` if the model used a tool for structured output.](/python/langchain/agents/middleware/context_editing/ModelResponse)[class

ContextEdit

Protocol describing a context editing strategy.](/python/langchain/agents/middleware/context_editing/ContextEdit)[class

ClearToolUsesEdit

Configuration for clearing tool outputs when token limits are exceeded.](/python/langchain/agents/middleware/context_editing/ClearToolUsesEdit)[class

ContextEditingMiddleware

Automatically prune tool results to manage context size.

The middleware applies a sequence of edits when the total input token count exceeds
configured thresholds.

Currently the `ClearToolUsesEdit` strategy is supported, aligning with Anthropic's
`clear_tool_uses_20250919` behavior [(read more)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool).](/python/langchain/agents/middleware/context_editing/ContextEditingMiddleware)


