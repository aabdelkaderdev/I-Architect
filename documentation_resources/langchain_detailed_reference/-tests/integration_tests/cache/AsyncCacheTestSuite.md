<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite -->

Classv1.1.4 (latest)●Since v1.1

# AsyncCacheTestSuite

Test suite for checking the `BaseCache` API of a caching layer for LLMs.

Verifies the basic caching API of a caching layer for LLMs.

The test suite is designed for synchronous caching layers.

Implementers should subclass this test suite and provide a fixture that returns an
empty cache for each test.


```
AsyncCacheTestSuite()
```

## Bases

`BaseStandardTests`

## Methods

[method

cache

Get the cache class to test.

The returned cache should be EMPTY.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite/cache)[method

get\_sample\_prompt

Return a sample prompt for testing.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite/get_sample_prompt)[method

get\_sample\_llm\_string

Return a sample LLM string for testing.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite/get_sample_llm_string)[method

get\_sample\_generation

Return a sample `Generation` object for testing.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite/get_sample_generation)[method

test\_cache\_is\_empty

Test that the cache is empty.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite/test_cache_is_empty)[method

test\_update\_cache

Test updating the cache.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite/test_update_cache)[method

test\_cache\_still\_empty

Test that the cache is still empty.

This test should follow a test that updates the cache.

This just verifies that the fixture is set up properly to be empty after each
test.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite/test_cache_still_empty)[method

test\_clear\_cache

Test clearing the cache.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite/test_clear_cache)[method

test\_cache\_miss

Test cache miss.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite/test_cache_miss)[method

test\_cache\_hit

Test cache hit.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite/test_cache_hit)[method

test\_update\_cache\_with\_multiple\_generations

Test updating the cache with multiple `Generation` objects.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite/test_update_cache_with_multiple_generations)

## Inherited from[BaseStandardTests](/python/langchain-tests/base/BaseStandardTests)

### Methods

[Mtest\_no\_overrides\_DO\_NOT\_OVERRIDE

—

Test that no standard tests are overridden.](/python/langchain-tests/base/BaseStandardTests/test_no_overrides_DO_NOT_OVERRIDE)


