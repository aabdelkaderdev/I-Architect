<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/AsyncBaseTracer/on_chat_model_start -->

Methodv1.2.21 (latest)●Since v0.2

# on\_chat\_model\_start


```
on_chat_model_start(
  self,
  serialized: dict[str, Any],
  messages: list[list[BaseMessage]],
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  name: str | None = None,
  **kwargs: Any = {}
) -> Any
```


