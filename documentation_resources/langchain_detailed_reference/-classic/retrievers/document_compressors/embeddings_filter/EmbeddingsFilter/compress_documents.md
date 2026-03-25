<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter/compress_documents -->

Methodv1.2.13 (latest)●Since v1.0

# compress\_documents

Filter documents based on similarity of their embeddings to the query.


```
compress_documents(
  self,
  documents: Sequence[Document],
  query: str,
  callbacks: Callbacks | None = None
) -> Sequence[Document]
```


