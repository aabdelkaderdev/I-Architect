<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/tools/ToolsUnitTests/test_has_input_schema -->

Methodv1.1.4 (latest)●Since v1.1

# test\_has\_input\_schema


```
test_has_input_schema(
    self,
    tool: BaseTool,
) -> None
```



Tests that the tool has an input schema.

If this fails, add an `args_schema` to your tool.

See [this guide](https://docs.langchain.com/oss/python/contributing/implement-langchain#tools)
and see how `CalculatorInput` is configured in the
`CustomCalculatorTool.args_schema` attribute