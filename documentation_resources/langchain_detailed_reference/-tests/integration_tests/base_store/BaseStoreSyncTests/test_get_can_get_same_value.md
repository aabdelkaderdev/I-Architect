<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/base_store/BaseStoreSyncTests/test_get_can_get_same_value -->

Methodv1.1.4 (latest)●Since v1.1

# test\_get\_can\_get\_same\_value

Test that the same value can be retrieved multiple times.


```
test_get_can_get_same_value(
  self,
  kv_store: BaseStore[str, V],
  three_values: tuple[V, V, V]
) -> None
```


