<!-- Source: https://reference.langchain.com/python/langchain-classic/embeddings/cache/CacheBackedEmbeddings/embed_documents -->

Methodv1.2.13 (latest)●Since v1.0

# embed\_documents

Embed a list of texts.

The method first checks the cache for the embeddings.
If the embeddings are not found, the method uses the underlying embedder
to embed the documents and stores the results in the cache.


```
embed_documents(
    self,
    texts: list[str],
) -> list[list[float]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `texts`\* | `list[str]` | A list of texts to embed. |


