<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_init -->

Methodv1.1.4 (latest)●Since v1.1

# test\_init

Test model initialization. This should pass for all integrations.

Troubleshooting

If this test fails, ensure that:

1. `chat_model_params` is specified and the model can be initialized
   from those params;
2. The model accommodates
   [standard parameters](https://docs.langchain.com/oss/python/langchain/models#parameters).


```
test_init(
    self,
) -> None
```


