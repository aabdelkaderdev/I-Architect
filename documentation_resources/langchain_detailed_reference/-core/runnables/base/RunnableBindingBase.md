<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableBindingBase -->

Classv1.2.21 (latest)●Since v0.1

# RunnableBindingBase

`Runnable` that delegates calls to another `Runnable` with a set of `**kwargs`.

Use only if creating a new `RunnableBinding` subclass with different `__init__`
args.

See documentation for `RunnableBinding` for more details.


```
RunnableBindingBase(
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

`RunnableSerializable[Input, Output]`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `bound`\* | `Runnable[Input, Output]` | The underlying `Runnable` that this `Runnable` delegates calls to. |
| `kwargs` | `Mapping[str, Any] | None` | Default:`None`  optional kwargs to pass to the underlying `Runnable`, when running the underlying `Runnable` (e.g., via `invoke`, `batch`, `transform`, or `stream` or async variants) |
| `config` | `RunnableConfig | None` | Default:`None`  optional config to bind to the underlying `Runnable`. |
| `config_factories` | `list[Callable[[RunnableConfig], RunnableConfig]] | None` | Default:`None`  optional list of config factories to apply to the config before binding to the underlying `Runnable`. |
| `custom_input_type` | `type[Input] | BaseModel | None` | Default:`None`  Specify to override the input type of the underlying `Runnable` with a custom type. |
| `custom_output_type` | `type[Output] | BaseModel | None` | Default:`None`  Specify to override the output type of the underlying `Runnable` with a custom type. |
| `**other_kwargs` | `Any` | Default:`{}`  Unpacked into the base class. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| bound | [Runnable](/python/langchain-core/runnables/base/Runnable)[[Input](/python/langchain-core/runnables/utils/Input), [Output](/python/langchain-core/runnables/utils/Output)] |
| kwargs | [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None |
| config | [RunnableConfig](/python/langchain-core/runnables/config/RunnableConfig) | None |
| config\_factories | [list](https://docs.python.org/3/library/stdtypes.html#list)[[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)[[[RunnableConfig](/python/langchain-core/runnables/config/RunnableConfig)], [RunnableConfig](/python/langchain-core/runnables/config/RunnableConfig)]] | None |
| custom\_input\_type | [type](https://docs.python.org/3/library/functions.html#type)[[Input](/python/langchain-core/runnables/utils/Input)] | [BaseModel](/python/langchain-community/vectorstores/pgembedding/BaseModel) | None |
| custom\_output\_type | [type](https://docs.python.org/3/library/functions.html#type)[[Output](/python/langchain-core/runnables/utils/Output)] | [BaseModel](/python/langchain-community/vectorstores/pgembedding/BaseModel) | None |

## Attributes

[attribute

bound: Runnable[Input, Output]

The underlying `Runnable` that this `Runnable` delegates to.](/python/langchain-core/runnables/base/RunnableBindingBase/bound)[attribute

kwargs: Mapping[str, Any]

kwargs to pass to the underlying `Runnable` when running.

For example, when the `Runnable` binding is invoked the underlying
`Runnable` will be invoked with the same input but with these additional
kwargs.](/python/langchain-core/runnables/base/RunnableBindingBase/kwargs)[attribute

config: RunnableConfig

The config to bind to the underlying `Runnable`.](/python/langchain-core/runnables/base/RunnableBindingBase/config)[attribute

config\_factories: list[Callable[[RunnableConfig], RunnableConfig]]

The config factories to bind to the underlying `Runnable`.](/python/langchain-core/runnables/base/RunnableBindingBase/config_factories)[attribute

custom\_input\_type: Any | None

Override the input type of the underlying `Runnable` with a custom type.

The type can be a Pydantic model, or a type annotation (e.g., `list[str]`).](/python/langchain-core/runnables/base/RunnableBindingBase/custom_input_type)[attribute

custom\_output\_type: Any | None

Override the output type of the underlying `Runnable` with a custom type.

The type can be a Pydantic model, or a type annotation (e.g., `list[str]`).](/python/langchain-core/runnables/base/RunnableBindingBase/custom_output_type)[attribute

model\_config](/python/langchain-core/runnables/base/RunnableBindingBase/model_config)[attribute

InputType: type[Input]](/python/langchain-core/runnables/base/RunnableBindingBase/InputType)[attribute

OutputType: type[Output]](/python/langchain-core/runnables/base/RunnableBindingBase/OutputType)[attribute

config\_specs: list[ConfigurableFieldSpec]](/python/langchain-core/runnables/base/RunnableBindingBase/config_specs)

## Methods

[method

get\_name](/python/langchain-core/runnables/base/RunnableBindingBase/get_name)[method

get\_input\_schema](/python/langchain-core/runnables/base/RunnableBindingBase/get_input_schema)[method

get\_output\_schema](/python/langchain-core/runnables/base/RunnableBindingBase/get_output_schema)[method

get\_graph](/python/langchain-core/runnables/base/RunnableBindingBase/get_graph)[method

is\_lc\_serializable

Return `True` as this class is serializable.](/python/langchain-core/runnables/base/RunnableBindingBase/is_lc_serializable)[method

get\_lc\_namespace

Get the namespace of the LangChain object.](/python/langchain-core/runnables/base/RunnableBindingBase/get_lc_namespace)[method

invoke](/python/langchain-core/runnables/base/RunnableBindingBase/invoke)[method

ainvoke](/python/langchain-core/runnables/base/RunnableBindingBase/ainvoke)[method

batch](/python/langchain-core/runnables/base/RunnableBindingBase/batch)[method

abatch](/python/langchain-core/runnables/base/RunnableBindingBase/abatch)[method

batch\_as\_completed](/python/langchain-core/runnables/base/RunnableBindingBase/batch_as_completed)[method

abatch\_as\_completed](/python/langchain-core/runnables/base/RunnableBindingBase/abatch_as_completed)[method

stream](/python/langchain-core/runnables/base/RunnableBindingBase/stream)[method

astream](/python/langchain-core/runnables/base/RunnableBindingBase/astream)[method

astream\_events](/python/langchain-core/runnables/base/RunnableBindingBase/astream_events)[method

transform](/python/langchain-core/runnables/base/RunnableBindingBase/transform)[method

atransform](/python/langchain-core/runnables/base/RunnableBindingBase/atransform)

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

[Mget\_input\_jsonschema

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

Assigns new fields to the `dict` output of this `Runnable`.](/python/langchain-core/runnables/base/Runnable/assign)[Mastream\_log

—

Stream all output from a `Runnable`, as reported to the callback system.](/python/langchain-core/runnables/base/Runnable/astream_log)[Mbind

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


