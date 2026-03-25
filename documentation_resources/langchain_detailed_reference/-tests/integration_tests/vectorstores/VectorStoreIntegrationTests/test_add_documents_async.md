<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_async -->

Methodv1.1.4 (latest)●Since v1.1

# test\_add\_documents\_async

Test adding documents into the `VectorStore`.

Troubleshooting

If this test fails, check that:

1. We correctly initialize an empty vector store in the `vectorestore`
   fixture.
2. Calling `.asimilarity_search` for the top `k` similar documents does
   not threshold by score.
3. We do not mutate the original document object when adding it to the
   vector store (e.g., by adding an ID).


```
test_add_documents_async(
    self,
    vectorstore: VectorStore,
) -> None
```


