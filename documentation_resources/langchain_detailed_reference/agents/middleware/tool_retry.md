<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/tool_retry -->

Modulev1.2.13 (latest)●Since v1.0

# tool\_retry

Tool retry middleware for agents.

## Attributes

[attribute

ResponseT](/python/langchain/agents/middleware/tool_retry/ResponseT)

## Functions

[function

calculate\_delay

Calculate delay for a retry attempt with exponential backoff and optional jitter.](/python/langchain/agents/middleware/tool_retry/calculate_delay)[function

should\_retry\_exception

Check if an exception should trigger a retry.](/python/langchain/agents/middleware/tool_retry/should_retry_exception)[function

validate\_retry\_params

Validate retry parameters.](/python/langchain/agents/middleware/tool_retry/validate_retry_params)

## Classes

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/tool_retry/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/tool_retry/AgentState)[class

ToolRetryMiddleware

Middleware that automatically retries failed tool calls with configurable backoff.

Supports retrying on specific exceptions and exponential backoff.](/python/langchain/agents/middleware/tool_retry/ToolRetryMiddleware)

## Type Aliases

[typeAlias

OnFailure: Literal['error', 'continue'] | Callable[[Exception], str]

Type for specifying failure handling behavior.

Can be either:

- A literal action string (`'error'` or `'continue'`)
  - `'error'`: Re-raise the exception, stopping agent execution.
  - `'continue'`: Inject a message with the error details, allowing the agent to continue.
    For tool retries, a `ToolMessage` with the error details will be injected.
    For model retries, an `AIMessage` with the error details will be returned.
- A callable that takes an exception and returns a string for error message content](/python/langchain/agents/middleware/tool_retry/OnFailure)[typeAlias

RetryOn: tuple[type[Exception], ...] | Callable[[Exception], bool]

Type for specifying which exceptions to retry on.

Can be either:

- A tuple of exception types to retry on (based on `isinstance` checks)
- A callable that takes an exception and returns `True` if it should be retried](/python/langchain/agents/middleware/tool_retry/RetryOn)


