<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_deleting_documents -->

Methodv1.1.4 (latest)●Since v1.1

# test\_deleting\_documents

Test deleting documents from the `VectorStore`.

Troubleshooting

If this test fails, check that `add_documents` preserves identifiers
passed in through `ids`, and that `delete` correctly removes
documents.


```
test_deleting_documents(
    self,
    vectorstore: VectorStore,
) -> None
```


