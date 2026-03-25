<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_standard_params -->

Methodv1.1.4 (latest)●Since v1.1

# test\_standard\_params

Test that model properly generates standard parameters.

These are used for tracing purposes.

Troubleshooting

If this test fails, check that the model accommodates [standard parameters](https://docs.langchain.com/oss/python/langchain/models#parameters).

Check also that the model class is named according to convention
(e.g., `ChatProviderName`).


```
test_standard_params(
    self,
    model: BaseChatModel,
) -> None
```


