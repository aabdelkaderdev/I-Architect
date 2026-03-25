<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/tools/ToolsIntegrationTests/test_invoke_matches_output_schema -->

Methodv1.1.4 (latest)●Since v1.1

# test\_invoke\_matches\_output\_schema

Test invoke matches output schema.

If invoked with a `ToolCall`, the tool should return a valid `ToolMessage`
content.

If you have followed the [custom tool guide](https://docs.langchain.com/oss/python/contributing/implement-langchain#tools),
this test should always pass because `ToolCall` inputs are handled by the
`langchain_core.tools.BaseTool` class.

If you have not followed this guide, you should ensure that your tool's
`invoke` method returns a valid ToolMessage content when it receives
a `dict` representing a `ToolCall` as input (as opposed to distinct args).


```
test_invoke_matches_output_schema(
    self,
    tool: BaseTool,
) -> None
```


