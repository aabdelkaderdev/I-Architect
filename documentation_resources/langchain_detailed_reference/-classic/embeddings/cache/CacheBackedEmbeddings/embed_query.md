<!-- Source: https://reference.langchain.com/python/langchain-classic/embeddings/cache/CacheBackedEmbeddings/embed_query -->

Methodv1.2.13 (latest)●Since v1.0

# embed\_query

Embed query text.

By default, this method does not cache queries. To enable caching, set the
`cache_query` parameter to `True` when initializing the embedder.


```
embed_query(
    self,
    text: str,
) -> list[float]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The text to embed. |


