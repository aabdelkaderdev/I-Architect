<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_tool_message_histories_list_content -->

Methodv1.1.4 (latest)●Since v1.1

# test\_tool\_message\_histories\_list\_content

Test that message histories are compatible with list tool contents.

For instance with Anthropic format contents.

These message histories will include `AIMessage` objects with "tool use" and
content blocks, e.g.,

```
[
    {"type": "text", "text": "Hmm let me think about that"},
    {
        "type": "tool_use",
        "input": {"fav_color": "green"},
        "id": "foo",
        "name": "color_picker",
    },
]
```

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
   `AIMessage` objects with list content.
2. The `tool_calls` attribute on `AIMessage` objects is correctly
   handled and passed to the model in an appropriate format.
3. The model can correctly handle ToolMessage objects with string content
   and arbitrary string values for `tool_call_id`.

You can `xfail` the test if tool calling is implemented but this format
is not supported.

```
@pytest.mark.xfail(reason=("Not implemented."))
def test_tool_message_histories_list_content(self, *args: Any) -> None:
    super().test_tool_message_histories_list_content(*args)
```


```
test_tool_message_histories_list_content(
  self,
  model: BaseChatModel,
  my_adder_tool: BaseTool
) -> None
```


