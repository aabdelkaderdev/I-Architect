<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/structured/StructuredPrompt/from_messages_and_schema -->

Methodv1.2.21 (latest)●Since v0.1

# from\_messages\_and\_schema

Create a chat prompt template from a variety of message formats.


```
from_messages_and_schema(
  cls,
  messages: Sequence[MessageLikeRepresentation],
  schema: dict | type,
  **kwargs: Any = {}
) -> ChatPromptTemplate
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `messages`\* | `Sequence[MessageLikeRepresentation]` | Sequence of message representations.  A message can be represented using the following formats:   1. `BaseMessagePromptTemplate` 2. `BaseMessage` 3. 2-tuple of `(message type, template)`; e.g.,    `("human", "{user_input}")` 4. 2-tuple of `(message class, template)` 5. A string which is shorthand for `("human", template)`; e.g.,    `"{user_input}"` |
| `schema`\* | `dict | type` | A dictionary representation of function call, or a Pydantic model. |
| `**kwargs` | `Any` | Default:`{}`  Any additional kwargs to pass through to `ChatModel.with_structured_output(schema, **kwargs)`. |


