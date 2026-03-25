<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests -->

Classv1.1.4 (latest)●Since v1.1

# BaseStoreAsyncTests

Test suite for checking the key-value API of a `BaseStore`.

This test suite verifies the basic key-value API of a `BaseStore`.

The test suite is designed for synchronous key-value stores.

Implementers should subclass this test suite and provide a fixture
that returns an empty key-value store for each test.


```
BaseStoreAsyncTests()
```

## Bases

`BaseStandardTests``Generic[V]`

## Methods

[method

kv\_store

Get the key-value store class to test.

The returned key-value store should be EMPTY.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/kv_store)[method

three\_values

Three example values that will be used in the tests.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/three_values)[method

test\_three\_values

Test that the fixture provides three values.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_three_values)[method

test\_kv\_store\_is\_empty

Test that the key-value store is empty.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_kv_store_is_empty)[method

test\_set\_and\_get\_values

Test setting and getting values in the key-value store.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_set_and_get_values)[method

test\_store\_still\_empty

Test that the store is still empty.

This test should follow a test that sets values.

This just verifies that the fixture is set up properly to be empty
after each test.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_store_still_empty)[method

test\_delete\_values

Test deleting values from the key-value store.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_delete_values)[method

test\_delete\_bulk\_values

Test that we can delete several values at once.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_delete_bulk_values)[method

test\_delete\_missing\_keys

Deleting missing keys should not raise an exception.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_delete_missing_keys)[method

test\_set\_values\_is\_idempotent

Setting values by key should be idempotent.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_set_values_is_idempotent)[method

test\_get\_can\_get\_same\_value

Test that the same value can be retrieved multiple times.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_get_can_get_same_value)[method

test\_overwrite\_values\_by\_key

Test that we can overwrite values by key using mset.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_overwrite_values_by_key)[method

test\_yield\_keys

Test that we can yield keys from the store.](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_yield_keys)

## Inherited from[BaseStandardTests](/python/langchain-tests/base/BaseStandardTests)

### Methods

[Mtest\_no\_overrides\_DO\_NOT\_OVERRIDE

—

Test that no standard tests are overridden.](/python/langchain-tests/base/BaseStandardTests/test_no_overrides_DO_NOT_OVERRIDE)


