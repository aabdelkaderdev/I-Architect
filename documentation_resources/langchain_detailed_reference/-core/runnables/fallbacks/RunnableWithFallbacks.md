<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks -->

Classv1.2.21 (latest)●Since v0.1

# RunnableWithFallbacks

`Runnable` that can fallback to other `Runnable` objects if it fails.

External APIs (e.g., APIs for a language model) may at times experience
degraded performance or even downtime.

In these cases, it can be useful to have a fallback `Runnable` that can be
used in place of the original `Runnable` (e.g., fallback to another LLM provider).

Fallbacks can be defined at the level of a single `Runnable`, or at the level
of a chain of `Runnable`s. Fallbacks are tried in order until one succeeds or
all fail.

While you can instantiate a `RunnableWithFallbacks` directly, it is usually
more convenient to use the `with_fallbacks` method on a `Runnable`.


```
RunnableWithFallbacks(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`RunnableSerializable[Input, Output]`

**Example:**

```
from langchain_core.chat_models.openai import ChatOpenAI
from langchain_core.chat_models.anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-3-haiku-20240307").with_fallbacks(
    [ChatOpenAI(model="gpt-3.5-turbo-0125")]
)
# Will usually use ChatAnthropic, but fallback to ChatOpenAI
# if ChatAnthropic fails.
model.invoke("hello")

# And you can also use fallbacks at the level of a chain.
# Here if both LLM providers fail, we'll fallback to a good hardcoded
# response.

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parser import StrOutputParser
from langchain_core.runnables import RunnableLambda

def when_all_is_lost(inputs):
    return (
        "Looks like our LLM providers are down. "
        "Here's a nice 🦜️ emoji for you instead."
    )

chain_with_fallback = (
    PromptTemplate.from_template("Tell me a joke about {topic}")
    | model
    | StrOutputParser()
).with_fallbacks([RunnableLambda(when_all_is_lost)])
```

## Attributes

[attribute

runnable: Runnable[Input, Output]

The `Runnable` to run first.](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/runnable)[attribute

fallbacks: Sequence[Runnable[Input, Output]]

A sequence of fallbacks to try.](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/fallbacks)[attribute

exceptions\_to\_handle: tuple[type[BaseException], ...]

The exceptions on which fallbacks should be tried.

Any exception that is not a subclass of these exceptions will be raised immediately.](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/exceptions_to_handle)[attribute

exception\_key: str | None

If `string` is specified then handled exceptions will be passed to fallbacks as
part of the input under the specified key.

If `None`, exceptions will not be passed to fallbacks.

If used, the base `Runnable` and its fallbacks must accept a dictionary as input.](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/exception_key)[attribute

model\_config](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/model_config)[attribute

InputType: type[Input]](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/InputType)[attribute

OutputType: type[Output]](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/OutputType)[attribute

config\_specs: list[ConfigurableFieldSpec]](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/config_specs)[attribute

runnables: Iterator[Runnable[Input, Output]]

Iterator over the `Runnable` and its fallbacks.](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/runnables)

## Methods

[method

get\_input\_schema](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/get_input_schema)[method

get\_output\_schema](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/get_output_schema)[method

is\_lc\_serializable

Return `True` as this class is serializable.](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/is_lc_serializable)[method

get\_lc\_namespace

Get the namespace of the LangChain object.](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/get_lc_namespace)[method

invoke](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/invoke)[method

ainvoke](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/ainvoke)[method

batch](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/batch)[method

abatch](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/abatch)[method

stream](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/stream)[method

astream](/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/astream)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)

### Attributes

[Aname: str | None

—

The name of the `Runnable`.](/python/langchain-core/runnables/base/RunnableSerializable/name)

### Methods

[Mto\_json

—

Serialize the `Runnable` to JSON.](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields

—

Configure particular `Runnable` fields at runtime.](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives

—

Configure alternatives for `Runnable` objects that can be set at runtime.](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)

### Attributes

[Alc\_secrets: dict[str, str]

—

A map of constructor argument names to secret ids.](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes: dict

—

List of attribute names that should be included in the serialized kwargs.](/python/langchain-core/load/serializable/Serializable/lc_attributes)

### Methods

[Mlc\_id

—

Return a unique identifier for this class for serialization purposes.](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json

—

Serialize the object to JSON.](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented

—

Serialize a "not implemented" object.](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)

### Attributes

[Aname: str | None

—

The name of the `Runnable`. Used for debugging and tracing.](/python/langchain-core/runnables/base/Runnable/name)[Ainput\_schema: type[BaseModel]

—

The type of input this `Runnable` accepts specified as a Pydantic model.](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema: type[BaseModel]

—

Output schema.](/python/langchain-core/runnables/base/Runnable/output_schema)

### Methods

[Mget\_name

—

Get the name of the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_jsonschema

—

Get a JSON schema that represents the input to the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_jsonschema

—

Get a JSON schema that represents the output of the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema

—

The type of config this `Runnable` accepts specified as a Pydantic model.](/python/langchain-core/runnables/base/Runnable/config_schema)[Mget\_config\_jsonschema

—

Get a JSON schema that represents the config of the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_config_jsonschema)[Mget\_graph

—

Return a graph representation of this `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_graph)[Mget\_prompts

—

Return a list of prompts used by this `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_prompts)[Mpipe

—

Pipe `Runnable` objects.](/python/langchain-core/runnables/base/Runnable/pipe)[Mpick

—

Pick keys from the output `dict` of this `Runnable`.](/python/langchain-core/runnables/base/Runnable/pick)[Massign

—

Assigns new fields to the `dict` output of this `Runnable`.](/python/langchain-core/runnables/base/Runnable/assign)[Mbatch\_as\_completed

—

Run `invoke` in parallel on a list of inputs.](/python/langchain-core/runnables/base/Runnable/batch_as_completed)[Mabatch\_as\_completed

—

Run `ainvoke` in parallel on a list of inputs.](/python/langchain-core/runnables/base/Runnable/abatch_as_completed)[Mastream\_log

—

Stream all output from a `Runnable`, as reported to the callback system.](/python/langchain-core/runnables/base/Runnable/astream_log)[Mastream\_events

—

Generate a stream of events.](/python/langchain-core/runnables/base/Runnable/astream_events)[Mtransform

—

Transform inputs to outputs.](/python/langchain-core/runnables/base/Runnable/transform)[Matransform

—

Transform inputs to outputs.](/python/langchain-core/runnables/base/Runnable/atransform)[Mbind

—

Bind arguments to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/bind)[Mwith\_config

—

Bind config to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_config)[Mwith\_listeners

—

Bind lifecycle listeners to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_listeners)[Mwith\_alisteners

—

Bind async lifecycle listeners to a `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_alisteners)[Mwith\_types

—

Bind input and output types to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_types)[Mwith\_retry

—

Create a new `Runnable` that retries the original `Runnable` on exceptions.](/python/langchain-core/runnables/base/Runnable/with_retry)[Mmap

—

Return a new `Runnable` that maps a list of inputs to a list of outputs.](/python/langchain-core/runnables/base/Runnable/map)[Mwith\_fallbacks

—

Add fallbacks to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_fallbacks)[Mas\_tool

—

Create a `BaseTool` from a `Runnable`.](/python/langchain-core/runnables/base/Runnable/as_tool)


