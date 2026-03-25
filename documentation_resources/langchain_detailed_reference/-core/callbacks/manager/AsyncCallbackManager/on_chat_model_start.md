<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_chat_model_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chat\_model\_start

Async run when LLM starts running.


```
on_chat_model_start(
  self,
  serialized: dict[str, Any],
  messages: list[list[BaseMessage]],
  run_id: UUID | None = None,
  **kwargs: Any = {}
) -> list[AsyncCallbackManagerForLLMRun]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized LLM. |
| `messages`\* | `list[list[BaseMessage]]` | The list of messages. |
| `run_id` | `UUID | None` | Default:`None`  The ID of the run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


