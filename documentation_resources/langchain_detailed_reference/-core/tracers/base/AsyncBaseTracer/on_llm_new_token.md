<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_new_token -->

Methodv1.2.21 (latest)●Since v0.2

# on\_llm\_new\_token


```
on_llm_new_token(
  self,
  token: str,
  *,
  chunk: GenerationChunk | ChatGenerationChunk | None = None,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  **kwargs: Any = {}
) -> None
```


