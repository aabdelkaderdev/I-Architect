<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/qa_with_sources/loading/load_qa_with_sources_chain -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# load\_qa\_with\_sources\_chain

Load a question answering with sources chain.


```
load_qa_with_sources_chain(
  llm: BaseLanguageModel,
  chain_type: str = 'stuff',
  verbose: bool | None = None,
  **kwargs: Any = {}
) -> BaseCombineDocumentsChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | Language Model to use in the chain. |
| `chain_type` | `str` | Default:`'stuff'`  Type of document combining chain to use. Should be one of "stuff", "map\_reduce", "refine" and "map\_rerank". |
| `verbose` | `bool | None` | Default:`None`  Whether chains should be run in verbose mode or not. Note that this applies to all chains that make up the final chain. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


