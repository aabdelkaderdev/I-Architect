<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base -->

Modulev1.2.21 (latest)●Since v0.1

# base

Base classes and utilities for `Runnable` objects.

## Attributes

[attribute

Input](/python/langchain-core/runnables/utils/Input)[attribute

Output](/python/langchain-core/runnables/utils/Output)[attribute

atee: Tee](/python/langchain-core/utils/aiter/atee)[attribute

safetee: Tee](/python/langchain-core/utils/iter/safetee)[attribute

Run: RunTree](/python/langchain-core/tracers/schemas/Run)[attribute

Other](/python/langchain-core/runnables/base/Other)[attribute

RunnableMap: RunnableParallel](/python/langchain-core/runnables/base/RunnableMap)

## Functions

[function

acall\_func\_with\_variable\_args

Async call function that may optionally accept a run\_manager and/or config.](/python/langchain-core/runnables/config/acall_func_with_variable_args)[function

call\_func\_with\_variable\_args

Call function that may optionally accept a run\_manager and/or config.](/python/langchain-core/runnables/config/call_func_with_variable_args)[function

ensure\_config

Ensure that a config is a dict with all keys present.](/python/langchain-core/runnables/config/ensure_config)[function

get\_async\_callback\_manager\_for\_config

Get an async callback manager for a config.](/python/langchain-core/runnables/config/get_async_callback_manager_for_config)[function

get\_callback\_manager\_for\_config

Get a callback manager for a config.](/python/langchain-core/runnables/config/get_callback_manager_for_config)[function

get\_config\_list

Get a list of configs from a single config or a list of configs.

It is useful for subclasses overriding batch() or abatch().](/python/langchain-core/runnables/config/get_config_list)[function

get\_executor\_for\_config

Get an executor for a config.](/python/langchain-core/runnables/config/get_executor_for_config)[function

merge\_configs

Merge multiple configs into one.](/python/langchain-core/runnables/config/merge_configs)[function

patch\_config

Patch a config with new values.](/python/langchain-core/runnables/config/patch_config)[function

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)[function

set\_config\_context

Set the child Runnable config + tracing context.](/python/langchain-core/runnables/config/set_config_context)[function

accepts\_config

Check if a callable accepts a config argument.](/python/langchain-core/runnables/utils/accepts_config)[function

accepts\_run\_manager

Check if a callable accepts a run\_manager argument.](/python/langchain-core/runnables/utils/accepts_run_manager)[function

coro\_with\_context

Await a coroutine with a context.](/python/langchain-core/runnables/utils/coro_with_context)[function

gated\_coro

Run a coroutine with a semaphore.](/python/langchain-core/runnables/utils/gated_coro)[function

gather\_with\_concurrency

Gather coroutines with a limit on the number of concurrent coroutines.](/python/langchain-core/runnables/utils/gather_with_concurrency)[function

get\_function\_first\_arg\_dict\_keys

Get the keys of the first argument of a function if it is a dict.](/python/langchain-core/runnables/utils/get_function_first_arg_dict_keys)[function

get\_function\_nonlocals

Get the nonlocal variables accessed by a function.](/python/langchain-core/runnables/utils/get_function_nonlocals)[function

get\_lambda\_source

Get the source code of a lambda function.](/python/langchain-core/runnables/utils/get_lambda_source)[function

get\_unique\_config\_specs

Get the unique config specs from a sequence of config specs.](/python/langchain-core/runnables/utils/get_unique_config_specs)[function

indent\_lines\_after\_first

Indent all lines of text after the first line.](/python/langchain-core/runnables/utils/indent_lines_after_first)[function

is\_async\_callable

Check if a function is async.](/python/langchain-core/runnables/utils/is_async_callable)[function

is\_async\_generator

Check if a function is an async generator.](/python/langchain-core/runnables/utils/is_async_generator)[function

create\_model\_v2

Create a Pydantic model with the given field definitions.

Warning

Do not use outside of langchain packages. This API is subject to change at any
time.](/python/langchain-core/utils/pydantic/create_model_v2)[function

coerce\_to\_runnable

Coerce a `Runnable`-like object into a `Runnable`.](/python/langchain-core/runnables/base/coerce_to_runnable)[function

chain

Decorate a function to make it a `Runnable`.

Sets the name of the `Runnable` to the name of the function.
Any runnables called by the function will be traced as dependencies.](/python/langchain-core/runnables/base/chain)

