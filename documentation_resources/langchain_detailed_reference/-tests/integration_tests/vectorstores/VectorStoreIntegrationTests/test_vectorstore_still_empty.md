<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_vectorstore_still_empty -->

Methodv1.1.4 (latest)●Since v1.1

# test\_vectorstore\_still\_empty

Test that the `VectorStore` is still empty.

This test should follow a test that adds documents.

This just verifies that the fixture is set up properly to be empty
after each test.

Troubleshooting

If this test fails, check that the test class (i.e., sub class of
`VectorStoreIntegrationTests`) correctly clears the vector store in the
`finally` block.


```
test_vectorstore_still_empty(
    self,
    vectorstore: VectorStore,
) -> None
```


