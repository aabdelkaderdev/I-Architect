<!-- Source: https://reference.langchain.com/python/langchain-classic/embeddings/cache/CacheBackedEmbeddings/from_bytes_store -->

Methodv1.2.13 (latest)●Since v1.0

# from\_bytes\_store

On-ramp that adds the necessary serialization and encoding to the store.


```
from_bytes_store(
  cls,
  underlying_embeddings: Embeddings,
  document_embedding_cache: ByteStore,
  *,
  namespace: str = '',
  batch_size: int | None = None,
  query_embedding_cache: bool | ByteStore = False,
  key_encoder: Callable[[str], str] | Literal['sha1', 'blake2b', 'sha256', 'sha512'] = 'sha1'
) -> CacheBackedEmbeddings
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `underlying_embeddings`\* | `Embeddings` | The embedder to use for embedding. |
| `document_embedding_cache`\* | `ByteStore` | The cache to use for storing document embeddings. |
| `namespace` | `str` | Default:`''`  The namespace to use for document cache. This namespace is used to avoid collisions with other caches. For example, set it to the name of the embedding model used. |
| `batch_size` | `int | None` | Default:`None`  The number of documents to embed between store updates. |
| `query_embedding_cache` | `bool | ByteStore` | Default:`False`  The cache to use for storing query embeddings. True to use the same cache as document embeddings. False to not cache query embeddings. |
| `key_encoder` | `Callable[[str], str] | Literal['sha1', 'blake2b', 'sha256', 'sha512']` | Default:`'sha1'`  Optional callable to encode keys. If not provided, a default encoder using SHA-1 will be used. SHA-1 is not collision-resistant, and a motivated attacker could craft two different texts that hash to the same cache key.  New applications should use one of the alternative encoders or provide a custom and strong key encoder function to avoid this risk.  If you change a key encoder in an existing cache, consider just creating a new cache, to avoid (the potential for) collisions with existing keys or having duplicate keys for the same text in the cache. |


