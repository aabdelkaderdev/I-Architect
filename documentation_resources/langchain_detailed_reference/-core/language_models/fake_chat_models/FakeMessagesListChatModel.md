<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/fake_chat_models/FakeMessagesListChatModel -->

Classv1.2.21 (latest)●Since v0.1

# FakeMessagesListChatModel

Fake chat model for testing purposes.


```
FakeMessagesListChatModel(
  self,
  *args: Any = (),
  **kwargs: Any = {}
)
```

## Bases

`BaseChatModel`

## Attributes

[attribute

responses: list[BaseMessage]

List of responses to **cycle** through in order.](/python/langchain-core/language_models/fake_chat_models/FakeMessagesListChatModel/responses)[attribute

sleep: float | None

Sleep time in seconds between responses.](/python/langchain-core/language_models/fake_chat_models/FakeMessagesListChatModel/sleep)[attribute

i: int

Internally incremented after every model invocation.](/python/langchain-core/language_models/fake_chat_models/FakeMessagesListChatModel/i)

## Inherited from[BaseChatModel](/python/langchain-core/language_models/chat_models/BaseChatModel)

### Attributes

[Arate\_limiter: BaseRateLimiter | None

—

An optional rate limiter to use for limiting the number of requests.](/python/langchain-core/language_models/chat_models/BaseChatModel/rate_limiter)[Adisable\_streaming: bool | Literal['tool\_calling']

—

Whether to disable streaming for this model.](/python/langchain-core/language_models/chat_models/BaseChatModel/disable_streaming)[Aoutput\_version: str | None

—

Version of `AIMessage` output format to store in message content.](/python/langchain-core/language_models/chat_models/BaseChatModel/output_version)[Aprofile: ModelProfile | None

—

Profile detailing model capabilities.](/python/langchain-core/language_models/chat_models/BaseChatModel/profile)[Amodel\_config](/python/langchain-core/language_models/chat_models/BaseChatModel/model_config)[AOutputType: Any

—

Get the output type for this `Runnable`.](/python/langchain-core/language_models/chat_models/BaseChatModel/OutputType)

### Methods

[Minvoke](/python/langchain-core/language_models/chat_models/BaseChatModel/invoke)[Mainvoke](/python/langchain-core/language_models/chat_models/BaseChatModel/ainvoke)[Mstream](/python/langchain-core/language_models/chat_models/BaseChatModel/stream)[Mastream](/python/langchain-core/language_models/chat_models/BaseChatModel/astream)[Mgenerate

—

Pass a sequence of prompts to the model and return model generations.](/python/langchain-core/language_models/chat_models/BaseChatModel/generate)[Magenerate

—

Asynchronously pass a sequence of prompts to a model and return generations.](/python/langchain-core/language_models/chat_models/BaseChatModel/agenerate)[Mgenerate\_prompt](/python/langchain-core/language_models/chat_models/BaseChatModel/generate_prompt)[Magenerate\_prompt](/python/langchain-core/language_models/chat_models/BaseChatModel/agenerate_prompt)[Mdict

—

Return a dictionary of the LLM.](/python/langchain-core/language_models/chat_models/BaseChatModel/dict)[Mbind\_tools

—

Bind tools to the model.](/python/langchain-core/language_models/chat_models/BaseChatModel/bind_tools)[Mwith\_structured\_output

—

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

Optional encoder to use for counting tokens.](/python/langchain-core/language_models/base/BaseLanguageModel/custom_get_token_ids)[Amodel\_config](/python/langchain-core/language_models/base/BaseLanguageModel/model_config)[AInputType: TypeAlias

—

Get the input type for this `Runnable`.](/python/langchain-core/language_models/base/BaseLanguageModel/InputType)

### Methods

[Mset\_verbose

—

If verbose is `None`, set it.](/python/langchain-core/language_models/base/BaseLanguageModel/set_verbose)[Mgenerate\_prompt

—

Pass a sequence of prompts to the model and return model generations.](/python/langchain-core/language_models/base/BaseLanguageModel/generate_prompt)[Magenerate\_prompt

—

Asynchronously pass a sequence of prompts and return model generations.](/python/langchain-core/language_models/base/BaseLanguageModel/agenerate_prompt)[Mwith\_structured\_output

—

Not implemented on this class.](/python/langchain-core/language_models/base/BaseLanguageModel/with_structured_output)[Mget\_token\_ids

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


