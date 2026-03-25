<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/AsyncBaseTracer/on_tool_error -->

Methodv1.2.21 (latest)●Since v0.2

# on\_tool\_error


```
on_tool_error(
  self,
  error: BaseException,
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  **kwargs: Any = {}
) -> None
```


