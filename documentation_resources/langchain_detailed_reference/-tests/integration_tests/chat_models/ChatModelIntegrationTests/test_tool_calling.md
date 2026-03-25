<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_tool_calling -->

Methodv1.1.4 (latest)●Since v1.1

# test\_tool\_calling

Test that the model generates tool calls.

This test is skipped if the `has_tool_calling` property on the test class is
set to `False`.

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
`tool_choice` is not supported and the model consistently fails this
test, you can `xfail` the test:

```
@pytest.mark.xfail(reason=("Does not support tool_choice."))
def test_tool_calling(self, model: BaseChatModel) -> None:
    super().test_tool_calling(model)
```

Otherwise, in the case that only one tool is bound, ensure that
`tool_choice` supports the string `'any'` to force calling that tool.


```
test_tool_calling(
    self,
    model: BaseChatModel,
) -> None
```


