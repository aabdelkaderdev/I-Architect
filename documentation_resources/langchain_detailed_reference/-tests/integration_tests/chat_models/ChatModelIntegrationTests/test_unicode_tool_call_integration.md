<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_unicode_tool_call_integration -->

Methodv1.1.4 (latest)●Since v1.1

# test\_unicode\_tool\_call\_integration

Generic integration test for Unicode characters in tool calls.


```
test_unicode_tool_call_integration(
  self,
  model: BaseChatModel,
  *,
  tool_choice: str | None = None,
  force_tool_call: bool = True
) -> None
```

Tests that Unicode characters in tool call arguments are preserved correctly,
not escaped as `\\uXXXX` sequences.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `model`\* | `BaseChatModel` | The chat model to test |
| `tool_choice` | `str | None` | Default:`None`  Tool choice parameter to pass to `bind_tools()` (provider-specific) |
| `force_tool_call` | `bool` | Default:`True`  Whether to force a tool call (use `tool_choice=True` if None) |


