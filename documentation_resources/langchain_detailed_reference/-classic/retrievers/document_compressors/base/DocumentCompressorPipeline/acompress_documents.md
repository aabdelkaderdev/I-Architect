<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/base/DocumentCompressorPipeline/acompress_documents -->

Methodv1.2.13 (latest)●Since v1.0

# acompress\_documents

Compress retrieved documents given the query context.


```
acompress_documents(
  self,
  documents: Sequence[Document],
  query: str,
  callbacks: Callbacks | None = None
) -> Sequence[Document]
```


