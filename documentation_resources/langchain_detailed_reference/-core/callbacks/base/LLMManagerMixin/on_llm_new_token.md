<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/LLMManagerMixin/on_llm_new_token -->

Methodv1.2.21 (latest)●Since v0.1

# on\_llm\_new\_token

Run on new output token.

Only available when streaming is enabled.

For both chat models and non-chat models (legacy text completion LLMs).


```
on_llm_new_token(
  self,
  token: str,
  *,
  chunk: GenerationChunk | ChatGenerationChunk | None = None,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `token`\* | `str` | The new token. |
| `chunk` | `GenerationChunk | ChatGenerationChunk | None` | Default:`None`  The new generated chunk, containing content and other information. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `tags` | `list[str] | None` | Default:`None`  The tags. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


