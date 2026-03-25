<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/AsyncBaseTracer/on_retriever_start -->

Methodv1.2.21 (latest)●Since v0.2

# on\_retriever\_start


```
on_retriever_start(
  self,
  serialized: dict[str, Any],
  query: str,
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  name: str | None = None,
  **kwargs: Any = {}
) -> None
```


