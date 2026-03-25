<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_start -->

Methodv1.2.21 (latest)●Since v0.2

# on\_llm\_start


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


