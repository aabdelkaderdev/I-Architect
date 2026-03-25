<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_agent_loop -->

Methodv1.1.4 (latest)●Since v1.1

# test\_agent\_loop

Test that the model supports a simple ReAct agent loop.

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

Check also that all required information (e.g., tool calling identifiers)
from `AIMessage` objects is propagated correctly to model payloads.

This test may fail if the chat model does not consistently generate tool
calls in response to an appropriate query. In these cases you can `xfail`
the test:

```
@pytest.mark.xfail(reason=("Does not support tool_choice."))
def test_agent_loop(self, model: BaseChatModel) -> None:
    super().test_agent_loop(model)
```


```
test_agent_loop(
    self,
    model: BaseChatModel,
) -> None
```


