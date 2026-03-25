<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_llm_new_token -->

Methodv1.2.21 (latest)●Since v0.1

# on\_llm\_new\_token

Run on new LLM token.

Only available when streaming is enabled.


```
on_llm_new_token(
  self,
  token: str,
  *,
  chunk: GenerationChunk | ChatGenerationChunk | None = None,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  **kwargs: Any = {}
) -> Run
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `token`\* | `str` | The token. |
| `chunk` | `GenerationChunk | ChatGenerationChunk | None` | Default:`None`  The chunk. |
| `run_id`\* | `UUID` | The run ID. |
| `parent_run_id` | `UUID | None` | Default:`None`  The parent run ID. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


