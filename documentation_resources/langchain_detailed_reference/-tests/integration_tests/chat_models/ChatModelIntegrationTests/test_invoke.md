<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_invoke -->

Methodv1.1.4 (latest)●Since v1.1

# test\_invoke

Test to verify that `model.invoke(simple_message)` works.

This should pass for all integrations.

Troubleshooting

If this test fails, you should make sure your `_generate` method
does not raise any exceptions, and that it returns a valid
`langchain_core.outputs.chat_result.ChatResult` like so:

```
return ChatResult(
    generations=[ChatGeneration(message=AIMessage(content="Output text"))]
)
```


```
test_invoke(
    self,
    model: BaseChatModel,
) -> None
```


