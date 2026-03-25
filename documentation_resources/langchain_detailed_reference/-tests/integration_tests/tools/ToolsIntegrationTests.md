<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/tools/ToolsIntegrationTests -->

Classv1.1.4 (latest)●Since v1.1

# ToolsIntegrationTests

Base class for tools integration tests.


```
ToolsIntegrationTests()
```

## Bases

`ToolsTests`

## Methods

[method

test\_invoke\_matches\_output\_schema

Test invoke matches output schema.

If invoked with a `ToolCall`, the tool should return a valid `ToolMessage`
content.

If you have followed the [custom tool guide](https://docs.langchain.com/oss/python/contributing/implement-langchain#tools),
this test should always pass because `ToolCall` inputs are handled by the
`langchain_core.tools.BaseTool` class.

If you have not followed this guide, you should ensure that your tool's
`invoke` method returns a valid ToolMessage content when it receives
a `dict` representing a `ToolCall` as input (as opposed to distinct args).](/python/langchain-tests/integration_tests/tools/ToolsIntegrationTests/test_invoke_matches_output_schema)[method

test\_async\_invoke\_matches\_output\_schema

Test async invoke matches output schema.

If ainvoked with a `ToolCall`, the tool should return a valid `ToolMessage`
content.

For debugging tips, see `test_invoke_matches_output_schema`.](/python/langchain-tests/integration_tests/tools/ToolsIntegrationTests/test_async_invoke_matches_output_schema)[method

test\_invoke\_no\_tool\_call

Test invoke without `ToolCall`.

If invoked without a `ToolCall`, the tool can return anything
but it shouldn't throw an error.

If this test fails, your tool may not be handling the input you defined
in `tool_invoke_params_example` correctly, and it's throwing an error.

This test doesn't have any checks. It's just to ensure that the tool
doesn't throw an error when invoked with a `dict` of `**kwargs`.](/python/langchain-tests/integration_tests/tools/ToolsIntegrationTests/test_invoke_no_tool_call)[method

test\_async\_invoke\_no\_tool\_call

Test async invoke without `ToolCall`.

If ainvoked without a `ToolCall`, the tool can return anything
but it shouldn't throw an error.

For debugging tips, see `test_invoke_no_tool_call`.](/python/langchain-tests/integration_tests/tools/ToolsIntegrationTests/test_async_invoke_no_tool_call)

## Inherited from[ToolsTests](/python/langchain-tests/unit_tests/tools/ToolsTests)

### Attributes

[Atool\_constructor: type[BaseTool] | BaseTool

—

Returns a class or instance of a tool to be tested.](/python/langchain-tests/unit_tests/tools/ToolsTests/tool_constructor)[Atool\_constructor\_params: dict[str, Any]

—

Returns a dictionary of parameters to pass to the tool constructor.](/python/langchain-tests/unit_tests/tools/ToolsTests/tool_constructor_params)[Atool\_invoke\_params\_example: dict[str, Any]

—

Returns a dictionary representing the "args" of an example tool call.](/python/langchain-tests/unit_tests/tools/ToolsTests/tool_invoke_params_example)

### Methods

[Mtool

—

Tool fixture.](/python/langchain-tests/unit_tests/tools/ToolsTests/tool)

## Inherited from[BaseStandardTests](/python/langchain-tests/base/BaseStandardTests)

### Methods

[Mtest\_no\_overrides\_DO\_NOT\_OVERRIDE

—

Test that no standard tests are overridden.](/python/langchain-tests/base/BaseStandardTests/test_no_overrides_DO_NOT_OVERRIDE)


