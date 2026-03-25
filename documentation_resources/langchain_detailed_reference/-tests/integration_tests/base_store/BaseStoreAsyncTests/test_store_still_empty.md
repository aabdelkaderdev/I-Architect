<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_store_still_empty -->

Methodv1.1.4 (latest)●Since v1.1

# test\_store\_still\_empty

Test that the store is still empty.

This test should follow a test that sets values.

This just verifies that the fixture is set up properly to be empty
after each test.


```
test_store_still_empty(
    self,
    kv_store: BaseStore[str, V],
) -> None
```


