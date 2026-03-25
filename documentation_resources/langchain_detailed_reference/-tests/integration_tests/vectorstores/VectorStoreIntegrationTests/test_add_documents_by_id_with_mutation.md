<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_by_id_with_mutation -->

Methodv1.1.4 (latest)●Since v1.1

# test\_add\_documents\_by\_id\_with\_mutation

Test that we can overwrite by ID using `add_documents`.

Troubleshooting

If this test fails, check that when `add_documents` is called with an
ID that already exists in the vector store, the content is updated
rather than duplicated.


```
test_add_documents_by_id_with_mutation(
    self,
    vectorstore: VectorStore,
) -> None
```


