<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/listwise_rerank/LLMListwiseRerank/reranker -->

Attributev1.2.13 (latest)●Since v1.0

# reranker

LLM-based reranker to use for filtering documents. Expected to take in a dict
with 'documents: Sequence[Document]' and 'query: str' keys and output a
List[Document].


```
reranker: Runnable[dict, list[Document]]
```


