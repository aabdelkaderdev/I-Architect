<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/AsyncBaseTracer/on_chain_start -->

Methodv1.2.21 (latest)●Since v0.2

# on\_chain\_start


```
on_chain_start(
  self,
  serialized: dict[str, Any],
  inputs: dict[str, Any],
  *,
  run_id: UUID,
  tags: list[str] | None = None,
  parent_run_id: UUID | None = None,
  metadata: dict[str, Any] | None = None,
  run_type: str | None = None,
  name: str | None = None,
  **kwargs: Any = {}
) -> None
```


