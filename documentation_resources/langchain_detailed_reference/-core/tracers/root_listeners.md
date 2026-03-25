<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/root_listeners -->

Modulev1.2.21 (latest)●Since v0.1

# root\_listeners

Tracers that call listeners.

## Attributes

[attribute

Run: RunTree](/python/langchain-core/tracers/schemas/Run)

## Functions

[function

acall\_func\_with\_variable\_args

Async call function that may optionally accept a run\_manager and/or config.](/python/langchain-core/runnables/config/acall_func_with_variable_args)[function

call\_func\_with\_variable\_args

Call function that may optionally accept a run\_manager and/or config.](/python/langchain-core/runnables/config/call_func_with_variable_args)

## Classes

[class

RunnableConfig

Configuration for a `Runnable`.

Note

Custom values

The `TypedDict` has `total=False` set intentionally to:

- Allow partial configs to be created and merged together via `merge_configs`
- Support config propagation from parent to child runnables via
  `var_child_runnable_config` (a `ContextVar` that automatically passes
  config down the call stack without explicit parameter passing), where
  configs are merged rather than replaced

Example

```
# Parent sets tags
chain.invoke(input, config={"tags": ["parent"]})
# Child automatically inherits and can add:
# ensure_config({"tags": ["child"]}) -> {"tags": ["parent", "child"]}
```](/python/langchain-core/runnables/config/RunnableConfig)[class

AsyncBaseTracer

Async base interface for tracers.](/python/langchain-core/tracers/base/AsyncBaseTracer)[class

BaseTracer

Base interface for tracers.](/python/langchain-core/tracers/base/BaseTracer)[class

RootListenersTracer

Tracer that calls listeners on run start, end, and error.](/python/langchain-core/tracers/root_listeners/RootListenersTracer)[class

AsyncRootListenersTracer

Async tracer that calls listeners on run start, end, and error.](/python/langchain-core/tracers/root_listeners/AsyncRootListenersTracer)

## Type Aliases

[typeAlias

Listener: Callable[[Run], None] | Callable[[Run, RunnableConfig], None]](/python/langchain-core/tracers/root_listeners/Listener)[typeAlias

AsyncListener: Callable[[Run], Awaitable[None]] | Callable[[Run, RunnableConfig], Awaitable[None]]](/python/langchain-core/tracers/root_listeners/AsyncListener)


