<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/llms/BaseLLM/stream -->

Methodv1.2.21 (latest)●Since v0.1

# stream


```
stream(
  self,
  input: LanguageModelInput,
  config: RunnableConfig | None = None,
  *,
  stop: list[str] | None = None,
  **kwargs: Any = {}
) -> Iterator[str]
```


