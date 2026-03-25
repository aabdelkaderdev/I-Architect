<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/chain_extract/LLMChainExtractor/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Initialize from LLM.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  prompt: PromptTemplate | None = None,
  get_input: Callable[[str, Document], str] | None = None,
  llm_chain_kwargs: dict | None = None
) -> LLMChainExtractor
```


