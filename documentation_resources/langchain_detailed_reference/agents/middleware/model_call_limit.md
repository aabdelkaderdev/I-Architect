<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/model_call_limit -->

Modulev1.2.13 (latest)●Since v1.0

# model\_call\_limit

Call tracking middleware for agents.

## Attributes

[attribute

PrivateStateAttr

Annotation used to mark state attributes as purely internal for a given middleware.](/python/langchain/agents/middleware/model_call_limit/PrivateStateAttr)[attribute

ResponseT](/python/langchain/agents/middleware/model_call_limit/ResponseT)

## Functions

[function

hook\_config

Decorator to configure hook behavior in middleware methods.

Use this decorator on `before_model` or `after_model` methods in middleware classes
to configure their behavior. Currently supports specifying which destinations they
can jump to, which establishes conditional edges in the agent graph.](/python/langchain/agents/middleware/model_call_limit/hook_config)

## Classes

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/model_call_limit/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/model_call_limit/AgentState)[class

ModelCallLimitState

State schema for `ModelCallLimitMiddleware`.

Extends `AgentState` with model call tracking fields.](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitState)[class

ModelCallLimitExceededError

Exception raised when model call limits are exceeded.

This exception is raised when the configured exit behavior is `'error'` and either
the thread or run model call limit has been exceeded.](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitExceededError)[class

ModelCallLimitMiddleware

Tracks model call counts and enforces limits.

This middleware monitors the number of model calls made during agent execution
and can terminate the agent when specified limits are reached. It supports
both thread-level and run-level call counting with configurable exit behaviors.

Thread-level: The middleware tracks the number of model calls and persists
call count across multiple runs (invocations) of the agent.

Run-level: The middleware tracks the number of model calls made during a single
run (invocation) of the agent.](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitMiddleware)


