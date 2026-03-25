<!-- Source: https://reference.langchain.com/python/langchain-core/stores -->

Modulev1.2.21 (latest)●Since v0.1

# stores

**Store** implements the key-value stores and storage helpers.

Module provides implementations of various key-value stores that conform
to a simple key-value interface.

The primary goal of these storages is to support implementation of caching.

## Attributes

[attribute

K](/python/langchain-core/stores/K)[attribute

V](/python/langchain-core/stores/V)[attribute

ByteStore: BaseStore[str, bytes]](/python/langchain-core/stores/ByteStore)

## Functions

[function

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)

## Classes

[class

LangChainException

General LangChain exception.](/python/langchain-core/exceptions/LangChainException)[class

BaseStore

Abstract interface for a key-value store.

This is an interface that's meant to abstract away the details of different
key-value stores. It provides a simple interface for getting, setting, and deleting
key-value pairs.

The basic methods are `mget`, `mset`, and `mdelete` for getting, setting, and
deleting multiple key-value pairs at once. The `yield_keys` method is used to
iterate over keys that match a given prefix.

The async versions of these methods are also provided, which are meant to be used in
async contexts. The async methods are named with an `a` prefix, e.g., `amget`,
`amset`, `amdelete`, and `ayield_keys`.

By default, the `amget`, `amset`, `amdelete`, and `ayield_keys` methods are
implemented using the synchronous methods. If the store can natively support async
operations, it should override these methods.

By design the methods only accept batches of keys and values, and not single keys or
values. This is done to force user code to work with batches which will usually be
more efficient by saving on round trips to the store.](/python/langchain-core/stores/BaseStore)[class

InMemoryBaseStore

In-memory implementation of the `BaseStore` using a dictionary.](/python/langchain-core/stores/InMemoryBaseStore)[class

InMemoryStore

In-memory store for any type of data.](/python/langchain-core/stores/InMemoryStore)[class

InMemoryByteStore

In-memory store for bytes.](/python/langchain-core/stores/InMemoryByteStore)[class

InvalidKeyException

Raised when a key is invalid; e.g., uses incorrect characters.](/python/langchain-core/stores/InvalidKeyException)


