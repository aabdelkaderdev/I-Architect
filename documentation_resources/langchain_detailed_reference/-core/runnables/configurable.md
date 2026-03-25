<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/configurable -->

Modulev1.2.21 (latest)●Since v0.1

# configurable

`Runnable` objects that can be dynamically configured.

## Attributes

[attribute

Input](/python/langchain-core/runnables/utils/Input)[attribute

Output](/python/langchain-core/runnables/utils/Output)

## Functions

[function

ensure\_config

Ensure that a config is a dict with all keys present.](/python/langchain-core/runnables/config/ensure_config)[function

get\_config\_list

Get a list of configs from a single config or a list of configs.

It is useful for subclasses overriding batch() or abatch().](/python/langchain-core/runnables/config/get_config_list)[function

get\_executor\_for\_config

Get an executor for a config.](/python/langchain-core/runnables/config/get_executor_for_config)[function

merge\_configs

Merge multiple configs into one.](/python/langchain-core/runnables/config/merge_configs)[function

gather\_with\_concurrency

Gather coroutines with a limit on the number of concurrent coroutines.](/python/langchain-core/runnables/utils/gather_with_concurrency)[function

get\_unique\_config\_specs

Get the unique config specs from a sequence of config specs.](/python/langchain-core/runnables/utils/get_unique_config_specs)[function

prefix\_config\_spec

Prefix the id of a `ConfigurableFieldSpec`.

This is useful when a `RunnableConfigurableAlternatives` is used as a
`ConfigurableField` of another `RunnableConfigurableAlternatives`.](/python/langchain-core/runnables/configurable/prefix_config_spec)[function

make\_options\_spec

Make options spec.

Make a `ConfigurableFieldSpec` for a `ConfigurableFieldSingleOption` or
`ConfigurableFieldMultiOption`.](/python/langchain-core/runnables/configurable/make_options_spec)

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

ConfigurableField

Field that can be configured by the user.](/python/langchain-core/runnables/utils/ConfigurableField)[class

ConfigurableFieldMultiOption

Field that can be configured by the user with multiple default values.](/python/langchain-core/runnables/utils/ConfigurableFieldMultiOption)[class

ConfigurableFieldSingleOption

Field that can be configured by the user with a default value.](/python/langchain-core/runnables/utils/ConfigurableFieldSingleOption)[class

ConfigurableFieldSpec

Field that can be configured by the user. It is a specification of a field.](/python/langchain-core/runnables/utils/ConfigurableFieldSpec)[class

Graph

Graph of nodes and edges.](/python/langchain-core/runnables/graph/Graph)[class

DynamicRunnable

Serializable `Runnable` that can be dynamically configured.

A `DynamicRunnable` should be initiated using the `configurable_fields` or
`configurable_alternatives` method of a `Runnable`.](/python/langchain-core/runnables/configurable/DynamicRunnable)[class

RunnableConfigurableFields

`Runnable` that can be dynamically configured.

A `RunnableConfigurableFields` should be initiated using the
`configurable_fields` method of a `Runnable`.

Here is an example of using a `RunnableConfigurableFields` with LLMs:

```
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

model = ChatOpenAI(temperature=0).configurable_fields(
    temperature=ConfigurableField(
        id="temperature",
        name="LLM Temperature",
        description="The temperature of the LLM",
    )
)
# This creates a RunnableConfigurableFields for a chat model.

# When invoking the created RunnableSequence, you can pass in the
# value for your ConfigurableField's id which in this case
# will be change in temperature

prompt = PromptTemplate.from_template("Pick a random number above {x}")
chain = prompt | model

chain.invoke({"x": 0})
chain.invoke({"x": 0}, config={"configurable": {"temperature": 0.9}})
```

Here is an example of using a `RunnableConfigurableFields` with `HubRunnables`:

```
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI
from langchain.runnables.hub import HubRunnable

prompt = HubRunnable("rlm/rag-prompt").configurable_fields(
    owner_repo_commit=ConfigurableField(
        id="hub_commit",
        name="Hub Commit",
        description="The Hub commit to pull from",
    )
)

prompt.invoke({"question": "foo", "context": "bar"})

# Invoking prompt with `with_config` method

prompt.invoke(
    {"question": "foo", "context": "bar"},
    config={"configurable": {"hub_commit": "rlm/rag-prompt-llama"}},
)
```](/python/langchain-core/runnables/configurable/RunnableConfigurableFields)[class

StrEnum

String enum.](/python/langchain-core/runnables/configurable/StrEnum)[class

RunnableConfigurableAlternatives

`Runnable` that can be dynamically configured.

A `RunnableConfigurableAlternatives` should be initiated using the
`configurable_alternatives` method of a `Runnable` or can be
initiated directly as well.

Here is an example of using a `RunnableConfigurableAlternatives` that uses
alternative prompts to illustrate its functionality:

```
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

# This creates a RunnableConfigurableAlternatives for Prompt Runnable
# with two alternatives.
prompt = PromptTemplate.from_template(
    "Tell me a joke about {topic}"
).configurable_alternatives(
    ConfigurableField(id="prompt"),
    default_key="joke",
    poem=PromptTemplate.from_template("Write a short poem about {topic}"),
)

# When invoking the created RunnableSequence, you can pass in the
# value for your ConfigurableField's id which in this case will either be
# `joke` or `poem`.
chain = prompt | ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

# The `with_config` method brings in the desired Prompt Runnable in your
# Runnable Sequence.
chain.with_config(configurable={"prompt": "poem"}).invoke({"topic": "bears"})
```

Equivalently, you can initialize `RunnableConfigurableAlternatives` directly
and use in LCEL in the same way:

```
from langchain_core.runnables import ConfigurableField
from langchain_core.runnables.configurable import (
    RunnableConfigurableAlternatives,
)
from langchain_openai import ChatOpenAI

prompt = RunnableConfigurableAlternatives(
    which=ConfigurableField(id="prompt"),
    default=PromptTemplate.from_template("Tell me a joke about {topic}"),
    default_key="joke",
    prefix_keys=False,
    alternatives={
        "poem": PromptTemplate.from_template("Write a short poem about {topic}")
    },
)
chain = prompt | ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
chain.with_config(configurable={"prompt": "poem"}).invoke({"topic": "bears"})
```](/python/langchain-core/runnables/configurable/RunnableConfigurableAlternatives)

## Type Aliases

[typeAlias

AnyConfigurableField](/python/langchain-core/runnables/utils/AnyConfigurableField)


