<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_ainvoke -->

Methodv1.1.4 (latest)●Since v1.1

# test\_ainvoke

Test to verify that `await model.ainvoke(simple_message)` works.

This should pass for all integrations. Passing this test does not indicate
a "natively async" implementation, but rather that the model can be used
in an async context.

Troubleshooting

First, debug
`langchain_tests.integration_tests.chat_models.ChatModelIntegrationTests.test_invoke`.
because `ainvoke` has a default implementation that calls `invoke` in an
async context.

If that test passes but not this one, you should make sure your `_agenerate`
method does not raise any exceptions, and that it returns a valid
`langchain_core.outputs.chat_result.ChatResult` like so:

```
return ChatResult(
    generations=[ChatGeneration(message=AIMessage(content="Output text"))]
)
```


```
test_ainvoke(
    self,
    model: BaseChatModel,
) -> None
```


