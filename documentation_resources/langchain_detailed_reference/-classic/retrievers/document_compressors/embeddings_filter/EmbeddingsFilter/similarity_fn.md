<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter/similarity_fn -->

Attributev1.2.13 (latest)●Since v1.0

# similarity\_fn

Similarity function for comparing documents. Function expected to take as input
two matrices (List[List[float]]) and return a matrix of scores where higher values
indicate greater similarity.


```
similarity_fn: Callable = Field(default_factory=_get_similarity_function)
```


