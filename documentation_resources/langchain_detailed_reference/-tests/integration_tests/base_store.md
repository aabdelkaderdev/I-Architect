<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/base_store -->

Modulev1.1.4 (latest)●Since v1.1

# base\_store

Standard tests for the `BaseStore` abstraction.

We don't recommend implementing externally managed `BaseStore` abstractions at this
time.

## Attributes

[attribute

V](/python/langchain-tests/integration_tests/base_store/V)

## Classes

[class

BaseStandardTests

Base class for standard tests.](/python/langchain-tests/base/BaseStandardTests)[class

BaseStoreSyncTests

Test suite for checking the key-value API of a `BaseStore`.

This test suite verifies the basic key-value API of a `BaseStore`.

The test suite is designed for synchronous key-value stores.

Implementers should subclass this test suite and provide a fixture
that returns an empty key-value store for each test.](/python/langchain-tests/integration_tests/base_store/BaseStoreSyncTests)[class

BaseStoreAsyncTests

Test suite for checking the key-value API of a `BaseStore`.

This test suite verifies the basic key-value API of a `BaseStore`.

The test suite is designed for synchronous key-value stores.

Implementers should subclass this test suite and provide a fixture
that returns an empty key-value store for each test.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests)


