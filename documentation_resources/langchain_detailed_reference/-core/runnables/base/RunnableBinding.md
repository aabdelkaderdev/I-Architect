<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableBinding -->

Classv1.2.21 (latest)●Since v0.1

# RunnableBinding

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
```


```
RunnableBinding(
  self,
  *,
  bound: Runnable[Input, Output],
  kwargs: Mapping[str, Any] | None = None,
  config: RunnableConfig | None = None,
  config_factories: list[Callable[[RunnableConfig], RunnableConfig]] | None = None,
  custom_input_type: type[Input] | BaseModel | None = None,
  custom_output_type: type[Output] | BaseModel | None = None,
  **other_kwargs: Any = {}
)
```

## Bases

`RunnableBindingBase[Input, Output]`

## Methods

[method

bind

Bind additional kwargs to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/RunnableBinding/bind)[method

with\_config](/python/langchain-core/runnables/base/RunnableBinding/with_config)[method

with\_listeners

Bind lifecycle listeners to a `Runnable`, returning a new `Runnable`.

The `Run` object contains information about the run, including its `id`,
`type`, `input`, `output`, `error`, `start_time`, `end_time`, and
any tags or metadata added to the run.](/python/langchain-core/runnables/base/RunnableBinding/with_listeners)[method

with\_types](/python/langchain-core/runnables/base/RunnableBinding/with_types)[method

with\_retry](/python/langchain-core/runnables/base/RunnableBinding/with_retry)

## Inherited from[RunnableBindingBase](/python/langchain-core/runnables/base/RunnableBindingBase)

### Attributes

[Abound: Runnable[Input, Output]

—

The underlying `Runnable` that this `Runnable` delegates to.](/python/langchain-core/runnables/base/RunnableBindingBase/bound)[Akwargs: Mapping[str, Any]

—

kwargs to pass to the underlying `Runnable` when running.](/python/langchain-core/runnables/base/RunnableBindingBase/kwargs)[Aconfig: RunnableConfig

—

The config to bind to the underlying `Runnable`.](/python/langchain-core/runnables/base/RunnableBindingBase/config)[Aconfig\_factories: list[Callable[[RunnableConfig], RunnableConfig]]

—

The config factories to bind to the underlying `Runnable`.](/python/langchain-core/runnables/base/RunnableBindingBase/config_factories)[Acustom\_input\_type: Any | None

—

Override the input type of the underlying `Runnable` with a custom type.](/python/langchain-core/runnables/base/RunnableBindingBase/custom_input_type)[Acustom\_output\_type: Any | None

—

Override the output type of the underlying `Runnable` with a custom type.](/python/langchain-core/runnables/base/RunnableBindingBase/custom_output_type)[Amodel\_config](/python/langchain-core/runnables/base/RunnableBindingBase/model_config)[AInputType: type[Input]](/python/langchain-core/runnables/base/RunnableBindingBase/InputType)[AOutputType: type[Output]](/python/langchain-core/runnables/base/RunnableBindingBase/OutputType)[Aconfig\_specs: list[ConfigurableFieldSpec]](/python/langchain-core/runnables/base/RunnableBindingBase/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/RunnableBindingBase/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/RunnableBindingBase/get_input_schema)[Mget\_output\_schema](/python/langchain-core/runnables/base/RunnableBindingBase/get_output_schema)[Mget\_graph](/python/langchain-core/runnables/base/RunnableBindingBase/get_graph)[Mis\_lc\_serializable

—

Return `True` as this class is serializable.](/python/langchain-core/runnables/base/RunnableBindingBase/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/runnables/base/RunnableBindingBase/get_lc_namespace)[Minvoke](/python/langchain-core/runnables/base/RunnableBindingBase/invoke)[Mainvoke](/python/langchain-core/runnables/base/RunnableBindingBase/ainvoke)[Mbatch](/python/langchain-core/runnables/base/RunnableBindingBase/batch)[Mabatch](/python/langchain-core/runnables/base/RunnableBindingBase/abatch)[Mbatch\_as\_completed](/python/langchain-core/runnables/base/RunnableBindingBase/batch_as_completed)[Mabatch\_as\_completed](/python/langchain-core/runnables/base/RunnableBindingBase/abatch_as_completed)[Mstream](/python/langchain-core/runnables/base/RunnableBindingBase/stream)[Mastream](/python/langchain-core/runnables/base/RunnableBindingBase/astream)[Mastream\_events](/python/langchain-core/runnables/base/RunnableBindingBase/astream_events)[Mtransform](/python/langchain-core/runnables/base/RunnableBindingBase/transform)[Matransform](/python/langchain-core/runnables/base/RunnableBindingBase/atransform)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)

### Attributes

[Aname: str | None

—

The name of the `Runnable`.](/python/langchain-core/runnables/base/RunnableSerializable/name)[Amodel\_config](/python/langchain-core/runnables/base/RunnableSerializable/model_config)

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

Output schema.](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs: list[ConfigurableFieldSpec]

—

List configurable fields for this `Runnable`.](/python/langchain-core/runnables/base/Runnable/config_specs)

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

Transform inputs to outputs.](/python/langchain-core/runnables/base/Runnable/atransform)[Mwith\_alisteners

—

Bind async lifecycle listeners to a `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_alisteners)[Mmap

—

Return a new `Runnable` that maps a list of inputs to a list of outputs.](/python/langchain-core/runnables/base/Runnable/map)[Mwith\_fallbacks

—

Add fallbacks to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_fallbacks)[Mas\_tool

—

Create a `BaseTool` from a `Runnable`.](/python/langchain-core/runnables/base/Runnable/as_tool)


