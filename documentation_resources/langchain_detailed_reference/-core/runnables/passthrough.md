<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/passthrough -->

Modulev1.2.21 (latest)●Since v0.1

# passthrough

Implementation of the `RunnablePassthrough`.

## Attributes

[attribute

Other](/python/langchain-core/runnables/base/Other)[attribute

atee: Tee](/python/langchain-core/utils/aiter/atee)[attribute

safetee: Tee](/python/langchain-core/utils/iter/safetee)

## Functions

[function

acall\_func\_with\_variable\_args

Async call function that may optionally accept a run\_manager and/or config.](/python/langchain-core/runnables/config/acall_func_with_variable_args)[function

call\_func\_with\_variable\_args

Call function that may optionally accept a run\_manager and/or config.](/python/langchain-core/runnables/config/call_func_with_variable_args)[function

ensure\_config

Ensure that a config is a dict with all keys present.](/python/langchain-core/runnables/config/ensure_config)[function

get\_executor\_for\_config

Get an executor for a config.](/python/langchain-core/runnables/config/get_executor_for_config)[function

patch\_config

Patch a config with new values.](/python/langchain-core/runnables/config/patch_config)[function

create\_model\_v2

Create a Pydantic model with the given field definitions.

Warning

Do not use outside of langchain packages. This API is subject to change at any
time.](/python/langchain-core/utils/pydantic/create_model_v2)[function

identity

Identity function.](/python/langchain-core/runnables/passthrough/identity)[function

aidentity

Async identity function.](/python/langchain-core/runnables/passthrough/aidentity)

## Classes

[class

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

RunnableParallel

Runnable that runs a mapping of `Runnable`s in parallel.

Returns a mapping of their outputs.

`RunnableParallel` is one of the two main composition primitives,
alongside `RunnableSequence`. It invokes `Runnable`s concurrently, providing the
same input to each.

A `RunnableParallel` can be instantiated directly or by using a dict literal
within a sequence.

Here is a simple example that uses functions to illustrate the use of
`RunnableParallel`:

```
from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

def mul_three(x: int) -> int:
    return x * 3

runnable_1 = RunnableLambda(add_one)
runnable_2 = RunnableLambda(mul_two)
runnable_3 = RunnableLambda(mul_three)

sequence = runnable_1 | {  # this dict is coerced to a RunnableParallel
    "mul_two": runnable_2,
    "mul_three": runnable_3,
}
# Or equivalently:
# sequence = runnable_1 | RunnableParallel(
#     {"mul_two": runnable_2, "mul_three": runnable_3}
# )
# Also equivalently:
# sequence = runnable_1 | RunnableParallel(
#     mul_two=runnable_2,
#     mul_three=runnable_3,
# )

sequence.invoke(1)
await sequence.ainvoke(1)

sequence.batch([1, 2, 3])
await sequence.abatch([1, 2, 3])
```

`RunnableParallel` makes it easy to run `Runnable`s in parallel. In the below
example, we simultaneously stream output from two different `Runnable` objects:

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

model = ChatOpenAI()
joke_chain = (
    ChatPromptTemplate.from_template("tell me a joke about {topic}") | model
)
poem_chain = (
    ChatPromptTemplate.from_template("write a 2-line poem about {topic}")
    | model
)

runnable = RunnableParallel(joke=joke_chain, poem=poem_chain)

# Display stream
output = {key: "" for key, _ in runnable.output_schema()}
for chunk in runnable.stream({"topic": "bear"}):
    for key in chunk:
        output[key] = output[key] + chunk[key].content
    print(output)  # noqa: T201
```](/python/langchain-core/runnables/base/RunnableParallel)[class

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

AddableDict

Dictionary that can be added to another dictionary.](/python/langchain-core/runnables/utils/AddableDict)[class

ConfigurableFieldSpec

Field that can be configured by the user. It is a specification of a field.](/python/langchain-core/runnables/utils/ConfigurableFieldSpec)[class

AsyncCallbackManagerForChainRun

Async callback manager for chain run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainRun)[class

CallbackManagerForChainRun

Callback manager for chain run.](/python/langchain-core/callbacks/manager/CallbackManagerForChainRun)[class

Graph

Graph of nodes and edges.](/python/langchain-core/runnables/graph/Graph)[class

RunnablePassthrough

Runnable to passthrough inputs unchanged or with additional keys.

This `Runnable` behaves almost like the identity function, except that it
can be configured to add additional keys to the output, if the input is a
dict.

The examples below demonstrate this `Runnable` works using a few simple
chains. The chains rely on simple lambdas to make the examples easy to execute
and experiment with.](/python/langchain-core/runnables/passthrough/RunnablePassthrough)[class

RunnableAssign

Runnable that assigns key-value pairs to `dict[str, Any]` inputs.

The `RunnableAssign` class takes input dictionaries and, through a
`RunnableParallel` instance, applies transformations, then combines
these with the original data, introducing new key-value pairs based
on the mapper's logic.](/python/langchain-core/runnables/passthrough/RunnableAssign)[class

RunnablePick

`Runnable` that picks keys from `dict[str, Any]` inputs.

`RunnablePick` class represents a `Runnable` that selectively picks keys from a
dictionary input. It allows you to specify one or more keys to extract
from the input dictionary.

Return Type Behavior

The return type depends on the `keys` parameter:

- When `keys` is a `str`: Returns the single value associated with that key
- When `keys` is a `list`: Returns a dictionary containing only the selected
  keys](/python/langchain-core/runnables/passthrough/RunnablePick)


