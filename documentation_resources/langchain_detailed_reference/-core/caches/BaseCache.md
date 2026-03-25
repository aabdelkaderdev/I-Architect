<!-- Source: https://reference.langchain.com/python/langchain-core/caches/BaseCache -->

Classv1.2.21 (latest)●Since v0.1

# BaseCache

Interface for a caching layer for LLMs and Chat models.

The cache interface consists of the following methods:

- lookup: Look up a value based on a prompt and `llm_string`.
- update: Update the cache based on a prompt and `llm_string`.
- clear: Clear the cache.

In addition, the cache interface provides an async version of each method.

The default implementation of the async methods is to run the synchronous
method in an executor. It's recommended to override the async methods
and provide async implementations to avoid unnecessary overhead.


```
BaseCache()
```

## Bases

`ABC`

## Methods

[method

lookup

Look up based on `prompt` and `llm_string`.

A cache implementation is expected to generate a key from the 2-tuple
of `prompt` and `llm_string` (e.g., by concatenating them with a delimiter).](/python/langchain-core/caches/BaseCache/lookup)[method

update

Update cache based on `prompt` and `llm_string`.

The `prompt` and `llm_string` are used to generate a key for the cache. The key
should match that of the lookup method.](/python/langchain-core/caches/BaseCache/update)[method

clear

Clear cache that can take additional keyword arguments.](/python/langchain-core/caches/BaseCache/clear)[method

alookup

Async look up based on `prompt` and `llm_string`.

A cache implementation is expected to generate a key from the 2-tuple
of `prompt` and `llm_string` (e.g., by concatenating them with a delimiter).](/python/langchain-core/caches/BaseCache/alookup)[method

aupdate

Async update cache based on `prompt` and `llm_string`.

The prompt and llm\_string are used to generate a key for the cache.
The key should match that of the look up method.](/python/langchain-core/caches/BaseCache/aupdate)[method

aclear

Async clear cache that can take additional keyword arguments.](/python/langchain-core/caches/BaseCache/aclear)


