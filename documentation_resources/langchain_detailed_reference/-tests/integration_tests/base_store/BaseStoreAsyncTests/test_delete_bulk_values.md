<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests/test_delete_bulk_values -->

Methodv1.1.4 (latest)●Since v1.1

# test\_delete\_bulk\_values

Test that we can delete several values at once.


```
test_delete_bulk_values(
  self,
  kv_store: BaseStore[str, V],
  three_values: tuple[V, V, V]
) -> None
```


