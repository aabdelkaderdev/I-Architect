<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/embeddings/EmbeddingsIntegrationTests/test_aembed_query -->

Methodv1.1.4 (latest)●Since v1.1

# test\_aembed\_query

Test embedding a string query async.

Troubleshooting

If this test fails, check that:

1. The model will generate a list of floats when calling `aembed_query`
   on a string.
2. The length of the list is consistent across different inputs.


```
test_aembed_query(
    self,
    model: Embeddings,
) -> None
```


