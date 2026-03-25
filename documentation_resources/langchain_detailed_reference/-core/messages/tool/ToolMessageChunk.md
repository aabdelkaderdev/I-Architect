<!-- Source: https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessageChunk -->

Classv1.2.21 (latest)●Since v0.1

# ToolMessageChunk

Tool Message chunk.


```
ToolMessageChunk(
  self,
  content: str | list[str | dict] | None = None,
  content_blocks: list[types.ContentBlock] | None = None,
  **kwargs: Any = {}
)
```

## Bases

`ToolMessage``BaseMessageChunk`

## Attributes

[attribute

type: Literal['ToolMessageChunk']](/python/langchain-core/messages/tool/ToolMessageChunk/type)

## Inherited from[ToolMessage](/python/langchain-core/messages/tool/ToolMessage)

### Attributes

[Atool\_call\_id: str

—

Tool call that this message is responding to.](/python/langchain-core/messages/tool/ToolMessage/tool_call_id)[Aartifact: Any

—

Artifact of the Tool execution which is not meant to be sent to the model.](/python/langchain-core/messages/tool/ToolMessage/artifact)[Astatus: Literal['success', 'error']

—

Status of the tool invocation.](/python/langchain-core/messages/tool/ToolMessage/status)[Aadditional\_kwargs: dict

—

Currently inherited from `BaseMessage`, but not used.](/python/langchain-core/messages/tool/ToolMessage/additional_kwargs)[Aresponse\_metadata: dict

—

Currently inherited from `BaseMessage`, but not used.](/python/langchain-core/messages/tool/ToolMessage/response_metadata)

### Methods

[Mcoerce\_args

—

Coerce the model arguments to the correct types.](/python/langchain-core/messages/tool/ToolMessage/coerce_args)

## Inherited from[BaseMessage](/python/langchain-core/messages/base/BaseMessage)

### Attributes

[Acontent: str | list[str | dict]

—

The contents of the message.](/python/langchain-core/messages/base/BaseMessage/content)[Aadditional\_kwargs: dict

—

Reserved for additional payload data associated with the message.](/python/langchain-core/messages/base/BaseMessage/additional_kwargs)[Aresponse\_metadata: dict

—

Examples: response headers, logprobs, token counts, model name.](/python/langchain-core/messages/base/BaseMessage/response_metadata)[Aname: str | None

—

An optional name for the message.](/python/langchain-core/messages/base/BaseMessage/name)[Aid: str | None

—

An optional unique identifier for the message.](/python/langchain-core/messages/base/BaseMessage/id)[Amodel\_config](/python/langchain-core/messages/base/BaseMessage/model_config)[Acontent\_blocks: list[types.ContentBlock]

—

Load content blocks from the message content.](/python/langchain-core/messages/base/BaseMessage/content_blocks)[Atext: TextAccessor

—

Get the text content of the message as a string.](/python/langchain-core/messages/base/BaseMessage/text)

### Methods

[Mis\_lc\_serializable

—

`BaseMessage` is serializable.](/python/langchain-core/messages/base/BaseMessage/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/messages/base/BaseMessage/get_lc_namespace)[Mpretty\_repr

—

Get a pretty representation of the message.](/python/langchain-core/messages/base/BaseMessage/pretty_repr)[Mpretty\_print

—

Print a pretty representation of the message.](/python/langchain-core/messages/base/BaseMessage/pretty_print)

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


