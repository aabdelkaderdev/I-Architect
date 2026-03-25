<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/llms/BaseLLM/generate -->

Methodv1.2.21 (latest)●Since v0.1

# generate

Pass a sequence of prompts to a model and return generations.

This method should make use of batched calls for models that expose a batched
API.

Use this method when you want to:

1. Take advantage of batched calls,
2. Need more output from the model than just the top generated value,
3. Are building chains that are agnostic to the underlying language model
   type (e.g., pure text completion models vs chat models).


```
generate(
  self,
  prompts: list[str],
  stop: list[str] | None = None,
  callbacks: Callbacks | list[Callbacks] | None = None,
  *,
  tags: list[str] | list[list[str]] | None = None,
  metadata: dict[str, Any] | list[dict[str, Any]] | None = None,
  run_name: str | list[str] | None = None,
  run_id: uuid.UUID | list[uuid.UUID | None] | None = None,
  **kwargs: Any = {}
) -> LLMResult
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `prompts`\* | `list[str]` | List of string prompts. |
| `stop` | `list[str] | None` | Default:`None`  Stop words to use when generating.  Model output is cut off at the first occurrence of any of these substrings. |
| `callbacks` | `Callbacks | list[Callbacks] | None` | Default:`None`  `Callbacks` to pass through.  Used for executing additional functionality, such as logging or streaming, throughout generation. |
| `tags` | `list[str] | list[list[str]] | None` | Default:`None`  List of tags to associate with each prompt. If provided, the length of the list must match the length of the prompts list. |
| `metadata` | `dict[str, Any] | list[dict[str, Any]] | None` | Default:`None`  List of metadata dictionaries to associate with each prompt. If provided, the length of the list must match the length of the prompts list. |
| `run_name` | `str | list[str] | None` | Default:`None`  List of run names to associate with each prompt. If provided, the length of the list must match the length of the prompts list. |
| `run_id` | `uuid.UUID | list[uuid.UUID | None] | None` | Default:`None`  List of run IDs to associate with each prompt. If provided, the length of the list must match the length of the prompts list. |
| `**kwargs` | `Any` | Default:`{}`  Arbitrary additional keyword arguments.  These are usually passed to the model provider API call. |


