<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/tools/ToolsIntegrationTests/test_invoke_no_tool_call -->

Methodv1.1.4 (latest)●Since v1.1

# test\_invoke\_no\_tool\_call

Test invoke without `ToolCall`.

If invoked without a `ToolCall`, the tool can return anything
but it shouldn't throw an error.

If this test fails, your tool may not be handling the input you defined
in `tool_invoke_params_example` correctly, and it's throwing an error.

This test doesn't have any checks. It's just to ensure that the tool
doesn't throw an error when invoked with a `dict` of `**kwargs`.


```
test_invoke_no_tool_call(
    self,
    tool: BaseTool,
) -> None
```


