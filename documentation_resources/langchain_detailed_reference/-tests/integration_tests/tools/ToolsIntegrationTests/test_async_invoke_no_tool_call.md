<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/tools/ToolsIntegrationTests/test_async_invoke_no_tool_call -->

Methodv1.1.4 (latest)●Since v1.1

# test\_async\_invoke\_no\_tool\_call

Test async invoke without `ToolCall`.

If ainvoked without a `ToolCall`, the tool can return anything
but it shouldn't throw an error.

For debugging tips, see `test_invoke_no_tool_call`.


```
test_async_invoke_no_tool_call(
    self,
    tool: BaseTool,
) -> None
```


