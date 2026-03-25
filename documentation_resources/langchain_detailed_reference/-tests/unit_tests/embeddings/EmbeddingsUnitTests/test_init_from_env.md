<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/embeddings/EmbeddingsUnitTests/test_init_from_env -->

Methodv1.1.4 (latest)●Since v1.1

# test\_init\_from\_env

Test initialization from environment variables.

Relies on the `init_from_env_params` property.
Test is skipped if that property is not set.

Troubleshooting

If this test fails, ensure that `init_from_env_params` is specified
correctly and that model parameters are properly set from environment
variables during initialization.


```
test_init_from_env(
    self,
) -> None
```


