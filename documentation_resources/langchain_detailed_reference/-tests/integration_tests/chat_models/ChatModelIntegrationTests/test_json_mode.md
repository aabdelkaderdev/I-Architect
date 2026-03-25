<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_json_mode -->

Methodv1.1.4 (latest)●Since v1.1

# test\_json\_mode

Test [structured output]((https://docs.langchain.com/oss/python/langchain/structured-output)) via JSON mode.

This test is optional and should be skipped if the model does not support
the JSON mode feature (see configuration below).

Configuration

To disable this test, set `supports_json_mode` to `False` in your
test class:

```
class TestMyChatModelIntegration(ChatModelIntegrationTests):
    @property
    def supports_json_mode(self) -> bool:
        return False
```

Troubleshooting

See example implementation of `with_structured_output` here: <https://python.langchain.com/api_reference/_modules/langchain_openai/chat_models/base.html#BaseChatOpenAI.with_structured_output>


```
test_json_mode(
    self,
    model: BaseChatModel,
) -> None
```


