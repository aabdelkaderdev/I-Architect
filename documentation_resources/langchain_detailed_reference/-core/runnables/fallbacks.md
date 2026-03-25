<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/fallbacks -->

Modulev1.2.21 (latest)●Since v0.1

# fallbacks

`Runnable` that can fallback to other `Runnable` objects if it fails.

## Attributes

[attribute

Input](/python/langchain-core/runnables/utils/Input)[attribute

Output](/python/langchain-core/runnables/utils/Output)

## Functions

[function

ensure\_config

Ensure that a config is a dict with all keys present.](/python/langchain-core/runnables/config/ensure_config)[function

get\_async\_callback\_manager\_for\_config

Get an async callback manager for a config.](/python/langchain-core/runnables/config/get_async_callback_manager_for_config)[function

get\_callback\_manager\_for\_config

Get a callback manager for a config.](/python/langchain-core/runnables/config/get_callback_manager_for_config)[function

get\_config\_list

Get a list of configs from a single config or a list of configs.

It is useful for subclasses overriding batch() or abatch().](/python/langchain-core/runnables/config/get_config_list)[function

patch\_config

Patch a config with new values.](/python/langchain-core/runnables/config/patch_config)[function

set\_config\_context

Set the child Runnable config + tracing context.](/python/langchain-core/runnables/config/set_config_context)[function

coro\_with\_context

Await a coroutine with a context.](/python/langchain-core/runnables/utils/coro_with_context)[function

get\_unique\_config\_specs

Get the unique config specs from a sequence of config specs.](/python/langchain-core/runnables/utils/get_unique_config_specs)

## Classes

[class

AsyncCallbackManager

Async callback manager that handles callbacks from LangChain.](/python/langchain-core/callbacks/manager/AsyncCallbackManager)[class

CallbackManager

Callback manager for LangChain.](/python/langchain-core/callbacks/manager/CallbackManager)[class

Runnable

A unit of work that can be invoked, batched, streamed, transformed and composed.

# Key Methods

- `invoke`/`ainvoke`: Transforms a single input into an output.
- `batch`/`abatch`: Efficiently transforms multiple inputs into outputs.
- `stream`/`astream`: Streams output from a single input as it's produced.
- `astream_log`: Streams output and selected intermediate results from an
  input.

Built-in optimizations:

- **Batch**: By default, batch runs invoke() in parallel using a thread pool
  executor. Override to optimize batching.
- **Async**: Methods with `'a'` prefix are asynchronous. By default, they execute
  the sync counterpart using asyncio's thread pool.
  Override for native async.

All methods accept an optional config argument, which can be used to configure
execution, add tags and metadata for tracing and debugging etc.

Runnables expose schematic information about their input, output and config via
the `input_schema` property, the `output_schema` property and `config_schema`
method.

# Composition

Runnable objects can be composed together to create chains in a declarative way.

Any chain constructed this way will automatically have sync, async, batch, and
streaming support.

The main composition primitives are `RunnableSequence` and `RunnableParallel`.

**`RunnableSequence`** invokes a series of runnables sequentially, with
one Runnable's output serving as the next's input. Construct using
the `|` operator or by passing a list of runnables to `RunnableSequence`.

**`RunnableParallel`** invokes runnables concurrently, providing the same input
to each. Construct it using a dict literal within a sequence or by passing a
dict to `RunnableParallel`.

For example,

```
from langchain_core.runnables import RunnableLambda

# A RunnableSequence constructed using the `|` operator
sequence = RunnableLambda(lambda x: x + 1) | RunnableLambda(lambda x: x * 2)
sequence.invoke(1)  # 4
sequence.batch([1, 2, 3])  # [4, 6, 8]

# A sequence that contains a RunnableParallel constructed using a dict literal
sequence = RunnableLambda(lambda x: x + 1) | {
    "mul_2": RunnableLambda(lambda x: x * 2),
    "mul_5": RunnableLambda(lambda x: x * 5),
}
sequence.invoke(1)  # {'mul_2': 4, 'mul_5': 10}
```

# Standard Methods

All `Runnable`s expose additional methods that can be used to modify their
behavior (e.g., add a retry policy, add lifecycle listeners, make them
configurable, etc.).

These methods will work on any `Runnable`, including `Runnable` chains
constructed by composing other `Runnable`s.
See the individual methods for details.

For example,

```
from langchain_core.runnables import RunnableLambda

import random

def add_one(x: int) -> int:
    return x + 1

def buggy_double(y: int) -> int:
    """Buggy code that will fail 70% of the time"""
    if random.random() > 0.3:
        print('This code failed, and will probably be retried!')  # noqa: T201
        raise ValueError('Triggered buggy code')
    return y * 2

sequence = (
    RunnableLambda(add_one) |
    RunnableLambda(buggy_double).with_retry( # Retry on failure
        stop_after_attempt=10,
        wait_exponential_jitter=False
    )
)

print(sequence.input_schema.model_json_schema()) # Show inferred input schema
print(sequence.output_schema.model_json_schema()) # Show inferred output schema
print(sequence.invoke(2)) # invoke the sequence (note the retry above!!)
```

# Debugging and tracing

As the chains get longer, it can be useful to be able to see intermediate results
to debug and trace the chain.

You can set the global debug flag to True to enable debug output for all chains:

```
from langchain_core.globals import set_debug

set_debug(True)
```

Alternatively, you can pass existing or custom callbacks to any given chain:

```
from langchain_core.tracers import ConsoleCallbackHandler

chain.invoke(..., config={"callbacks": [ConsoleCallbackHandler()]})
```

For a UI (and much more) checkout [LangSmith](https://docs.langchain.com/langsmith/home).](/python/langchain-core/runnables/base/Runnable)[class

RunnableSerializable

Runnable that can be serialized to JSON.](/python/langchain-core/runnables/base/RunnableSerializable)[class

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

ConfigurableFieldSpec

Field that can be configured by the user. It is a specification of a field.](/python/langchain-core/runnables/utils/ConfigurableFieldSpec)[class

AsyncCallbackManagerForChainRun

Async callback manager for chain run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainRun)[class

RunnableWithFallbacks

`Runnable` that can fallback to other `Runnable` objects if it fails.

External APIs (e.g., APIs for a language model) may at times experience
degraded performance or even downtime.

In these cases, it can be useful to have a fallback `Runnable` that can be
used in place of the original `Runnable` (e.g., fallback to another LLM provider).

Fallbacks can be defined at the level of a single `Runnable`, or at the level
of a chain of `Runnable`s. Fallbacks are tried in order until one succeeds or
all fail.

While you can instantiate a `RunnableWithFallbacks` directly, it is usually
more convenient to use the `with_fallbacks` method on a `Runnable`.](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks)


