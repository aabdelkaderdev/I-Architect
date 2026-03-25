<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_bind_runnables_as_tools -->

Methodv1.1.4 (latest)●Since v1.1

# test\_bind\_runnables\_as\_tools

Test bind runnables as tools.

Test that the model generates tool calls for tools that are derived from
LangChain runnables. This test is skipped if the `has_tool_calling` property
on the test class is set to `False`.

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

If this test fails, check that `bind_tools` is implemented to correctly
translate LangChain tool objects into the appropriate schema for your
chat model.

This test may fail if the chat model does not support a `tool_choice`
parameter. This parameter can be used to force a tool call. If
`tool_choice` is not supported, set `has_tool_choice` to `False` in
your test class:

```
@property
def has_tool_choice(self) -> bool:
    return False
```


```
test_bind_runnables_as_tools(
    self,
    model: BaseChatModel,
) -> None
```


