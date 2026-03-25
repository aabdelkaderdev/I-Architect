<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/string/StringPromptTemplate -->

Classv1.2.21 (latest)●Since v0.1

# StringPromptTemplate

String prompt that exposes the format method, returning a prompt.


```
StringPromptTemplate(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`BasePromptTemplate``ABC`

## Methods

[method

get\_lc\_namespace

Get the namespace of the LangChain object.](/python/langchain-core/prompts/string/StringPromptTemplate/get_lc_namespace)[method

format\_prompt

Format the prompt with the inputs.](/python/langchain-core/prompts/string/StringPromptTemplate/format_prompt)[method

aformat\_prompt

Async format the prompt with the inputs.](/python/langchain-core/prompts/string/StringPromptTemplate/aformat_prompt)[method

format](/python/langchain-core/prompts/string/StringPromptTemplate/format)[method

pretty\_repr

Get a pretty representation of the prompt.](/python/langchain-core/prompts/string/StringPromptTemplate/pretty_repr)[method

pretty\_print

Print a pretty representation of the prompt.](/python/langchain-core/prompts/string/StringPromptTemplate/pretty_print)

## Inherited from[BasePromptTemplate](/python/langchain-core/prompts/base/BasePromptTemplate)

### Attributes

[Ainput\_variables: list[str]

—

A list of the names of the variables whose values are required as inputs to the](/python/langchain-core/prompts/base/BasePromptTemplate/input_variables)[Aoptional\_variables: list[str]

—

A list of the names of the variables for placeholder or `MessagePlaceholder` that](/python/langchain-core/prompts/base/BasePromptTemplate/optional_variables)[Ainput\_types: builtins.dict[str, Any]

—

A dictionary of the types of the variables the prompt template expects.](/python/langchain-core/prompts/base/BasePromptTemplate/input_types)[Aoutput\_parser: BaseOutputParser | None

—

How to parse the output of calling an LLM on this formatted prompt.](/python/langchain-core/prompts/base/BasePromptTemplate/output_parser)[Apartial\_variables: Mapping[str, Any]

—

A dictionary of the partial variables the prompt template carries.](/python/langchain-core/prompts/base/BasePromptTemplate/partial_variables)[Ametadata: builtins.dict[str, Any] | None

—

Metadata to be used for tracing.](/python/langchain-core/prompts/base/BasePromptTemplate/metadata)[Atags: list[str] | None

—

Tags to be used for tracing.](/python/langchain-core/prompts/base/BasePromptTemplate/tags)[Amodel\_config](/python/langchain-core/prompts/base/BasePromptTemplate/model_config)[AOutputType: Any

—

Return the output type of the prompt.](/python/langchain-core/prompts/base/BasePromptTemplate/OutputType)

### Methods

[Mvalidate\_variable\_names

—

Validate variable names do not include restricted names.](/python/langchain-core/prompts/base/BasePromptTemplate/validate_variable_names)[Mis\_lc\_serializable

—

Return `True` as this class is serializable.](/python/langchain-core/prompts/base/BasePromptTemplate/is_lc_serializable)[Mget\_input\_schema

—

Get the input schema for the prompt.](/python/langchain-core/prompts/base/BasePromptTemplate/get_input_schema)[Minvoke

—

Invoke the prompt.](/python/langchain-core/prompts/base/BasePromptTemplate/invoke)[Mainvoke

—

Async invoke the prompt.](/python/langchain-core/prompts/base/BasePromptTemplate/ainvoke)[Mpartial

—

Return a partial of the prompt template.](/python/langchain-core/prompts/base/BasePromptTemplate/partial)[Maformat

—

Async format the prompt with the inputs.](/python/langchain-core/prompts/base/BasePromptTemplate/aformat)[Mdict

—

Return dictionary representation of prompt.](/python/langchain-core/prompts/base/BasePromptTemplate/dict)[Msave

—

Save the prompt.](/python/langchain-core/prompts/base/BasePromptTemplate/save)

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

Is this class serializable?](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mlc\_id

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


