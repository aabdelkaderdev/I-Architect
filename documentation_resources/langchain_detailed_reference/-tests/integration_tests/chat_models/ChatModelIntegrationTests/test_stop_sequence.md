<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_stop_sequence -->

Methodv1.1.4 (latest)●Since v1.1

# test\_stop\_sequence

Test that model does not fail when invoked with the `stop` parameter.

The `stop` parameter is a standard parameter for stopping generation at a
certain token.

[More on standard parameters](https://python.langchain.com/docs/concepts/chat_models/#standard-parameters).

This should pass for all integrations.

Troubleshooting

If this test fails, check that the function signature for `_generate`
(as well as `_stream` and async variants) accepts the `stop` parameter:

```
def _generate(
    self,
    messages: List[BaseMessage],
    stop: list[str] | None = None,
    run_manager: CallbackManagerForLLMRun | None = None,
    **kwargs: Any,
) -> ChatResult:
```


```
test_stop_sequence(
    self,
    model: BaseChatModel,
) -> None
```


