<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/test_invoke_returns_documents -->

Methodv1.1.4 (latest)●Since v1.1

# test\_invoke\_returns\_documents

Test invoke returns documents.

If invoked with the example params, the retriever should return a list of
Documents.

Troubleshooting

If this test fails, the retriever's invoke method does not return a list of
`Document` objects. Please confirm that your
`_get_relevant_documents` method returns a list of `Document` objects.


```
test_invoke_returns_documents(
    self,
    retriever: BaseRetriever,
) -> None
```


