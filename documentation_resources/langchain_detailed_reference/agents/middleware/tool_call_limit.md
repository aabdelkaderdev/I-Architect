<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/tool_call_limit -->

Modulev1.2.13 (latest)●Since v1.0

# tool\_call\_limit

Tool call limit middleware for agents.

## Attributes

[attribute

PrivateStateAttr

Annotation used to mark state attributes as purely internal for a given middleware.](/python/langchain/agents/middleware/tool_call_limit/PrivateStateAttr)[attribute

ResponseT](/python/langchain/agents/middleware/tool_call_limit/ResponseT)[attribute

ExitBehavior: Literal['continue', 'error', 'end']

How to handle execution when tool call limits are exceeded.

- `'continue'`: Block exceeded tools with error messages, let other tools continue
  (default)
- `'error'`: Raise a `ToolCallLimitExceededError` exception
- `'end'`: Stop execution immediately, injecting a `ToolMessage` and an `AIMessage` for
  the single tool call that exceeded the limit. Raises `NotImplementedError` if there
  are other pending tool calls (due to parallel tool calling).](/python/langchain/agents/middleware/tool_call_limit/ExitBehavior)

## Functions

[function

hook\_config

Decorator to configure hook behavior in middleware methods.

Use this decorator on `before_model` or `after_model` methods in middleware classes
to configure their behavior. Currently supports specifying which destinations they
can jump to, which establishes conditional edges in the agent graph.](/python/langchain/agents/middleware/tool_call_limit/hook_config)

## Classes

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/tool_call_limit/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/tool_call_limit/AgentState)[class

ToolCallLimitState

State schema for `ToolCallLimitMiddleware`.

Extends `AgentState` with tool call tracking fields.

The count fields are dictionaries mapping tool names to execution counts. This
allows multiple middleware instances to track different tools independently. The
special key `'__all__'` is used for tracking all tool calls globally.](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitState)[class

ToolCallLimitExceededError

Exception raised when tool call limits are exceeded.

This exception is raised when the configured exit behavior is `'error'` and either
the thread or run tool call limit has been exceeded.](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitExceededError)[class

ToolCallLimitMiddleware

Track tool call counts and enforces limits during agent execution.

This middleware monitors the number of tool calls made and can terminate or
restrict execution when limits are exceeded. It supports both thread-level
(persistent across runs) and run-level (per invocation) call counting.](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitMiddleware)


