<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/multi_query/MultiQueryRetriever/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Initialize from llm using default template.


```
from_llm(
  cls,
  retriever: BaseRetriever,
  llm: BaseLanguageModel,
  prompt: BasePromptTemplate = DEFAULT_QUERY_PROMPT,
  parser_key: str | None = None,
  include_original: bool = False
) -> MultiQueryRetriever
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `retriever`\* | `BaseRetriever` | retriever to query documents from |
| `llm`\* | `BaseLanguageModel` | llm for query generation using DEFAULT\_QUERY\_PROMPT |
| `prompt` | `BasePromptTemplate` | Default:`DEFAULT_QUERY_PROMPT`  The prompt which aims to generate several different versions of the given user query |
| `parser_key` | `str | None` | Default:`None`  DEPRECATED. `parser_key` is no longer used and should not be specified. |
| `include_original` | `bool` | Default:`False`  Whether to include the original query in the list of generated queries. |


