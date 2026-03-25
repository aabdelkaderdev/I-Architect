<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_bind_tool_pydantic -->

Methodv1.1.4 (latest)●Since v1.1

# test\_bind\_tool\_pydantic

Test bind tools with Pydantic models.

Test that chat model correctly handles Pydantic models that are passed
into `bind_tools`. Test is skipped if the `has_tool_calling` property
on the test class is False.

Troubleshooting

If this test fails, ensure that the model's `bind_tools` method
properly handles Pydantic V2 models.

`langchain_core` implements a [utility function](https://reference.langchain.com/python/langchain_core/utils/?h=convert_to_op#langchain_core.utils.function_calling.convert_to_openai_tool).
that will accommodate most formats.

See [example implementation](https://github.com/langchain-ai/langchain/blob/master/libs/partners/openai/langchain_openai/chat_models/base.py).
of `with_structured_output`.


```
test_bind_tool_pydantic(
  self,
  model: BaseChatModel,
  my_adder_tool: BaseTool
) -> None
```


