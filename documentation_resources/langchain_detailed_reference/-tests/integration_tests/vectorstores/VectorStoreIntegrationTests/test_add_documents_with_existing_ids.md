<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_with_existing_ids -->

Methodv1.1.4 (latest)●Since v1.1

# test\_add\_documents\_with\_existing\_ids

Test that `add_documents` with existing IDs is idempotent.

Troubleshooting

If this test fails, check that `get_by_ids` is implemented and returns
documents in the same order as the IDs passed in.

This test also verifies that:

1. IDs specified in the `Document.id` field are assigned when adding
   documents.
2. If some documents include IDs and others don't string IDs are generated
   for the latter.

Note

`get_by_ids` was added to the `VectorStore` interface in
`langchain-core` version 0.2.11. If difficult to implement, this
test can be skipped by setting the `has_get_by_ids` property to
`False`.

```
@property
def has_get_by_ids(self) -> bool:
    return False
```


```
test_add_documents_with_existing_ids(
    self,
    vectorstore: VectorStore,
) -> None
```


