<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_stream -->

Methodv1.1.4 (latest)●Since v1.1

# test\_stream

Test to verify that `model.stream(simple_message)` works.

This should pass for all integrations. Passing this test does not indicate
a "streaming" implementation, but rather that the model can be used in a
streaming context.

Troubleshooting

First, debug
`langchain_tests.integration_tests.chat_models.ChatModelIntegrationTests.test_invoke`.
because `stream` has a default implementation that calls `invoke` and
yields the result as a single chunk.

If that test passes but not this one, you should make sure your `_stream`
method does not raise any exceptions, and that it yields valid
`langchain_core.outputs.chat_generation.ChatGenerationChunk`
objects like so:

```
yield ChatGenerationChunk(message=AIMessageChunk(content="chunk text"))
```

The final chunk must have `chunk_position='last'` to signal stream
completion. This enables proper parsing of `tool_call_chunks` into
`tool_calls` on the aggregated message:

```
for i, token in enumerate(tokens):
    is_last = i == len(tokens) - 1
    yield ChatGenerationChunk(
        message=AIMessageChunk(
            content=token,
            chunk_position="last" if is_last else None,
        )
    )
```


```
test_stream(
    self,
    model: BaseChatModel,
) -> None
```


