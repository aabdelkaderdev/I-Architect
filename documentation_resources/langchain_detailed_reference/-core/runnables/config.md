<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/config -->

Modulev1.2.21 (latest)●Since v0.1

# config

Configuration utilities for `Runnable` objects.

## Attributes

[attribute

Input](/python/langchain-core/runnables/utils/Input)[attribute

Output](/python/langchain-core/runnables/utils/Output)[attribute

CONFIG\_KEYS: list](/python/langchain-core/runnables/config/CONFIG_KEYS)[attribute

COPIABLE\_KEYS: list](/python/langchain-core/runnables/config/COPIABLE_KEYS)[attribute

DEFAULT\_RECURSION\_LIMIT: int](/python/langchain-core/runnables/config/DEFAULT_RECURSION_LIMIT)[attribute

var\_child\_runnable\_config: ContextVar[RunnableConfig | None]](/python/langchain-core/runnables/config/var_child_runnable_config)[attribute

P](/python/langchain-core/runnables/config/P)[attribute

T](/python/langchain-core/runnables/config/T)

## Functions

[function

accepts\_config

Check if a callable accepts a config argument.](/python/langchain-core/runnables/utils/accepts_config)[function

accepts\_run\_manager

Check if a callable accepts a run\_manager argument.](/python/langchain-core/runnables/utils/accepts_run_manager)[function

set\_config\_context

Set the child Runnable config + tracing context.](/python/langchain-core/runnables/config/set_config_context)[function

ensure\_config

Ensure that a config is a dict with all keys present.](/python/langchain-core/runnables/config/ensure_config)[function

get\_config\_list

Get a list of configs from a single config or a list of configs.

It is useful for subclasses overriding batch() or abatch().](/python/langchain-core/runnables/config/get_config_list)[function

patch\_config

Patch a config with new values.](/python/langchain-core/runnables/config/patch_config)[function

merge\_configs

Merge multiple configs into one.](/python/langchain-core/runnables/config/merge_configs)[function

call\_func\_with\_variable\_args

Call function that may optionally accept a run\_manager and/or config.](/python/langchain-core/runnables/config/call_func_with_variable_args)[function

acall\_func\_with\_variable\_args

Async call function that may optionally accept a run\_manager and/or config.](/python/langchain-core/runnables/config/acall_func_with_variable_args)[function

get\_callback\_manager\_for\_config

Get a callback manager for a config.](/python/langchain-core/runnables/config/get_callback_manager_for_config)[function

get\_async\_callback\_manager\_for\_config

Get an async callback manager for a config.](/python/langchain-core/runnables/config/get_async_callback_manager_for_config)[function

get\_executor\_for\_config

Get an executor for a config.](/python/langchain-core/runnables/config/get_executor_for_config)[function

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)

## Classes

[class

AsyncCallbackManager

Async callback manager that handles callbacks from LangChain.](/python/langchain-core/callbacks/manager/AsyncCallbackManager)[class

CallbackManager

Callback manager for LangChain.](/python/langchain-core/callbacks/manager/CallbackManager)[class

BaseCallbackManager

Base callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager)[class

AsyncCallbackManagerForChainRun

Async callback manager for chain run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainRun)[class

CallbackManagerForChainRun

Callback manager for chain run.](/python/langchain-core/callbacks/manager/CallbackManagerForChainRun)[class

EmptyDict

Empty dict type.](/python/langchain-core/runnables/config/EmptyDict)[class

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

ContextThreadPoolExecutor

ThreadPoolExecutor that copies the context to the child thread.](/python/langchain-core/runnables/config/ContextThreadPoolExecutor)

## Type Aliases

[typeAlias

Callbacks: list[BaseCallbackHandler] | BaseCallbackManager | None](/python/langchain-core/callbacks/base/Callbacks)


