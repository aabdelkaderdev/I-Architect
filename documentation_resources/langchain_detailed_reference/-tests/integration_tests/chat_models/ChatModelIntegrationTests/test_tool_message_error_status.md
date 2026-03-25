<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_tool_message_error_status -->

Methodv1.1.4 (latest)●Since v1.1

# test\_tool\_message\_error\_status

Test that `ToolMessage` with `status="error"` can be handled.

These messages may take the form:

```
ToolMessage(
    "Error: Missing required argument 'b'.",
    name="my_adder_tool",
    tool_call_id="abc123",
    status="error",
)
```

If possible, the `status` field should be parsed and passed appropriately
to the model.

This test is optional and should be skipped if the model does not support
tool calling (see configuration below).

Configuration

To disable tool calling tests, set `has_tool_calling` to `False` in your
test class:

```
class TestMyChatModelIntegration(ChatModelIntegrationTests):
    @property
    def has_tool_calling(self) -> bool:
        return False
```

Troubleshooting

If this test fails, check that the `status` field on `ToolMessage`
objects is either ignored or passed to the model appropriately.


```
test_tool_message_error_status(
  self,
  model: BaseChatModel,
  my_adder_tool: BaseTool
) -> None
```


