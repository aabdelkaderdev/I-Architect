<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_astream -->

Methodv1.1.4 (latest)●Since v1.1

# test\_astream

Test to verify that `await model.astream(simple_message)` works.

This should pass for all integrations. Passing this test does not indicate
a "natively async" or "streaming" implementation, but rather that the model can
be used in an async streaming context.

Troubleshooting

First, debug
`langchain_tests.integration_tests.chat_models.ChatModelIntegrationTests.test_stream`.
and
`langchain_tests.integration_tests.chat_models.ChatModelIntegrationTests.test_ainvoke`.
because `astream` has a default implementation that calls `_stream` in
an async context if it is implemented, or `ainvoke` and yields the result
as a single chunk if not.

If those tests pass but not this one, you should make sure your `_astream`
method does not raise any exceptions, and that it yields valid
`langchain_core.outputs.chat_generation.ChatGenerationChunk`
objects like so:

```
yield ChatGenerationChunk(message=AIMessageChunk(content="chunk text"))
```

See `test_stream` troubleshooting for `chunk_position` requirements.


```
test_astream(
    self,
    model: BaseChatModel,
) -> None
```


