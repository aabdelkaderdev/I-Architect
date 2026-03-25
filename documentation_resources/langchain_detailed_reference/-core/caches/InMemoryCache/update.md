<!-- Source: https://reference.langchain.com/python/langchain-core/caches/InMemoryCache/update -->

Methodv1.2.21 (latest)●Since v0.1

# update

Update cache based on `prompt` and `llm_string`.


```
update(
  self,
  prompt: str,
  llm_string: str,
  return_val: RETURN_VAL_TYPE
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `prompt`\* | `str` | A string representation of the prompt.  In the case of a chat model, the prompt is a non-trivial serialization of the prompt into the language model. |
| `llm_string`\* | `str` | A string representation of the LLM configuration. |
| `return_val`\* | `RETURN_VAL_TYPE` | The value to be cached.  The value is a list of `Generation` (or subclasses). |


