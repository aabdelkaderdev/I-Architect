<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/hyde/base/HypotheticalDocumentEmbedder/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Load and use LLMChain with either a specific prompt key or custom prompt.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  base_embeddings: Embeddings,
  prompt_key: str | None = None,
  custom_prompt: BasePromptTemplate | None = None,
  **kwargs: Any = {}
) -> HypotheticalDocumentEmbedder
```


