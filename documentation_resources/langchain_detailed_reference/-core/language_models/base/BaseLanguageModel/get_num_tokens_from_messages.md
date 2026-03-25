<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/base/BaseLanguageModel/get_num_tokens_from_messages -->

Methodv1.2.21 (latest)●Since v0.1

# get\_num\_tokens\_from\_messages

Get the number of tokens in the messages.

Useful for checking if an input fits in a model's context window.

This should be overridden by model-specific implementations to provide accurate
token counts via model-specific tokenizers.

Note

- The base implementation of `get_num_tokens_from_messages` ignores tool
  schemas.
- The base implementation of `get_num_tokens_from_messages` adds additional
  prefixes to messages in represent user roles, which will add to the
  overall token count. Model-specific implementations may choose to
  handle this differently.


```
get_num_tokens_from_messages(
  self,
  messages: list[BaseMessage],
  tools: Sequence | None = None
) -> int
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `messages`\* | `list[BaseMessage]` | The message inputs to tokenize. |
| `tools` | `Sequence | None` | Default:`None`  If provided, sequence of dict, `BaseModel`, function, or `BaseTool` objects to be converted to tool schemas. |


