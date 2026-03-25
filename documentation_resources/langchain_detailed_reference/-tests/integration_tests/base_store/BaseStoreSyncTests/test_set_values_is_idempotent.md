<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/base_store/BaseStoreSyncTests/test_set_values_is_idempotent -->

Methodv1.1.4 (latest)●Since v1.1

# test\_set\_values\_is\_idempotent

Setting values by key should be idempotent.


```
test_set_values_is_idempotent(
  self,
  kv_store: BaseStore[str, V],
  three_values: tuple[V, V, V]
) -> None
```


