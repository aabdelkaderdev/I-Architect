<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_structured_few_shot_examples -->

Methodv1.1.4 (latest)●Since v1.1

# test\_structured\_few\_shot\_examples

Test that the model can process few-shot examples with tool calls.

These are represented as a sequence of messages of the following form:

- `HumanMessage` with string content;
- `AIMessage` with the `tool_calls` attribute populated;
- `ToolMessage` with string content;
- `AIMessage` with string content (an answer);
- `HumanMessage` with string content (a follow-up question).

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

If this test fails, check that the model can correctly handle this
sequence of messages.

You can `xfail` the test if tool calling is implemented but this format
is not supported.

```
@pytest.mark.xfail(reason=("Not implemented."))
def test_structured_few_shot_examples(self, *args: Any) -> None:
    super().test_structured_few_shot_examples(*args)
```


```
test_structured_few_shot_examples(
  self,
  model: BaseChatModel,
  my_adder_tool: BaseTool
) -> None
```


