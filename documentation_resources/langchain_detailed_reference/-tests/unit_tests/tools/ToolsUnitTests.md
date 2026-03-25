<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/tools/ToolsUnitTests -->

Classv1.1.4 (latest)●Since v1.1

# ToolsUnitTests


```
ToolsUnitTests()
```

## Bases

`ToolsTests`

## Attributes

## Methods

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

[attribute

init\_from\_env\_params: tuple[dict[str, str], dict[str, Any], dict[str, Any]]](/python/langchain-tests/unit_tests/tools/ToolsUnitTests/init_from_env_params)

[method

test\_init](/python/langchain-tests/unit_tests/tools/ToolsUnitTests/test_init)

[method

test\_init\_from\_env](/python/langchain-tests/unit_tests/tools/ToolsUnitTests/test_init_from_env)

[method

test\_has\_name](/python/langchain-tests/unit_tests/tools/ToolsUnitTests/test_has_name)

[method

test\_has\_input\_schema](/python/langchain-tests/unit_tests/tools/ToolsUnitTests/test_has_input_schema)

[method

test\_input\_schema\_matches\_invoke\_params](/python/langchain-tests/unit_tests/tools/ToolsUnitTests/test_input_schema_matches_invoke_params)

Base class for tools unit tests.

Init from env params.

Return env vars, init args, and expected instance attrs for initializing
from env vars.

Test init.

Test that the tool can be initialized with `tool_constructor` and
`tool_constructor_params`. If this fails, check that the
keyword args defined in `tool_constructor_params` are valid.

Test that the tool can be initialized from environment variables.

Tests that the tool has a name attribute to pass to chat models.

If this fails, add a `name` parameter to your tool.

Tests that the tool has an input schema.

If this fails, add an `args_schema` to your tool.

See [this guide](https://docs.langchain.com/oss/python/contributing/implement-langchain#tools)
and see how `CalculatorInput` is configured in the
`CustomCalculatorTool.args_schema` attribute

Tests that the provided example params match the declared input schema.

If this fails, update the `tool_invoke_params_example` attribute to match
the input schema (`args_schema`) of the tool.