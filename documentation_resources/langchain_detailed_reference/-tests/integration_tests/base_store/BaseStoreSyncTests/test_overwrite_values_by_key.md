<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/base_store/BaseStoreSyncTests/test_overwrite_values_by_key -->

Methodv1.1.4 (latest)●Since v1.1

# test\_overwrite\_values\_by\_key

Test that we can overwrite values by key using mset.


```
test_overwrite_values_by_key(
  self,
  kv_store: BaseStore[str, V],
  three_values: tuple[V, V, V]
) -> None
```


