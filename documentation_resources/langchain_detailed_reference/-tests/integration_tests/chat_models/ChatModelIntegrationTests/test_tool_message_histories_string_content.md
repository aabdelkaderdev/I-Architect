<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_tool_message_histories_string_content -->

Methodv1.1.4 (latest)●Since v1.1

# test\_tool\_message\_histories\_string\_content

Test that message histories are compatible with string tool contents.

For instance with OpenAI format contents.
If a model passes this test, it should be compatible
with messages generated from providers following OpenAI format.

This test should be skipped if the model does not support tool calling
(see configuration below).

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

If this test fails, check that:

1. The model can correctly handle message histories that include
   `AIMessage` objects with `""` content.
2. The `tool_calls` attribute on `AIMessage` objects is correctly
   handled and passed to the model in an appropriate format.
3. The model can correctly handle `ToolMessage` objects with string
   content and arbitrary string values for `tool_call_id`.

You can `xfail` the test if tool calling is implemented but this format
is not supported.

```
@pytest.mark.xfail(reason=("Not implemented."))
def test_tool_message_histories_string_content(self, *args: Any) -> None:
    super().test_tool_message_histories_string_content(*args)
```


```
test_tool_message_histories_string_content(
  self,
  model: BaseChatModel,
  my_adder_tool: BaseTool
) -> None
```


