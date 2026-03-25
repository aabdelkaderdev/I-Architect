<!-- Source: https://reference.langchain.com/python/langchain-core/caches/BaseCache/update -->

Methodv1.2.21 (latest)●Since v0.1

# update

Update cache based on `prompt` and `llm_string`.

The `prompt` and `llm_string` are used to generate a key for the cache. The key
should match that of the lookup method.


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
| `llm_string`\* | `str` | A string representation of the LLM configuration.  This is used to capture the invocation parameters of the LLM (e.g., model name, temperature, stop tokens, max tokens, etc.).  These invocation parameters are serialized into a string representation. |
| `return_val`\* | `RETURN_VAL_TYPE` | The value to be cached.  The value is a list of `Generation` (or subclasses). |


