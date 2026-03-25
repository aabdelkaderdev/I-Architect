<!-- Source: https://reference.langchain.com/python/langchain-core/caches/InMemoryCache/alookup -->

Methodv1.2.21 (latest)●Since v0.1

# alookup

Async look up based on `prompt` and `llm_string`.


```
alookup(
  self,
  prompt: str,
  llm_string: str
) -> RETURN_VAL_TYPE | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `prompt`\* | `str` | A string representation of the prompt.  In the case of a chat model, the prompt is a non-trivial serialization of the prompt into the language model. |
| `llm_string`\* | `str` | A string representation of the LLM configuration. |


