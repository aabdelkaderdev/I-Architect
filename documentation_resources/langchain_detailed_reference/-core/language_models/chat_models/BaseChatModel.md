<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel -->

Classv1.2.21 (latest)●Since v0.1

# BaseChatModel

Base class for chat models.


```
BaseChatModel(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`BaseLanguageModel[AIMessage]``ABC`

**Key imperative methods:**

Methods that actually call the underlying model.

This table provides a brief overview of the main imperative methods. Please see the base `Runnable` reference for full documentation.

| Method | Input | Output | Description |
| --- | --- | --- | --- |
| `invoke` | `str` | `list[dict | tuple | BaseMessage]` | `PromptValue` | `BaseMessage` | A single chat model call. |
| `ainvoke` | `'''` | `BaseMessage` | Defaults to running `invoke` in an async executor. |
| `stream` | `'''` | `Iterator[BaseMessageChunk]` | Defaults to yielding output of `invoke`. |
| `astream` | `'''` | `AsyncIterator[BaseMessageChunk]` | Defaults to yielding output of `ainvoke`. |
| `astream_events` | `'''` | `AsyncIterator[StreamEvent]` | Event types: `on_chat_model_start`, `on_chat_model_stream`, `on_chat_model_end`. |
| `batch` | `list[''']` | `list[BaseMessage]` | Defaults to running `invoke` in concurrent threads. |
| `abatch` | `list[''']` | `list[BaseMessage]` | Defaults to running `ainvoke` in concurrent threads. |
| `batch_as_completed` | `list[''']` | `Iterator[tuple[int, Union[BaseMessage, Exception]]]` | Defaults to running `invoke` in concurrent threads. |
| `abatch_as_completed` | `list[''']` | `AsyncIterator[tuple[int, Union[BaseMessage, Exception]]]` | Defaults to running `ainvoke` in concurrent threads. |

**Key declarative methods:**

Methods for creating another `Runnable` using the chat model.

This table provides a brief overview of the main declarative methods. Please see the reference for each method for full documentation.

| Method | Description |
| --- | --- |
| `bind_tools` | Create chat model that can call tools. |
| `with_structured_output` | Create wrapper that structures model output using schema. |
| `with_retry` | Create wrapper that retries model calls on failure. |
| `with_fallbacks` | Create wrapper that falls back to other models on failure. |
| `configurable_fields` | Specify init args of the model that can be configured at runtime via the `RunnableConfig`. |
| `configurable_alternatives` | Specify alternative models which can be swapped in at runtime via the `RunnableConfig`. |

**Creating custom chat model:**

Custom chat model implementations should inherit from this class.
Please reference the table below for information about which
methods and properties are required or optional for implementations.

| Method/Property | Description | Required |
| --- | --- | --- |
| `_generate` | Use to generate a chat result from a prompt | Required |
| `_llm_type` (property) | Used to uniquely identify the type of the model. Used for logging. | Required |
| `_identifying_params` (property) | Represent model parameterization for tracing purposes. | Optional |
| `_stream` | Use to implement streaming | Optional |
| `_agenerate` | Use to implement a native async method | Optional |
| `_astream` | Use to implement async version of `_stream` | Optional |

## Attributes

[attribute

rate\_limiter: BaseRateLimiter | None

An optional rate limiter to use for limiting the number of requests.](/python/langchain-core/language_models/chat_models/BaseChatModel/rate_limiter)[attribute

disable\_streaming: bool | Literal['tool\_calling']

Whether to disable streaming for this model.

If streaming is bypassed, then `stream`/`astream`/`astream_events` will
defer to `invoke`/`ainvoke`.

- If `True`, will always bypass streaming case.
- If `'tool_calling'`, will bypass streaming case only when the model is called
  with a `tools` keyword argument. In other words, LangChain will automatically
  switch to non-streaming behavior (`invoke`) only when the tools argument is
  provided. This offers the best of both worlds.
- If `False` (Default), will always use streaming case if available.

The main reason for this flag is that code might be written using `stream` and
a user may want to swap out a given model for another model whose implementation
does not properly support streaming.](/python/langchain-core/language_models/chat_models/BaseChatModel/disable_streaming)[attribute

output\_version: str | None

Version of `AIMessage` output format to store in message content.

`AIMessage.content_blocks` will lazily parse the contents of `content` into a
standard format. This flag can be used to additionally store the standard format
in message content, e.g., for serialization purposes.

Supported values:

- `'v0'`: provider-specific format in content (can lazily-parse with
  `content_blocks`)
- `'v1'`: standardized format in content (consistent with `content_blocks`)

Partner packages (e.g.,
[`langchain-openai`](https://pypi.org/project/langchain-openai)) can also use this
field to roll out new content formats in a backward-compatible way.](/python/langchain-core/language_models/chat_models/BaseChatModel/output_version)[attribute

profile: ModelProfile | None

Profile detailing model capabilities.

Beta feature

This is a beta feature. The format of model profiles is subject to change.

If not specified, automatically loaded from the provider package on initialization
if data is available.

Example profile data includes context window sizes, supported modalities, or support
for tool calling, structured output, and other features.](/python/langchain-core/language_models/chat_models/BaseChatModel/profile)[attribute

model\_config](/python/langchain-core/language_models/chat_models/BaseChatModel/model_config)[attribute

OutputType: Any

Get the output type for this `Runnable`.](/python/langchain-core/language_models/chat_models/BaseChatModel/OutputType)

## Methods

[method

invoke](/python/langchain-core/language_models/chat_models/BaseChatModel/invoke)[method

ainvoke](/python/langchain-core/language_models/chat_models/BaseChatModel/ainvoke)[method

stream](/python/langchain-core/language_models/chat_models/BaseChatModel/stream)[method

astream](/python/langchain-core/language_models/chat_models/BaseChatModel/astream)[method

generate

Pass a sequence of prompts to the model and return model generations.

This method should make use of batched calls for models that expose a batched
API.

Use this method when you want to:

1. Take advantage of batched calls,
2. Need more output from the model than just the top generated value,
3. Are building chains that are agnostic to the underlying language model
   type (e.g., pure text completion models vs chat models).](/python/langchain-core/language_models/chat_models/BaseChatModel/generate)[method

agenerate

Asynchronously pass a sequence of prompts to a model and return generations.

This method should make use of batched calls for models that expose a batched
API.

Use this method when you want to:

1. Take advantage of batched calls,
2. Need more output from the model than just the top generated value,
3. Are building chains that are agnostic to the underlying language model
   type (e.g., pure text completion models vs chat models).](/python/langchain-core/language_models/chat_models/BaseChatModel/agenerate)[method

generate\_prompt](/python/langchain-core/language_models/chat_models/BaseChatModel/generate_prompt)[method

agenerate\_prompt](/python/langchain-core/language_models/chat_models/BaseChatModel/agenerate_prompt)[method

dict

Return a dictionary of the LLM.](/python/langchain-core/language_models/chat_models/BaseChatModel/dict)[method

bind\_tools

Bind tools to the model.](/python/langchain-core/language_models/chat_models/BaseChatModel/bind_tools)[method

with\_structured\_output

Model wrapper that returns outputs formatted to match the given schema.](/python/langchain-core/language_models/chat_models/BaseChatModel/with_structured_output)

## Inherited from[BaseLanguageModel](/python/langchain-core/language_models/base/BaseLanguageModel)

### Attributes

[Acache: BaseCache | bool | None

—

Whether to cache the response.](/python/langchain-core/language_models/base/BaseLanguageModel/cache)[Averbose: bool

—

Whether to print out response text.](/python/langchain-core/language_models/base/BaseLanguageModel/verbose)[Acallbacks: Callbacks

—

Callbacks to add to the run trace.](/python/langchain-core/language_models/base/BaseLanguageModel/callbacks)[Atags: list[str] | None

—

Tags to add to the run trace.](/python/langchain-core/language_models/base/BaseLanguageModel/tags)[Ametadata: dict[str, Any] | None

—

Metadata to add to the run trace.](/python/langchain-core/language_models/base/BaseLanguageModel/metadata)[Acustom\_get\_token\_ids: Callable[[str], list[int]] | None

—

Optional encoder to use for counting tokens.](/python/langchain-core/language_models/base/BaseLanguageModel/custom_get_token_ids)[AInputType: TypeAlias

—

Get the input type for this `Runnable`.](/python/langchain-core/language_models/base/BaseLanguageModel/InputType)

### Methods

[Mset\_verbose

—

If verbose is `None`, set it.](/python/langchain-core/language_models/base/BaseLanguageModel/set_verbose)[Mget\_token\_ids

—

Return the ordered IDs of the tokens in a text.](/python/langchain-core/language_models/base/BaseLanguageModel/get_token_ids)[Mget\_num\_tokens

—

Get the number of tokens present in the text.](/python/langchain-core/language_models/base/BaseLanguageModel/get_num_tokens)[Mget\_num\_tokens\_from\_messages

—

Get the number of tokens in the messages.](/python/langchain-core/language_models/base/BaseLanguageModel/get_num_tokens_from_messages)

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

Input type.](/python/langchain-core/runnables/base/Runnable/InputType)[Ainput\_schema: type[BaseModel]

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

Assigns new fields to the `dict` output of this `Runnable`.](/python/langchain-core/runnables/base/Runnable/assign)[Mbatch

—

Default implementation runs invoke in parallel using a thread pool executor.](/python/langchain-core/runnables/base/Runnable/batch)[Mbatch\_as\_completed

—

Run `invoke` in parallel on a list of inputs.](/python/langchain-core/runnables/base/Runnable/batch_as_completed)[Mabatch

—

Default implementation runs `ainvoke` in parallel using `asyncio.gather`.](/python/langchain-core/runnables/base/Runnable/abatch)[Mabatch\_as\_completed

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


