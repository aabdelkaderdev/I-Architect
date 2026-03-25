<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/llms/BaseLLM/batch -->

Methodv1.2.21 (latest)●Since v0.1

# batch


```
batch(
  self,
  inputs: list[LanguageModelInput],
  config: RunnableConfig | list[RunnableConfig] | None = None,
  *,
  return_exceptions: bool = False,
  **kwargs: Any = {}
) -> list[str]
```


