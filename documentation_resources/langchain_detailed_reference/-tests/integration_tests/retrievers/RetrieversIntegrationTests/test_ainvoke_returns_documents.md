<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/test_ainvoke_returns_documents -->

Methodv1.1.4 (latest)●Since v1.1

# test\_ainvoke\_returns\_documents

Test ainvoke returns documents.

If `ainvoke`'d with the example params, the retriever should return a list of
`Document` objects.

See `test_invoke_returns_documents` for more information on
troubleshooting.


```
test_ainvoke_returns_documents(
    self,
    retriever: BaseRetriever,
) -> None
```


