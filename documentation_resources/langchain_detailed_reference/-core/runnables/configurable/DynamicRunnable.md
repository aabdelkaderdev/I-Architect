<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/configurable/DynamicRunnable -->

Classv1.2.21 (latest)●Since v0.1

# DynamicRunnable

Serializable `Runnable` that can be dynamically configured.

A `DynamicRunnable` should be initiated using the `configurable_fields` or
`configurable_alternatives` method of a `Runnable`.


```
DynamicRunnable(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`RunnableSerializable[Input, Output]`

## Attributes

[attribute

default: RunnableSerializable[Input, Output]

The default `Runnable` to use.](/python/langchain-core/runnables/configurable/DynamicRunnable/default)[attribute

config: RunnableConfig | None

The configuration to use.](/python/langchain-core/runnables/configurable/DynamicRunnable/config)[attribute

model\_config](/python/langchain-core/runnables/configurable/DynamicRunnable/model_config)[attribute

InputType: type[Input]](/python/langchain-core/runnables/configurable/DynamicRunnable/InputType)[attribute

OutputType: type[Output]](/python/langchain-core/runnables/configurable/DynamicRunnable/OutputType)

## Methods

[method

is\_lc\_serializable

Return `True` as this class is serializable.](/python/langchain-core/runnables/configurable/DynamicRunnable/is_lc_serializable)[method

get\_lc\_namespace

Get the namespace of the LangChain object.](/python/langchain-core/runnables/configurable/DynamicRunnable/get_lc_namespace)[method

get\_input\_schema](/python/langchain-core/runnables/configurable/DynamicRunnable/get_input_schema)[method

get\_output\_schema](/python/langchain-core/runnables/configurable/DynamicRunnable/get_output_schema)[method

get\_graph](/python/langchain-core/runnables/configurable/DynamicRunnable/get_graph)[method

with\_config](/python/langchain-core/runnables/configurable/DynamicRunnable/with_config)[method

prepare

Prepare the `Runnable` for invocation.](/python/langchain-core/runnables/configurable/DynamicRunnable/prepare)[method

invoke](/python/langchain-core/runnables/configurable/DynamicRunnable/invoke)[method

ainvoke](/python/langchain-core/runnables/configurable/DynamicRunnable/ainvoke)[method

batch](/python/langchain-core/runnables/configurable/DynamicRunnable/batch)[method

abatch](/python/langchain-core/runnables/configurable/DynamicRunnable/abatch)[method

stream](/python/langchain-core/runnables/configurable/DynamicRunnable/stream)[method

astream](/python/langchain-core/runnables/configurable/DynamicRunnable/astream)[method

transform](/python/langchain-core/runnables/configurable/DynamicRunnable/transform)[method

atransform](/python/langchain-core/runnables/configurable/DynamicRunnable/atransform)

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

Output schema.](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs: list[ConfigurableFieldSpec]

—

List configurable fields for this `Runnable`.](/python/langchain-core/runnables/base/Runnable/config_specs)

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

Get a JSON schema that represents the config of the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_config_jsonschema)[Mget\_prompts

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

Generate a stream of events.](/python/langchain-core/runnables/base/Runnable/astream_events)[Mbind

—

Bind arguments to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/bind)[Mwith\_listeners

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


