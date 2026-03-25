<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_stream_with_model_override -->

Methodv1.1.4 (latest)●Since v1.1

# test\_stream\_with\_model\_override

Test that model name can be overridden at stream time via kwargs.

Test is skipped if `supports_model_override` is `False`.

Troubleshooting

See troubleshooting for `test_invoke_with_model_override`.


```
test_stream_with_model_override(
    self,
    model: BaseChatModel,
) -> None
```


