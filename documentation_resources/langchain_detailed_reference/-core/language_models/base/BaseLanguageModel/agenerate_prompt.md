<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/base/BaseLanguageModel/agenerate_prompt -->

Methodv1.2.21 (latest)●Since v0.1

# agenerate\_prompt

Asynchronously pass a sequence of prompts and return model generations.

This method should make use of batched calls for models that expose a batched
API.

Use this method when you want to:

1. Take advantage of batched calls,
2. Need more output from the model than just the top generated value,
3. Are building chains that are agnostic to the underlying language model
   type (e.g., pure text completion models vs chat models).


```
agenerate_prompt(
  self,
  prompts: list[PromptValue],
  stop: list[str] | None = None,
  callbacks: Callbacks = None,
  **kwargs: Any = {}
) -> LLMResult
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `prompts`\* | `list[PromptValue]` | List of `PromptValue` objects.  A `PromptValue` is an object that can be converted to match the format of any language model (string for pure text generation models and `BaseMessage` objects for chat models). |
| `stop` | `list[str] | None` | Default:`None`  Stop words to use when generating.  Model output is cut off at the first occurrence of any of these substrings. |
| `callbacks` | `Callbacks` | Default:`None`  `Callbacks` to pass through.  Used for executing additional functionality, such as logging or streaming, throughout generation. |
| `**kwargs` | `Any` | Default:`{}`  Arbitrary additional keyword arguments.  These are usually passed to the model provider API call. |


