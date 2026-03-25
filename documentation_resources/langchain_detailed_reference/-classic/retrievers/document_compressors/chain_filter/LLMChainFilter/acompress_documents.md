<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/chain_filter/LLMChainFilter/acompress_documents -->

Methodv1.2.13 (latest)●Since v1.0

# acompress\_documents

Filter down documents based on their relevance to the query.


```
acompress_documents(
  self,
  documents: Sequence[Document],
  query: str,
  callbacks: Callbacks | None = None
) -> Sequence[Document]
```


