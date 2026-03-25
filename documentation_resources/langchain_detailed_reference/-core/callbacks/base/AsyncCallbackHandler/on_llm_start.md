<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_llm_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_llm\_start

Run when the model starts running.

Warning

This method is called for non-chat models (regular text completion LLMs). If
you're implementing a handler for a chat model, you should use
`on_chat_model_start` instead.


```
on_llm_start(
  self,
  serialized: dict[str, Any],
  prompts: list[str],
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized LLM. |
| `prompts`\* | `list[str]` | The prompts. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `tags` | `list[str] | None` | Default:`None`  The tags. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


