<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_tool_choice -->

Methodv1.1.4 (latest)●Since v1.1

# test\_tool\_choice

Test `tool_choice` parameter.

Test that the model can force tool calling via the `tool_choice`
parameter. This test is skipped if the `has_tool_choice` property on the
test class is set to `False`.

This test is optional and should be skipped if the model does not support
tool calling (see configuration below).

Configuration

To disable tool calling tests, set `has_tool_choice` to `False` in your
test class:

```
class TestMyChatModelIntegration(ChatModelIntegrationTests):
    @property
    def has_tool_choice(self) -> bool:
        return False
```

Troubleshooting

If this test fails, check whether the `test_tool_calling` test is passing.
If it is not, refer to the troubleshooting steps in that test first.

If `test_tool_calling` is passing, check that the underlying model
supports forced tool calling. If it does, `bind_tools` should accept a
`tool_choice` parameter that can be used to force a tool call.

It should accept (1) the string `'any'` to force calling the bound tool,
and (2) the string name of the tool to force calling that tool.


```
test_tool_choice(
    self,
    model: BaseChatModel,
) -> None
```


