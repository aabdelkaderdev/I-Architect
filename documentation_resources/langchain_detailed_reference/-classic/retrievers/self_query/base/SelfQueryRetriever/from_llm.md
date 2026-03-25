<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/self_query/base/SelfQueryRetriever/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create a SelfQueryRetriever from an LLM and a vector store.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  vectorstore: VectorStore,
  document_contents: str,
  metadata_field_info: Sequence[AttributeInfo | dict],
  structured_query_translator: Visitor | None = None,
  chain_kwargs: dict | None = None,
  enable_limit: bool = False,
  use_original_query: bool = False,
  **kwargs: Any = {}
) -> SelfQueryRetriever
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The language model to use for generating queries. |
| `vectorstore`\* | `VectorStore` | The vector store to use for retrieving documents. |
| `document_contents`\* | `str` | Description of the page contents of the document to be queried. |
| `metadata_field_info`\* | `Sequence[AttributeInfo | dict]` | Metadata field information for the documents. |
| `structured_query_translator` | `Visitor | None` | Default:`None`  Optional translator for turning internal query language into `VectorStore` search params. |
| `chain_kwargs` | `dict | None` | Default:`None`  Additional keyword arguments for the query constructor. |
| `enable_limit` | `bool` | Default:`False`  Whether to enable the limit operator. |
| `use_original_query` | `bool` | Default:`False`  Whether to use the original query instead of the revised query from the LLM. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments for the SelfQueryRetriever. |


