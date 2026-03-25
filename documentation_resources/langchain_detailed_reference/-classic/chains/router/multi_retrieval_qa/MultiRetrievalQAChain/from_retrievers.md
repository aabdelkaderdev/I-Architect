<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/router/multi_retrieval_qa/MultiRetrievalQAChain/from_retrievers -->

Methodv1.2.13 (latest)●Since v1.0

# from\_retrievers

Create a multi retrieval qa chain from an LLM and a default chain.


```
from_retrievers(
  cls,
  llm: BaseLanguageModel,
  retriever_infos: list[dict[str, Any]],
  default_retriever: BaseRetriever | None = None,
  default_prompt: PromptTemplate | None = None,
  default_chain: Chain | None = None,
  *,
  default_chain_llm: BaseLanguageModel | None = None,
  **kwargs: Any = {}
) -> MultiRetrievalQAChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The language model to use. |
| `retriever_infos`\* | `list[dict[str, Any]]` | Dictionaries containing retriever information. |
| `default_retriever` | `BaseRetriever | None` | Default:`None`  Optional default retriever to use if no default chain is provided. |
| `default_prompt` | `PromptTemplate | None` | Default:`None`  Optional prompt template to use for the default retriever. |
| `default_chain` | `Chain | None` | Default:`None`  Optional default chain to use when router doesn't map input to one of the destinations. |
| `default_chain_llm` | `BaseLanguageModel | None` | Default:`None`  Optional language model to use if no default chain and no default retriever are provided. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments to pass to the chain. |


