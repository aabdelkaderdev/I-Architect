<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/tools/ToolsIntegrationTests/test_async_invoke_matches_output_schema -->

Methodv1.1.4 (latest)●Since v1.1

# test\_async\_invoke\_matches\_output\_schema

Test async invoke matches output schema.

If ainvoked with a `ToolCall`, the tool should return a valid `ToolMessage`
content.

For debugging tips, see `test_invoke_matches_output_schema`.


```
test_async_invoke_matches_output_schema(
    self,
    tool: BaseTool,
) -> None
```


