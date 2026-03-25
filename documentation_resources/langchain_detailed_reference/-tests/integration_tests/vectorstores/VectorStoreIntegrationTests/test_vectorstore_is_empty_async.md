<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_vectorstore_is_empty_async -->

Methodv1.1.4 (latest)●Since v1.1

# test\_vectorstore\_is\_empty\_async

Test that the `VectorStore` is empty.

Troubleshooting

If this test fails, check that the test class (i.e., sub class of
`VectorStoreIntegrationTests`) initializes an empty vector store in the
`vectorestore` fixture.


```
test_vectorstore_is_empty_async(
    self,
    vectorstore: VectorStore,
) -> None
```


