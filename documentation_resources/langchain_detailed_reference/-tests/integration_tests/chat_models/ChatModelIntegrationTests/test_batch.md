<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_batch -->

Methodv1.1.4 (latest)●Since v1.1

# test\_batch

Test to verify that `model.batch([messages])` works.

This should pass for all integrations. Tests the model's ability to process
multiple prompts in a single batch.

Troubleshooting

First, debug
`langchain_tests.integration_tests.chat_models.ChatModelIntegrationTests.test_invoke`
because `batch` has a default implementation that calls `invoke` for
each message in the batch.

If that test passes but not this one, you should make sure your `batch`
method does not raise any exceptions, and that it returns a list of valid
`AIMessage` objects.


```
test_batch(
    self,
    model: BaseChatModel,
) -> None
```


