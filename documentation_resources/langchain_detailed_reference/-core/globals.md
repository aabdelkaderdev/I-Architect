<!-- Source: https://reference.langchain.com/python/langchain-core/globals -->

Modulev1.2.21 (latest)●Since v0.1

# globals

Global values and configuration that apply to all of LangChain.

## Functions

[function

set\_verbose

Set a new value for the `verbose` global setting.](/python/langchain-core/globals/set_verbose)[function

get\_verbose

Get the value of the `verbose` global setting.](/python/langchain-core/globals/get_verbose)[function

set\_debug

Set a new value for the `debug` global setting.](/python/langchain-core/globals/set_debug)[function

get\_debug

Get the value of the `debug` global setting.](/python/langchain-core/globals/get_debug)[function

set\_llm\_cache

Set a new LLM cache, overwriting the previous value, if any.](/python/langchain-core/globals/set_llm_cache)[function

get\_llm\_cache

Get the value of the `llm_cache` global setting.](/python/langchain-core/globals/get_llm_cache)

## Classes

[class

BaseCache

Interface for a caching layer for LLMs and Chat models.

The cache interface consists of the following methods:

- lookup: Look up a value based on a prompt and `llm_string`.
- update: Update the cache based on a prompt and `llm_string`.
- clear: Clear the cache.

In addition, the cache interface provides an async version of each method.

The default implementation of the async methods is to run the synchronous
method in an executor. It's recommended to override the async methods
and provide async implementations to avoid unnecessary overhead.](/python/langchain-core/caches/BaseCache)


