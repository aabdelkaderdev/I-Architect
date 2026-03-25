<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/CallbackManagerForLLMRun/on_llm_new_token -->

Methodv1.2.21 (latest)●Since v0.1

# on\_llm\_new\_token

Run when LLM generates a new token.


```
on_llm_new_token(
  self,
  token: str,
  *,
  chunk: GenerationChunk | ChatGenerationChunk | None = None,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `token`\* | `str` | The new token. |
| `chunk` | `GenerationChunk | ChatGenerationChunk | None` | Default:`None`  The chunk. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


