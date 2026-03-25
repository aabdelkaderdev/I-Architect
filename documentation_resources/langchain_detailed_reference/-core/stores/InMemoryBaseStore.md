<!-- Source: https://reference.langchain.com/python/langchain-core/stores/InMemoryBaseStore -->

Classv1.2.21 (latest)●Since v0.1

# InMemoryBaseStore

In-memory implementation of the `BaseStore` using a dictionary.


```
InMemoryBaseStore(
    self,
)
```

## Bases

`BaseStore[str, V]``Generic[V]`

## Constructors

[constructor

\_\_init\_\_](/python/langchain-core/stores/InMemoryBaseStore/__init__)

## Attributes

[attribute

store: dict[str, V]](/python/langchain-core/stores/InMemoryBaseStore/store)

## Methods

[method

mget](/python/langchain-core/stores/InMemoryBaseStore/mget)[method

amget](/python/langchain-core/stores/InMemoryBaseStore/amget)[method

mset](/python/langchain-core/stores/InMemoryBaseStore/mset)[method

amset](/python/langchain-core/stores/InMemoryBaseStore/amset)[method

mdelete](/python/langchain-core/stores/InMemoryBaseStore/mdelete)[method

amdelete](/python/langchain-core/stores/InMemoryBaseStore/amdelete)[method

yield\_keys

Get an iterator over keys that match the given prefix.](/python/langchain-core/stores/InMemoryBaseStore/yield_keys)[method

ayield\_keys

Async get an async iterator over keys that match the given prefix.](/python/langchain-core/stores/InMemoryBaseStore/ayield_keys)


