<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_delete_missing_content_async -->

Methodv1.1.4 (latest)●Since v1.1

# test\_delete\_missing\_content\_async

Deleting missing content should not raise an exception.

Troubleshooting

If this test fails, check that `adelete` does not raise an exception
when deleting IDs that do not exist.


```
test_delete_missing_content_async(
    self,
    vectorstore: VectorStore,
) -> None
```


