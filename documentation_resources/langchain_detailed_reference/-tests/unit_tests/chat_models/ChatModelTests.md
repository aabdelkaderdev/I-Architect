<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/chat_models/ChatModelTests -->

Classv1.1.4 (latest)●Since v1.1

# ChatModelTests

Base class for chat model tests.


```
ChatModelTests()
```

## Bases

`BaseStandardTests`

## Attributes

[attribute

chat\_model\_class: type[BaseChatModel]

The chat model class to test, e.g., `ChatParrotLink`.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/chat_model_class)[attribute

chat\_model\_params: dict[str, Any]

Initialization parameters for the chat model.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/chat_model_params)[attribute

standard\_chat\_model\_params: dict[str, Any]

Standard chat model parameters.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/standard_chat_model_params)[attribute

has\_tool\_calling: bool

Whether the model supports tool calling.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/has_tool_calling)[attribute

has\_tool\_choice: bool

Whether the model supports tool calling.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/has_tool_choice)[attribute

has\_structured\_output: bool

Whether the chat model supports structured output.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/has_structured_output)[attribute

structured\_output\_kwargs: dict[str, Any]

Additional kwargs to pass to `with_structured_output()` in tests.

Override this property to customize how structured output is generated
for your model. The most common use case is specifying the `method`
parameter, which controls the mechanism used to enforce structured output:

- `'function_calling'`: Uses tool/function calling to enforce the schema.
- `'json_mode'`: Uses the model's JSON mode.
- `'json_schema'`: Uses native JSON schema support (e.g., OpenAI's
  structured outputs).](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/structured_output_kwargs)[attribute

supports\_json\_mode: bool

Whether the chat model supports JSON mode.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_json_mode)[attribute

supports\_image\_inputs: bool

Supports image inputs.

Whether the chat model supports image inputs, defaults to
`False`.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_image_inputs)[attribute

supports\_image\_urls: bool

Supports image inputs from URLs.

Whether the chat model supports image inputs from URLs, defaults to
`False`.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_image_urls)[attribute

supports\_pdf\_inputs: bool

Whether the chat model supports PDF inputs, defaults to `False`.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_pdf_inputs)[attribute

supports\_audio\_inputs: bool

Supports audio inputs.

Whether the chat model supports audio inputs, defaults to `False`.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_audio_inputs)[attribute

supports\_video\_inputs: bool

Supports video inputs.

Whether the chat model supports video inputs, defaults to `False`.

No current tests are written for this feature.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_video_inputs)[attribute

returns\_usage\_metadata: bool

Returns usage metadata.

Whether the chat model returns usage metadata on invoke and streaming
responses.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/returns_usage_metadata)[attribute

supports\_anthropic\_inputs: bool

Whether the chat model supports Anthropic-style inputs.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_anthropic_inputs)[attribute

supports\_image\_tool\_message: bool

Supports image `ToolMessage` objects.

Whether the chat model supports `ToolMessage` objects that include image
content.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_image_tool_message)[attribute

supports\_pdf\_tool\_message: bool

Supports PDF `ToolMessage` objects.

Whether the chat model supports `ToolMessage` objects that include PDF
content.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_pdf_tool_message)[attribute

enable\_vcr\_tests: bool

Whether to enable VCR tests for the chat model.

Warning

See `enable_vcr_tests` dropdown `above <ChatModelTests>` for more
information.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/enable_vcr_tests)[attribute

supported\_usage\_metadata\_details: dict[Literal['invoke', 'stream'], list[Literal['audio\_input', 'audio\_output', 'reasoning\_output', 'cache\_read\_input', 'cache\_creation\_input']]]

Supported usage metadata details.

What usage metadata details are emitted in invoke and stream. Only needs to be
overridden if these details are returned by the model.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supported_usage_metadata_details)[attribute

supports\_model\_override: bool

Whether the model supports overriding the model name at runtime.

Defaults to `True`.

If `True`, the model accepts a `model` kwarg in `invoke()`, `stream()`,
etc. that overrides the model specified at initialization.

This enables dynamic model selection without creating new instances.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_model_override)[attribute

model\_override\_value: str | None

Alternative model name to use when testing model override.

Should return a valid model name that differs from the default model.
Required if `supports_model_override` is `True`.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/model_override_value)

## Methods

[method

model

Model fixture.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/model)[method

my\_adder\_tool

Adder tool fixture.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/my_adder_tool)

## Inherited from[BaseStandardTests](/python/langchain-tests/base/BaseStandardTests)

### Methods

[Mtest\_no\_overrides\_DO\_NOT\_OVERRIDE

—

Test that no standard tests are overridden.](/python/langchain-tests/base/BaseStandardTests/test_no_overrides_DO_NOT_OVERRIDE)


