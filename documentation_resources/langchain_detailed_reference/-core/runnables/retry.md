<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/retry -->

Modulev1.2.21 (latest)●Since v0.1

# retry

`Runnable` that retries a `Runnable` if it fails.

## Attributes

[attribute

Input](/python/langchain-core/runnables/utils/Input)[attribute

Output](/python/langchain-core/runnables/utils/Output)[attribute

T](/python/langchain-core/runnables/retry/T)[attribute

U](/python/langchain-core/runnables/retry/U)

## Functions

[function

patch\_config

Patch a config with new values.](/python/langchain-core/runnables/config/patch_config)

## Classes

[class

RunnableBindingBase

`Runnable` that delegates calls to another `Runnable` with a set of `**kwargs`.

Use only if creating a new `RunnableBinding` subclass with different `__init__`
args.

See documentation for `RunnableBinding` for more details.](/python/langchain-core/runnables/base/RunnableBindingBase)[class

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

AsyncCallbackManagerForChainRun

Async callback manager for chain run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainRun)[class

CallbackManagerForChainRun

Callback manager for chain run.](/python/langchain-core/callbacks/manager/CallbackManagerForChainRun)[class

ExponentialJitterParams

Parameters for `tenacity.wait_exponential_jitter`.](/python/langchain-core/runnables/retry/ExponentialJitterParams)[class

RunnableRetry

Retry a Runnable if it fails.

RunnableRetry can be used to add retry logic to any object
that subclasses the base Runnable.

Such retries are especially useful for network calls that may fail
due to transient errors.

The RunnableRetry is implemented as a RunnableBinding. The easiest
way to use it is through the `.with_retry()` method on all Runnables.

Example:
Here's an example that uses a RunnableLambda to raise an exception

```
import time

def foo(input) -> None:
    '''Fake function that raises an exception.'''
    raise ValueError(f"Invoking foo failed. At time {time.time()}")

runnable = RunnableLambda(foo)

runnable_with_retries = runnable.with_retry(
    retry_if_exception_type=(ValueError,),  # Retry only on ValueError
    wait_exponential_jitter=True,  # Add jitter to the exponential backoff
    stop_after_attempt=2,  # Try twice
    exponential_jitter_params={"initial": 2},  # if desired, customize backoff
)

# The method invocation above is equivalent to the longer form below:

runnable_with_retries = RunnableRetry(
    bound=runnable,
    retry_exception_types=(ValueError,),
    max_attempt_number=2,
    wait_exponential_jitter=True,
    exponential_jitter_params={"initial": 2},
)
```

This logic can be used to retry any Runnable, including a chain of Runnables,
but in general it's best practice to keep the scope of the retry as small as
possible. For example, if you have a chain of Runnables, you should only retry
the Runnable that is likely to fail, not the entire chain.](/python/langchain-core/runnables/retry/RunnableRetry)


