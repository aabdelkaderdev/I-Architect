<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_deleting_bulk_documents -->

Methodv1.1.4 (latest)●Since v1.1

# test\_deleting\_bulk\_documents

Test that we can delete several documents at once.

Troubleshooting

If this test fails, check that `delete` correctly removes multiple
documents when given a list of IDs.


```
test_deleting_bulk_documents(
    self,
    vectorstore: VectorStore,
) -> None
```


