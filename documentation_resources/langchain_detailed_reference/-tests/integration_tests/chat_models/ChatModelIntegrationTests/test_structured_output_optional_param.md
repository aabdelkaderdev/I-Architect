<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_structured_output_optional_param -->

Methodv1.1.4 (latest)●Since v1.1

# test\_structured\_output\_optional\_param

Test structured output with optional parameters.

Test to verify we can generate structured output that includes optional
parameters.

This test is optional and should be skipped if the model does not support
structured output (see configuration below).

Configuration

To disable structured output tests, set `has_structured_output` to `False`
in your test class:

```
class TestMyChatModelIntegration(ChatModelIntegrationTests):
    @property
    def has_structured_output(self) -> bool:
        return False
```

By default, `has_structured_output` is True if a model overrides the
`with_structured_output` or `bind_tools` methods.

Troubleshooting

If this test fails, ensure that the model's `bind_tools` method
properly handles Pydantic V2 models with optional parameters.

`langchain_core` implements a [utility function](https://reference.langchain.com/python/langchain_core/utils/?h=convert_to_op#langchain_core.utils.function_calling.convert_to_openai_tool).
that will accommodate most formats.

See [example implementation](https://github.com/langchain-ai/langchain/blob/master/libs/partners/openai/langchain_openai/chat_models/base.py).
of `with_structured_output`.


```
test_structured_output_optional_param(
    self,
    model: BaseChatModel,
) -> None
```


