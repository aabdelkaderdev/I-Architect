<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/re_phraser/RePhraseQueryRetriever/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Initialize from llm using default template.

The prompt used here expects a single input: `question`


```
from_llm(
  cls,
  retriever: BaseRetriever,
  llm: BaseLLM,
  prompt: BasePromptTemplate = DEFAULT_QUERY_PROMPT
) -> RePhraseQueryRetriever
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `retriever`\* | `BaseRetriever` | retriever to query documents from |
| `llm`\* | `BaseLLM` | llm for query generation using DEFAULT\_QUERY\_PROMPT |
| `prompt` | `BasePromptTemplate` | Default:`DEFAULT_QUERY_PROMPT`  prompt template for query generation |


