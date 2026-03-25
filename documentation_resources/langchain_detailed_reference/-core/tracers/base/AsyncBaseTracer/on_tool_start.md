<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/AsyncBaseTracer/on_tool_start -->

Methodv1.2.21 (latest)●Since v0.2

# on\_tool\_start


```
on_tool_start(
  self,
  serialized: dict[str, Any],
  input_str: str,
  *,
  run_id: UUID,
  tags: list[str] | None = None,
  parent_run_id: UUID | None = None,
  metadata: dict[str, Any] | None = None,
  name: str | None = None,
  inputs: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> None
```


