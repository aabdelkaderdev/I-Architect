<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/cross_encoder_rerank/CrossEncoderReranker/compress_documents -->

Methodv1.2.13 (latest)●Since v1.0

# compress\_documents

Rerank documents using CrossEncoder.


```
compress_documents(
  self,
  documents: Sequence[Document],
  query: str,
  callbacks: Callbacks | None = None
) -> Sequence[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `documents`\* | `Sequence[Document]` | A sequence of documents to compress. |
| `query`\* | `str` | The query to use for compressing the documents. |
| `callbacks` | `Callbacks | None` | Default:`None`  Callbacks to run during the compression process. |


