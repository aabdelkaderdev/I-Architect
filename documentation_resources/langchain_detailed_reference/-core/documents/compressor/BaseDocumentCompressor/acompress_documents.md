<!-- Source: https://reference.langchain.com/python/langchain-core/documents/compressor/BaseDocumentCompressor/acompress_documents -->

Methodv1.2.21 (latest)●Since v0.1

# acompress\_documents

Async compress retrieved documents given the query context.


```
acompress_documents(
  self,
  documents: Sequence[Document],
  query: str,
  callbacks: Callbacks | None = None
) -> Sequence[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `documents`\* | `Sequence[Document]` | The retrieved `Document` objects. |
| `query`\* | `str` | The query context. |
| `callbacks` | `Callbacks | None` | Default:`None`  Optional `Callbacks` to run during compression. |


