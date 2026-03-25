<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/configurable/RunnableConfigurableAlternatives -->

Classv1.2.21 (latest)●Since v0.1

# RunnableConfigurableAlternatives

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
```


```
RunnableConfigurableAlternatives(
  self,
  *args: Any = (),
  **kwargs: Any = {}
)
```

## Bases

`DynamicRunnable[Input, Output]`

## Attributes

[attribute

which: ConfigurableField

The `ConfigurableField` to use to choose between alternatives.](/python/langchain-core/runnables/configurable/RunnableConfigurableAlternatives/which)[attribute

alternatives: dict[str, Runnable[Input, Output] | Callable[[], Runnable[Input, Output]]]

The alternatives to choose from.](/python/langchain-core/runnables/configurable/RunnableConfigurableAlternatives/alternatives)[attribute

default\_key: str

The enum value to use for the default option.](/python/langchain-core/runnables/configurable/RunnableConfigurableAlternatives/default_key)[attribute

prefix\_keys: bool

Whether to prefix configurable fields of each alternative with a namespace
of the form <which.id>==<alternative\_key>, e.g. a key named "temperature" used by
the alternative named "gpt3" becomes "model==gpt3/temperature".](/python/langchain-core/runnables/configurable/RunnableConfigurableAlternatives/prefix_keys)[attribute

config\_specs: list[ConfigurableFieldSpec]](/python/langchain-core/runnables/configurable/RunnableConfigurableAlternatives/config_specs)

## Methods

[method

configurable\_fields](/python/langchain-core/runnables/configurable/RunnableConfigurableAlternatives/configurable_fields)

## Inherited from[DynamicRunnable](/python/langchain-core/runnables/configurable/DynamicRunnable)

### Attributes

[Adefault: RunnableSerializable[Input, Output]

—

The default `Runnable` to use.](/python/langchain-core/runnables/configurable/DynamicRunnable/default)[Aconfig: RunnableConfig | None

—

The configuration to use.](/python/langchain-core/runnables/configurable/DynamicRunnable/config)[Amodel\_config](/python/langchain-core/runnables/configurable/DynamicRunnable/model_config)[AInputType: type[Input]](/python/langchain-core/runnables/configurable/DynamicRunnable/InputType)[AOutputType: type[Output]](/python/langchain-core/runnables/configurable/DynamicRunnable/OutputType)

### Methods

[Mis\_lc\_serializable

—

Return `True` as this class is serializable.](/python/langchain-core/runnables/configurable/DynamicRunnable/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/runnables/configurable/DynamicRunnable/get_lc_namespace)[Mget\_input\_schema](/python/langchain-core/runnables/configurable/DynamicRunnable/get_input_schema)[Mget\_output\_schema](/python/langchain-core/runnables/configurable/DynamicRunnable/get_output_schema)[Mget\_graph](/python/langchain-core/runnables/configurable/DynamicRunnable/get_graph)[Mwith\_config](/python/langchain-core/runnables/configurable/DynamicRunnable/with_config)[Mprepare

—

Prepare the `Runnable` for invocation.](/python/langchain-core/runnables/configurable/DynamicRunnable/prepare)[Minvoke](/python/langchain-core/runnables/configurable/DynamicRunnable/invoke)[Mainvoke](/python/langchain-core/runnables/configurable/DynamicRunnable/ainvoke)[Mbatch](/python/langchain-core/runnables/configurable/DynamicRunnable/batch)[Mabatch](/python/langchain-core/runnables/configurable/DynamicRunnable/abatch)[Mstream](/python/langchain-core/runnables/configurable/DynamicRunnable/stream)[Mastream](/python/langchain-core/runnables/configurable/DynamicRunnable/astream)[Mtransform](/python/langchain-core/runnables/configurable/DynamicRunnable/transform)[Matransform](/python/langchain-core/runnables/configurable/DynamicRunnable/atransform)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)

### Attributes

[Aname: str | None

—

The name of the `Runnable`.](/python/langchain-core/runnables/base/RunnableSerializable/name)[Amodel\_config](/python/langchain-core/runnables/base/RunnableSerializable/model_config)

### Methods

[Mto\_json

—

Serialize the `Runnable` to JSON.](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_alternatives

—

Configure alternatives for `Runnable` objects that can be set at runtime.](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)

### Attributes

[Alc\_secrets: dict[str, str]

—

A map of constructor argument names to secret ids.](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes: dict

—

List of attribute names that should be included in the serialized kwargs.](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable

—

Is this class serializable?](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id

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

The name of the `Runnable`. Used for debugging and tracing.](/python/langchain-core/runnables/base/Runnable/name)[AInputType: type[Input]

—

Input type.](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType: type[Output]

—

Output Type.](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema: type[BaseModel]

—

The type of input this `Runnable` accepts specified as a Pydantic model.](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema: type[BaseModel]

—

Output schema.](/python/langchain-core/runnables/base/Runnable/output_schema)

### Methods

[Mget\_name

—

Get the name of the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema

—

Get a Pydantic model that can be used to validate input to the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema

—

Get a JSON schema that represents the input to the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema

—

Get a Pydantic model that can be used to validate output to the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema

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

Assigns new fields to the `dict` output of this `Runnable`.](/python/langchain-core/runnables/base/Runnable/assign)[Minvoke

—

Transform a single input into an output.](/python/langchain-core/runnables/base/Runnable/invoke)[Mainvoke

—

Transform a single input into an output.](/python/langchain-core/runnables/base/Runnable/ainvoke)[Mbatch

—

Default implementation runs invoke in parallel using a thread pool executor.](/python/langchain-core/runnables/base/Runnable/batch)[Mbatch\_as\_completed

—

Run `invoke` in parallel on a list of inputs.](/python/langchain-core/runnables/base/Runnable/batch_as_completed)[Mabatch

—

Default implementation runs `ainvoke` in parallel using `asyncio.gather`.](/python/langchain-core/runnables/base/Runnable/abatch)[Mabatch\_as\_completed

—

Run `ainvoke` in parallel on a list of inputs.](/python/langchain-core/runnables/base/Runnable/abatch_as_completed)[Mstream

—

Default implementation of `stream`, which calls `invoke`.](/python/langchain-core/runnables/base/Runnable/stream)[Mastream

—

Default implementation of `astream`, which calls `ainvoke`.](/python/langchain-core/runnables/base/Runnable/astream)[Mastream\_log

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


