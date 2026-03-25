<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_chat_model_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chat\_model\_start

Start a trace for a chat model run.


```
on_chat_model_start(
  self,
  serialized: dict[str, Any],
  messages: list[list[BaseMessage]],
  *,
  run_id: UUID,
  tags: list[str] | None = None,
  parent_run_id: UUID | None = None,
  metadata: dict[str, Any] | None = None,
  name: str | None = None,
  **kwargs: Any = {}
) -> Run
```

**Note:**

Naming can be confusing here: there is `on_chat_model_start`, but no
corresponding `on_chat_model_end` callback. Chat model completion is
routed through `on_llm_end` / `_on_llm_end`, which are shared with
text LLM runs.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized model. |
| `messages`\* | `list[list[BaseMessage]]` | The messages to start the chat with. |
| `run_id`\* | `UUID` | The run ID. |
| `tags` | `list[str] | None` | Default:`None`  The tags for the run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The parent run ID. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata for the run. |
| `name` | `str | None` | Default:`None`  The name of the run. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


