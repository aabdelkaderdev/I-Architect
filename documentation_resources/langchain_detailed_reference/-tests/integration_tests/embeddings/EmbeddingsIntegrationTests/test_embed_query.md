<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/embeddings/EmbeddingsIntegrationTests/test_embed_query -->

Methodv1.1.4 (latest)●Since v1.1

# test\_embed\_query

Test embedding a string query.

Troubleshooting

If this test fails, check that:

1. The model will generate a list of floats when calling `.embed_query`
   on a string.
2. The length of the list is consistent across different inputs.


```
test_embed_query(
    self,
    model: Embeddings,
) -> None
```


