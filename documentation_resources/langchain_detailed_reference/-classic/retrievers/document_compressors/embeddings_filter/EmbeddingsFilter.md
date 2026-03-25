<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter -->

Classv1.2.13 (latest)●Since v1.0

# EmbeddingsFilter


```
EmbeddingsFilter()
```

## Bases

`BaseDocumentCompressor`

## Attributes

## Methods



[attribute

embeddings: Embeddings

Embeddings to use for embedding document contents and queries.](/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter/embeddings)

[attribute

similarity\_fn: Callable

Similarity function for comparing documents. Function expected to take as input
two matrices (List[List[float]]) and return a matrix of scores where higher values
indicate greater similarity.](/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter/similarity_fn)

[attribute

k: int | None

The number of relevant documents to return. Can be set to `None`, in which case
`similarity_threshold` must be specified.](/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter/k)

[attribute

similarity\_threshold: float | None

Threshold for determining when two documents are similar enough
to be considered redundant. Defaults to `None`, must be specified if `k` is set
to None.](/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter/similarity_threshold)

[attribute

model\_config](/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter/model_config)

[method

validate\_params

Validate similarity parameters.](/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter/validate_params)

[method

compress\_documents

Filter documents based on similarity of their embeddings to the query.](/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter/compress_documents)

[method

acompress\_documents

Filter documents based on similarity of their embeddings to the query.](/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter/acompress_documents)

Embeddings Filter.

Document compressor that uses embeddings to drop documents unrelated to the query.