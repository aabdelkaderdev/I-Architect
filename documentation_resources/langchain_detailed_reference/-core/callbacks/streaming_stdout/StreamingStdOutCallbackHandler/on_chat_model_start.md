<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/streaming_stdout/StreamingStdOutCallbackHandler/on_chat_model_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chat\_model\_start

Run when LLM starts running.


```
on_chat_model_start(
  self,
  serialized: dict[str, Any],
  messages: list[list[BaseMessage]],
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized LLM. |
| `messages`\* | `list[list[BaseMessage]]` | The messages to run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