## Classes

[class

AsyncCallbackManager

Async callback manager that handles callbacks from LangChain.](/python/langchain-core/callbacks/manager/AsyncCallbackManager)[class

CallbackManager

Callback manager for LangChain.](/python/langchain-core/callbacks/manager/CallbackManager)[class

Serializable

Serializable base class.

This class is used to serialize objects to JSON.

It relies on the following methods and properties:

- [`is_lc_serializable`](/python/langchain-core/load/serializable/Serializable/is_lc_serializable): Is this class serializable?

  By design, even if a class inherits from `Serializable`, it is not serializable
  by default. This is to prevent accidental serialization of objects that should
  not be serialized.
- [`get_lc_namespace`](/python/langchain-core/load/serializable/Serializable/get_lc_namespace): Get the namespace of the LangChain object.

  During deserialization, this namespace is used to identify
  the correct class to instantiate.

  Please see the `Reviver` class in `langchain_core.load.load` for more details.

  During deserialization an additional mapping is handle classes that have moved
  or been renamed across package versions.
- [`lc_secrets`](/python/langchain-core/load/serializable/Serializable/lc_secrets): A map of constructor argument names to secret ids.
- [`lc_attributes`](/python/langchain-core/load/serializable/Serializable/lc_attributes): List of additional attribute names that should be included
  as part of the serialized representation.](/python/langchain-core/load/serializable/Serializable)[class

SerializedConstructor

Serialized constructor.](/python/langchain-core/load/serializable/SerializedConstructor)[class

SerializedNotImplemented

Serialized not implemented.](/python/langchain-core/load/serializable/SerializedNotImplemented)[class

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

ConfigurableField

Field that can be configured by the user.](/python/langchain-core/runnables/utils/ConfigurableField)[class

ConfigurableFieldSpec

Field that can be configured by the user. It is a specification of a field.](/python/langchain-core/runnables/utils/ConfigurableFieldSpec)[class

LogStreamCallbackHandler

Tracer that streams run logs to a stream.](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler)[class

AsyncRootListenersTracer

Async tracer that calls listeners on run start, end, and error.](/python/langchain-core/tracers/root_listeners/AsyncRootListenersTracer)[class

RootListenersTracer

Tracer that calls listeners on run start, end, and error.](/python/langchain-core/tracers/root_listeners/RootListenersTracer)[class

aclosing

Async context manager to wrap an `AsyncGenerator` that has a `aclose()` method.

Code like this:

```
async with aclosing(<module>.fetch(<arguments>)) as agen:
    <block>
```

...is equivalent to this:

```
agen = <module>.fetch(<arguments>)
try:
    <block>
finally:
    await agen.aclose()
```](/python/langchain-core/utils/aiter/aclosing)[class

AsyncCallbackManagerForChainRun

Async callback manager for chain run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainRun)[class

CallbackManagerForChainRun

Callback manager for chain run.](/python/langchain-core/callbacks/manager/CallbackManagerForChainRun)[class

BasePromptTemplate

Base class for all prompt templates, returning a prompt.](/python/langchain-core/prompts/base/BasePromptTemplate)[class

RunnableWithFallbacksT

`Runnable` that can fallback to other `Runnable` objects if it fails.

External APIs (e.g., APIs for a language model) may at times experience
degraded performance or even downtime.

In these cases, it can be useful to have a fallback `Runnable` that can be
used in place of the original `Runnable` (e.g., fallback to another LLM provider).

Fallbacks can be defined at the level of a single `Runnable`, or at the level
of a chain of `Runnable`s. Fallbacks are tried in order until one succeeds or
all fail.

While you can instantiate a `RunnableWithFallbacks` directly, it is usually
more convenient to use the `with_fallbacks` method on a `Runnable`.](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks)[class

Graph

Graph of nodes and edges.](/python/langchain-core/runnables/graph/Graph)[class

ExponentialJitterParams

Parameters for `tenacity.wait_exponential_jitter`.](/python/langchain-core/runnables/retry/ExponentialJitterParams)[class

BaseTool

Base class for all LangChain tools.

This abstract class defines the interface that all LangChain tools must implement.

Tools are components that can be called by agents to perform specific actions.](/python/langchain-core/tools/base/BaseTool)[class

RunLog

Run log.](/python/langchain-core/tracers/log_stream/RunLog)[class

RunLogPatch

Patch to the run log.](/python/langchain-core/tracers/log_stream/RunLogPatch)[class

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

RunnableSequence

Sequence of `Runnable` objects, where the output of one is the input of the next.

**`RunnableSequence`** is the most important composition operator in LangChain
as it is used in virtually every chain.

A `RunnableSequence` can be instantiated directly or more commonly by using the
`|` operator where either the left or right operands (or both) must be a
`Runnable`.

Any `RunnableSequence` automatically supports sync, async, batch.

The default implementations of `batch` and `abatch` utilize threadpools and
asyncio gather and will be faster than naive invocation of `invoke` or `ainvoke`
for IO bound `Runnable`s.

Batching is implemented by invoking the batch method on each component of the
`RunnableSequence` in order.

A `RunnableSequence` preserves the streaming properties of its components, so if
all components of the sequence implement a `transform` method -- which
is the method that implements the logic to map a streaming input to a streaming
output -- then the sequence will be able to stream input to output!

If any component of the sequence does not implement transform then the
streaming will only begin after this component is run. If there are
multiple blocking components, streaming begins after the last one.

Note

`RunnableLambdas` do not support `transform` by default! So if you need to
use a `RunnableLambdas` be careful about where you place them in a
`RunnableSequence` (if you need to use the `stream`/`astream` methods).

If you need arbitrary logic and need streaming, you can subclass
Runnable, and implement `transform` for whatever logic you need.

Here is a simple example that uses simple functions to illustrate the use of
`RunnableSequence`:

```
from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

runnable_1 = RunnableLambda(add_one)
runnable_2 = RunnableLambda(mul_two)
sequence = runnable_1 | runnable_2
# Or equivalently:
# sequence = RunnableSequence(first=runnable_1, last=runnable_2)
sequence.invoke(1)
await sequence.ainvoke(1)

sequence.batch([1, 2, 3])
await sequence.abatch([1, 2, 3])
```

Here's an example that uses streams JSON output generated by an LLM:

```
from langchain_core.output_parsers.json import SimpleJsonOutputParser
from langchain_openai import ChatOpenAI

prompt = PromptTemplate.from_template(
    "In JSON format, give me a list of {topic} and their "
    "corresponding names in French, Spanish and in a "
    "Cat Language."
)

model = ChatOpenAI()
chain = prompt | model | SimpleJsonOutputParser()

async for chunk in chain.astream({"topic": "colors"}):
    print("-")  # noqa: T201
    print(chunk, sep="", flush=True)  # noqa: T201
```](/python/langchain-core/runnables/base/RunnableSequence)[class

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

RunnableGenerator

`Runnable` that runs a generator function.

`RunnableGenerator`s can be instantiated directly or by using a generator within
a sequence.

`RunnableGenerator`s can be used to implement custom behavior, such as custom
output parsers, while preserving streaming capabilities. Given a generator function
with a signature `Iterator[A] -> Iterator[B]`, wrapping it in a
`RunnableGenerator` allows it to emit output chunks as soon as they are streamed
in from the previous step.

Note

If a generator function has a `signature A -> Iterator[B]`, such that it
requires its input from the previous step to be completed before emitting chunks
(e.g., most LLMs need the entire prompt available to start generating), it can
instead be wrapped in a `RunnableLambda`.

Here is an example to show the basic mechanics of a `RunnableGenerator`:

```
from typing import Any, AsyncIterator, Iterator

from langchain_core.runnables import RunnableGenerator

def gen(input: Iterator[Any]) -> Iterator[str]:
    for token in ["Have", " a", " nice", " day"]:
        yield token

runnable = RunnableGenerator(gen)
runnable.invoke(None)  # "Have a nice day"
list(runnable.stream(None))  # ["Have", " a", " nice", " day"]
runnable.batch([None, None])  # ["Have a nice day", "Have a nice day"]

# Async version:
async def agen(input: AsyncIterator[Any]) -> AsyncIterator[str]:
    for token in ["Have", " a", " nice", " day"]:
        yield token

runnable = RunnableGenerator(agen)
await runnable.ainvoke(None)  # "Have a nice day"
[p async for p in runnable.astream(None)]  # ["Have", " a", " nice", " day"]
```

`RunnableGenerator` makes it easy to implement custom behavior within a streaming
context. Below we show an example:

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableGenerator, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI()
chant_chain = (
    ChatPromptTemplate.from_template("Give me a 3 word chant about {topic}")
    | model
    | StrOutputParser()
)

def character_generator(input: Iterator[str]) -> Iterator[str]:
    for token in input:
        if "," in token or "." in token:
            yield "👏" + token
        else:
            yield token

runnable = chant_chain | character_generator
assert type(runnable.last) is RunnableGenerator
"".join(runnable.stream({"topic": "waste"}))  # Reduce👏, Reuse👏, Recycle👏.

# Note that RunnableLambda can be used to delay streaming of one step in a
# sequence until the previous step is finished:
def reverse_generator(input: str) -> Iterator[str]:
    # Yield characters of input in reverse order.
    for character in input[::-1]:
        yield character

runnable = chant_chain | RunnableLambda(reverse_generator)
"".join(runnable.stream({"topic": "waste"}))  # ".elcycer ,esuer ,ecudeR"
```](/python/langchain-core/runnables/base/RunnableGenerator)[class

RunnableLambda

`RunnableLambda` converts a python callable into a `Runnable`.

Wrapping a callable in a `RunnableLambda` makes the callable usable
within either a sync or async context.

`RunnableLambda` can be composed as any other `Runnable` and provides
seamless integration with LangChain tracing.

`RunnableLambda` is best suited for code that does not need to support
streaming. If you need to support streaming (i.e., be able to operate
on chunks of inputs and yield chunks of outputs), use `RunnableGenerator`
instead.

Note that if a `RunnableLambda` returns an instance of `Runnable`, that
instance is invoked (or streamed) during execution.](/python/langchain-core/runnables/base/RunnableLambda)[class

RunnableEachBase

RunnableEachBase class.

`Runnable` that calls another `Runnable` for each element of the input sequence.

Use only if creating a new `RunnableEach` subclass with different `__init__`
args.

See documentation for `RunnableEach` for more details.](/python/langchain-core/runnables/base/RunnableEachBase)[class

RunnableEach

RunnableEach class.

`Runnable` that calls another `Runnable` for each element of the input sequence.

It allows you to call multiple inputs with the bounded `Runnable`.

`RunnableEach` makes it easy to run multiple inputs for the `Runnable`.
In the below example, we associate and run three inputs
with a `Runnable`:

```
from langchain_core.runnables.base import RunnableEach
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
prompt = ChatPromptTemplate.from_template("Tell me a short joke about
{topic}")
model = ChatOpenAI()
output_parser = StrOutputParser()
runnable = prompt | model | output_parser
runnable_each = RunnableEach(bound=runnable)
output = runnable_each.invoke([{'topic':'Computer Science'},
                            {'topic':'Art'},
                            {'topic':'Biology'}])
print(output)  # noqa: T201
```](/python/langchain-core/runnables/base/RunnableEach)[class

RunnableBindingBase

`Runnable` that delegates calls to another `Runnable` with a set of `**kwargs`.

Use only if creating a new `RunnableBinding` subclass with different `__init__`
args.

See documentation for `RunnableBinding` for more details.](/python/langchain-core/runnables/base/RunnableBindingBase)[class

RunnableBinding

Wrap a `Runnable` with additional functionality.

A `RunnableBinding` can be thought of as a "runnable decorator" that
preserves the essential features of `Runnable`; i.e., batching, streaming,
and async support, while adding additional functionality.

Any class that inherits from `Runnable` can be bound to a `RunnableBinding`.
Runnables expose a standard set of methods for creating `RunnableBindings`
or sub-classes of `RunnableBindings` (e.g., `RunnableRetry`,
`RunnableWithFallbacks`) that add additional functionality.

These methods include:

- `bind`: Bind kwargs to pass to the underlying `Runnable` when running it.
- `with_config`: Bind config to pass to the underlying `Runnable` when running
  it.
- `with_listeners`: Bind lifecycle listeners to the underlying `Runnable`.
- `with_types`: Override the input and output types of the underlying
  `Runnable`.
- `with_retry`: Bind a retry policy to the underlying `Runnable`.
- `with_fallbacks`: Bind a fallback policy to the underlying `Runnable`.

Example:
`bind`: Bind kwargs to pass to the underlying `Runnable` when running it.

```
# Create a Runnable binding that invokes the chat model with the
# additional kwarg `stop=['-']` when running it.
from langchain_openai import ChatOpenAI

model = ChatOpenAI()
model.invoke('Say "Parrot-MAGIC"', stop=["-"])  # Should return `Parrot`
# Using it the easy way via `bind` method which returns a new
# RunnableBinding
runnable_binding = model.bind(stop=["-"])
runnable_binding.invoke('Say "Parrot-MAGIC"')  # Should return `Parrot`
```

Can also be done by instantiating a `RunnableBinding` directly (not
recommended):

```
from langchain_core.runnables import RunnableBinding

runnable_binding = RunnableBinding(
    bound=model,
    kwargs={"stop": ["-"]},  # <-- Note the additional kwargs
)
runnable_binding.invoke('Say "Parrot-MAGIC"')  # Should return `Parrot`
```](/python/langchain-core/runnables/base/RunnableBinding)

## Type Aliases

[typeAlias

AnyConfigurableField](/python/langchain-core/runnables/utils/AnyConfigurableField)[typeAlias

StreamEvent](/python/langchain-core/runnables/schema/StreamEvent)[typeAlias

AsyncListener: Callable[[Run], Awaitable[None]] | Callable[[Run, RunnableConfig], Awaitable[None]]](/python/langchain-core/tracers/root_listeners/AsyncListener)[typeAlias

RunnableLike: Runnable[Input, Output] | Callable[[Input], Output] | Callable[[Input], Awaitable[Output]] | Callable[[Iterator[Input]], Iterator[Output]] | Callable[[AsyncIterator[Input]], AsyncIterator[Output]] | \_RunnableCallableSync[Input, Output] | \_RunnableCallableAsync[Input, Output] | \_RunnableCallableIterator[Input, Output] | \_RunnableCallableAsyncIterator[Input, Output] | Mapping[str, Any]](/python/langchain-core/runnables/base/RunnableLike)

## Modules

[module

beta\_decorator

Helper functions for marking parts of the LangChain API as beta.

This module was loosely adapted from matplotlib's [`_api/deprecation.py`](https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/_api/deprecation.py)
module.

Warning

This module is for internal use only. Do not use it in your own code. We may change
the API at any time with no warning.](/python/langchain-core/_api/beta_decorator)


