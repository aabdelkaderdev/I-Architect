<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/cache -->

Modulev1.1.4 (latest)●Since v1.1

# cache

## Classes



[class

BaseStandardTests

Base class for standard tests.](/python/langchain-tests/base/BaseStandardTests)

[class

SyncCacheTestSuite

Test suite for checking the `BaseCache` API of a caching layer for LLMs.

This test suite verifies the basic caching API of a caching layer for LLMs.

The test suite is designed for synchronous caching layers.

Implementers should subclass this test suite and provide a fixture
that returns an empty cache for each test.](/python/langchain-tests/integration_tests/cache/SyncCacheTestSuite)

[class

AsyncCacheTestSuite

Test suite for checking the `BaseCache` API of a caching layer for LLMs.

Verifies the basic caching API of a caching layer for LLMs.

The test suite is designed for synchronous caching layers.

Implementers should subclass this test suite and provide a fixture that returns an
empty cache for each test.](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite)

Standard tests for the `BaseCache` abstraction.

We don't recommend implementing externally managed `BaseCache` abstractions at this
time.