<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_error -->

Methodv1.2.21 (latest)●Since v0.2

# on\_llm\_error


```
on_llm_error(
  self,
  error: BaseException,
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  **kwargs: Any = {}
) -> None
```


