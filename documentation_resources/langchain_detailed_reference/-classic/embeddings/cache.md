<!-- Source: https://reference.langchain.com/python/langchain-classic/embeddings/cache -->

Modulev1.2.13 (latest)●Since v1.0

# cache

Module contains code for a cache backed embedder.

The cache backed embedder is a wrapper around an embedder that caches
embeddings in a key-value store. The cache is used to avoid recomputing
embeddings for the same text.

The text is hashed and the hash is used as the key in the cache.

## Attributes

[attribute

NAMESPACE\_UUID](/python/langchain-classic/embeddings/cache/NAMESPACE_UUID)

## Classes

[class

EncoderBackedStore

Wraps a store with key and value encoders/decoders.

Examples that uses JSON for encoding/decoding:

```
import json

def key_encoder(key: int) -> str:
    return json.dumps(key)

def value_serializer(value: float) -> str:
    return json.dumps(value)

def value_deserializer(serialized_value: str) -> float:
    return json.loads(serialized_value)

# Create an instance of the abstract store
abstract_store = MyCustomStore()

# Create an instance of the encoder-backed store
store = EncoderBackedStore(
    store=abstract_store,
    key_encoder=key_encoder,
    value_serializer=value_serializer,
    value_deserializer=value_deserializer,
)

# Use the encoder-backed store methods
store.mset([(1, 3.14), (2, 2.718)])
values = store.mget([1, 2])  # Retrieves [3.14, 2.718]
store.mdelete([1, 2])  # Deletes the keys 1 and 2
```](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore)[class

CacheBackedEmbeddings

Interface for caching results from embedding models.

The interface allows works with any store that implements
the abstract store interface accepting keys of type str and values of list of
floats.

If need be, the interface can be extended to accept other implementations
of the value serializer and deserializer, as well as the key encoder.

Note that by default only document embeddings are cached. To cache query
embeddings too, pass in a query\_embedding\_store to constructor.](/python/langchain-classic/embeddings/cache/CacheBackedEmbeddings)


