<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_with_ids_is_idempotent -->

Methodv1.1.4 (latest)●Since v1.1

# test\_add\_documents\_with\_ids\_is\_idempotent

Adding by ID should be idempotent.

Troubleshooting

If this test fails, check that adding the same document twice with the
same IDs has the same effect as adding it once (i.e., it does not
duplicate the documents).


```
test_add_documents_with_ids_is_idempotent(
    self,
    vectorstore: VectorStore,
) -> None
```


