<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/get_embeddings -->

Methodv1.1.4 (latest)●Since v1.1

# get\_embeddings

Get embeddings.

A pre-defined embeddings model that should be used for this test.

This currently uses `DeterministicFakeEmbedding` from `langchain-core`,
which uses numpy to generate random numbers based on a hash of the input text.

The resulting embeddings are not meaningful, but they are deterministic.


```
get_embeddings() -> Embeddings
```


