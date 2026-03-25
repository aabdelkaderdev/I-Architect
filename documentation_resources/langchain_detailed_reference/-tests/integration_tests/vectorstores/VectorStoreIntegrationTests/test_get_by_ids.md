<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_get_by_ids -->

Methodv1.1.4 (latest)●Since v1.1

# test\_get\_by\_ids

Test get by IDs.

This test requires that `get_by_ids` be implemented on the vector store.

Troubleshooting

If this test fails, check that `get_by_ids` is implemented and returns
documents in the same order as the IDs passed in.

Note

`get_by_ids` was added to the `VectorStore` interface in
`langchain-core` version 0.2.11. If difficult to implement, this
test can be skipped by setting the `has_get_by_ids` property to
`False`.

```
@property
def has_get_by_ids(self) -> bool:
    return False
```


```
test_get_by_ids(
    self,
    vectorstore: VectorStore,
) -> None
```


