<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/embeddings/EmbeddingsIntegrationTests/test_embed_documents -->

Methodv1.1.4 (latest)●Since v1.1

# test\_embed\_documents

Test embedding a list of strings.

Troubleshooting

If this test fails, check that:

1. The model will generate a list of lists of floats when calling
   `embed_documents` on a list of strings.
2. The length of each list is the same.


```
test_embed_documents(
    self,
    model: Embeddings,
) -> None
```


