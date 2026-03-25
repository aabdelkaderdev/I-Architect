<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/context -->

Modulev1.2.21 (latest)●Since v0.1

# context

Context management for tracers.

## Attributes

[attribute

tracing\_callback\_var: Any](/python/langchain-core/tracers/context/tracing_callback_var)[attribute

tracing\_v2\_callback\_var: ContextVar[LangChainTracer | None]](/python/langchain-core/tracers/context/tracing_v2_callback_var)[attribute

run\_collector\_var: ContextVar[RunCollectorCallbackHandler | None]](/python/langchain-core/tracers/context/run_collector_var)

## Functions

[function

tracing\_v2\_enabled

Instruct LangChain to log all runs in context to LangSmith.](/python/langchain-core/tracers/context/tracing_v2_enabled)[function

collect\_runs

Collect all run traces in context.](/python/langchain-core/tracers/context/collect_runs)[function

register\_configure\_hook

Register a configure hook.](/python/langchain-core/tracers/context/register_configure_hook)

## Classes

[class

LangChainTracer

Implementation of the `SharedTracer` that `POSTS` to the LangChain endpoint.](/python/langchain-core/tracers/langchain/LangChainTracer)[class

RunCollectorCallbackHandler

Tracer that collects all nested runs in a list.

This tracer is useful for inspection and evaluation purposes.](/python/langchain-core/tracers/run_collector/RunCollectorCallbackHandler)[class

BaseCallbackHandler

Base callback handler.](/python/langchain-core/callbacks/base/BaseCallbackHandler)[class

AsyncCallbackManager

Async callback manager that handles callbacks from LangChain.](/python/langchain-core/callbacks/manager/AsyncCallbackManager)[class

CallbackManager

Callback manager for LangChain.](/python/langchain-core/callbacks/manager/CallbackManager)

## Type Aliases

[typeAlias

Callbacks: list[BaseCallbackHandler] | BaseCallbackManager | None](/python/langchain-core/callbacks/base/Callbacks)


