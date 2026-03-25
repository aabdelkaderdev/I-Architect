<!-- Source: https://reference.langchain.com/python/langchain-core/caches/BaseCache/lookup -->

Methodv1.2.21 (latest)●Since v0.1

# lookup

Look up based on `prompt` and `llm_string`.

A cache implementation is expected to generate a key from the 2-tuple
of `prompt` and `llm_string` (e.g., by concatenating them with a delimiter).


```
lookup(
  self,
  prompt: str,
  llm_string: str
) -> RETURN_VAL_TYPE | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `prompt`\* | `str` | A string representation of the prompt.  In the case of a chat model, the prompt is a non-trivial serialization of the prompt into the language model. |
| `llm_string`\* | `str` | A string representation of the LLM configuration.  This is used to capture the invocation parameters of the LLM (e.g., model name, temperature, stop tokens, max tokens, etc.).  These invocation parameters are serialized into a string representation. |


