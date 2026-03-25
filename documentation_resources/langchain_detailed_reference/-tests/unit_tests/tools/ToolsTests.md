<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/tools/ToolsTests -->

Classv1.1.4 (latest)●Since v1.1

# ToolsTests

Base class for testing tools.

This won't show in the documentation, but the docstrings will be inherited by
subclasses.


```
ToolsTests()
```

## Bases

`BaseStandardTests`

## Attributes

[attribute

tool\_constructor: type[BaseTool] | BaseTool

Returns a class or instance of a tool to be tested.](/python/langchain-tests/unit_tests/tools/ToolsTests/tool_constructor)[attribute

tool\_constructor\_params: dict[str, Any]

Returns a dictionary of parameters to pass to the tool constructor.](/python/langchain-tests/unit_tests/tools/ToolsTests/tool_constructor_params)[attribute

tool\_invoke\_params\_example: dict[str, Any]

Returns a dictionary representing the "args" of an example tool call.

This should NOT be a `ToolCall` dict - it should not have
`{"name", "id", "args"}` keys.](/python/langchain-tests/unit_tests/tools/ToolsTests/tool_invoke_params_example)

## Methods

[method

tool

Tool fixture.](/python/langchain-tests/unit_tests/tools/ToolsTests/tool)

## Inherited from[BaseStandardTests](/python/langchain-tests/base/BaseStandardTests)

### Methods

[Mtest\_no\_overrides\_DO\_NOT\_OVERRIDE

—

Test that no standard tests are overridden.](/python/langchain-tests/base/BaseStandardTests/test_no_overrides_DO_NOT_OVERRIDE)


