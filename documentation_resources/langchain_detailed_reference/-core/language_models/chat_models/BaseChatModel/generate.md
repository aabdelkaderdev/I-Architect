<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/generate -->

Methodv1.2.21 (latest)●Since v0.1

# generate

Pass a sequence of prompts to the model and return model generations.

This method should make use of batched calls for models that expose a batched
API.

Use this method when you want to:

1. Take advantage of batched calls,
2. Need more output from the model than just the top generated value,
3. Are building chains that are agnostic to the underlying language model
   type (e.g., pure text completion models vs chat models).


```
generate(
  self,
  messages: list[list[BaseMessage]],
  stop: list[str] | None = None,
  callbacks: Callbacks = None,
  *,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  run_name: str | None = None,
  run_id: uuid.UUID | None = None,
  **kwargs: Any = {}
) -> LLMResult
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `messages`\* | `list[list[BaseMessage]]` | List of list of messages. |
| `stop` | `list[str] | None` | Default:`None`  Stop words to use when generating.  Model output is cut off at the first occurrence of any of these substrings. |
| `callbacks` | `Callbacks` | Default:`None`  `Callbacks` to pass through.  Used for executing additional functionality, such as logging or streaming, throughout generation. |
| `tags` | `list[str] | None` | Default:`None`  The tags to apply. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata to apply. |
| `run_name` | `str | None` | Default:`None`  The name of the run. |
| `run_id` | `uuid.UUID | None` | Default:`None`  The ID of the run. |
| `**kwargs` | `Any` | Default:`{}`  Arbitrary additional keyword arguments.  These are usually passed to the model provider API call. |


