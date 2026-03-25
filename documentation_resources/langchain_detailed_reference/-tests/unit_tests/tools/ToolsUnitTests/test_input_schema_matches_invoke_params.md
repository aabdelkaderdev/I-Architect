<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/tools/ToolsUnitTests/test_input_schema_matches_invoke_params -->

Methodv1.1.4 (latest)●Since v1.1

# test\_input\_schema\_matches\_invoke\_params

Tests that the provided example params match the declared input schema.

If this fails, update the `tool_invoke_params_example` attribute to match
the input schema (`args_schema`) of the tool.


```
test_input_schema_matches_invoke_params(
    self,
    tool: BaseTool,
) -> None
```


