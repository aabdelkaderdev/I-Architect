<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests -->

Classv1.1.4 (latest)●Since v1.1

# ChatModelUnitTests

Base class for chat model unit tests.

Test subclasses must implement the `chat_model_class` and
`chat_model_params` properties to specify what model to test and its
initialization parameters.

```
from typing import Type

from langchain_tests.unit_tests import ChatModelUnitTests
from my_package.chat_models import MyChatModel

class TestMyChatModelUnit(ChatModelUnitTests):
    @property
    def chat_model_class(self) -> Type[MyChatModel]:
        # Return the chat model class to test here
        return MyChatModel

    @property
    def chat_model_params(self) -> dict:
        # Return initialization parameters for the model.
        return {"model": "model-001", "temperature": 0}
```

Note

API references for individual test methods include troubleshooting tips.

Test subclasses **must** implement the following two properties:

`chat_model_class`: The chat model class to test, e.g., `ChatParrotLink`.

```
@property
def chat_model_class(self) -> Type[ChatParrotLink]:
    return ChatParrotLink
```

`chat_model_params`: Initialization parameters for the chat model.

```
@property
def chat_model_params(self) -> dict:
    return {"model": "bird-brain-001", "temperature": 0}
```

In addition, test subclasses can control what features are tested (such as tool
calling or multi-modality) by selectively overriding the following properties.

Expand to see details:

`has_tool_calling`

Boolean property indicating whether the chat model supports tool calling.

By default, this is determined by whether the chat model's `bind_tools` method
is overridden. It typically does not need to be overridden on the test class.

```
@property
def has_tool_calling(self) -> bool:
    return True
```

`has_tool_choice`

Boolean property indicating whether the chat model supports forcing tool
calling via a `tool_choice` parameter.

By default, this is determined by whether the parameter is included in the
signature for the corresponding `bind_tools` method.

If `True`, the minimum requirement for this feature is that
`tool_choice='any'` will force a tool call, and `tool_choice=<tool name>`
will force a call to a specific tool.

```
@property
def has_tool_choice(self) -> bool:
    return False
```

`has_structured_output`

Boolean property indicating whether the chat model supports structured
output.

By default, this is determined by whether the chat model overrides the
`with_structured_output` or `bind_tools` methods. If the base
implementations are intended to be used, this method should be overridden.

See docs for [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output).

```
@property
def has_structured_output(self) -> bool:
    return True
```

`structured_output_kwargs`

Dict property specifying additional kwargs to pass to
`with_structured_output()` when running structured output tests.

Override this to customize how your model generates structured output.

The most common use case is specifying the `method` parameter:

- `'function_calling'`: Uses tool/function calling to enforce the schema.
- `'json_mode'`: Uses the model's JSON mode.
- `'json_schema'`: Uses native JSON schema support (e.g., OpenAI's structured
  outputs).

```
@property
def structured_output_kwargs(self) -> dict:
    return {"method": "json_schema"}
```

`supports_json_mode`

Boolean property indicating whether the chat model supports
`method='json_mode'` in `with_structured_output`.

JSON mode constrains the model to output valid JSON without enforcing
a specific schema (unlike `'function_calling'` or `'json_schema'` methods).

When using JSON mode, you must prompt the model to output JSON in your
message.

Example:

```
structured_llm = llm.with_structured_output(MySchema, method="json_mode")
structured_llm.invoke("... Return the result as JSON.")
```

See docs for [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output).

Defaults to `False`.

```
@property
def supports_json_mode(self) -> bool:
    return True
```

`supports_image_inputs`

Boolean property indicating whether the chat model supports image inputs.

Defaults to `False`.

If set to `True`, the chat model will be tested using the LangChain
`ImageContentBlock` format:

```
{
    "type": "image",
    "base64": "<base64 image data>",
    "mime_type": "image/jpeg",  # or appropriate MIME type
}
```

In addition to OpenAI Chat Completions `image_url` blocks:

```
{
    "type": "image_url",
    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
}
```

See docs for [Multimodality](https://docs.langchain.com/oss/python/langchain/models#multimodal).

```
@property
def supports_image_inputs(self) -> bool:
    return True
```

`supports_image_urls`

Boolean property indicating whether the chat model supports image inputs from
URLs.

Defaults to `False`.

If set to `True`, the chat model will be tested using content blocks of the
form.

```
{
    "type": "image",
    "url": "https://...",
}
```

See docs for [Multimodality](https://docs.langchain.com/oss/python/langchain/models#multimodal).

```
@property
def supports_image_urls(self) -> bool:
    return True
```

`supports_image_tool_message`

Boolean property indicating whether the chat model supports a `ToolMessage`
that includes image content, e.g. in the OpenAI Chat Completions format.

Defaults to `False`.

```
ToolMessage(
    content=[
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
        },
    ],
    tool_call_id="1",
    name="random_image",
)
```

(OpenAI Chat Completions format), as well as LangChain's `ImageContentBlock`
format:

```
ToolMessage(
    content=[
        {
            "type": "image",
            "base64": image_data,
            "mime_type": "image/jpeg",
        },
    ],
    tool_call_id="1",
    name="random_image",
)
```

(standard format).

If set to `True`, the chat model will be tested with message sequences that
include `ToolMessage` objects of this form.

```
@property
def supports_image_tool_message(self) -> bool:
    return True
```

`supports_pdf_inputs`

Boolean property indicating whether the chat model supports PDF inputs.

Defaults to `False`.

If set to `True`, the chat model will be tested using the LangChain
`FileContentBlock` format:

```
{
    "type": "file",
    "base64": "<base64 file data>",
    "mime_type": "application/pdf",
}
```

See docs for [Multimodality](https://docs.langchain.com/oss/python/langchain/models#multimodal).

```
@property
def supports_pdf_inputs(self) -> bool:
    return True
```

`supports_pdf_tool_message`

Boolean property indicating whether the chat model supports a `ToolMessage`
that includes PDF content using the LangChain `FileContentBlock` format.

Defaults to `False`.

```
ToolMessage(
    content=[
        {
            "type": "file",
            "base64": pdf_data,
            "mime_type": "application/pdf",
        },
    ],
    tool_call_id="1",
    name="random_pdf",
)
```

using LangChain's `FileContentBlock` format.

If set to `True`, the chat model will be tested with message sequences that
include `ToolMessage` objects of this form.

```
@property
def supports_pdf_tool_message(self) -> bool:
    return True
```

`supports_audio_inputs`

Boolean property indicating whether the chat model supports audio inputs.

Defaults to `False`.

If set to `True`, the chat model will be tested using the LangChain
`AudioContentBlock` format:

```
{
    "type": "audio",
    "base64": "<base64 audio data>",
    "mime_type": "audio/wav",  # or appropriate MIME type
}
```

See docs for [Multimodality](https://docs.langchain.com/oss/python/langchain/models#multimodal).

```
@property
def supports_audio_inputs(self) -> bool:
    return True
```

Warning

This test downloads audio data from wikimedia.org. You may need to set the
`LANGCHAIN_TESTS_USER_AGENT` environment variable to identify these tests,
e.g.,

```
export LANGCHAIN_TESTS_USER_AGENT="CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org) generic-library/0.0"
```

Refer to the [Wikimedia Foundation User-Agent Policy](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy).

`supports_video_inputs`

Boolean property indicating whether the chat model supports image inputs.

Defaults to `False`.

No current tests are written for this feature.

`returns_usage_metadata`

Boolean property indicating whether the chat model returns usage metadata
on invoke and streaming responses.

Defaults to `True`.

`usage_metadata` is an optional dict attribute on `AIMessage` objects that track
input and output tokens.

[See more](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.messages.ai.UsageMetadata).

```
@property
def returns_usage_metadata(self) -> bool:
    return False
```

Models supporting `usage_metadata` should also return the name of the
underlying model in the `response_metadata` of the `AIMessage`.

`supports_anthropic_inputs`

Boolean property indicating whether the chat model supports Anthropic-style
inputs.

These inputs might feature "tool use" and "tool result" content blocks, e.g.,

```
[
    {"type": "text", "text": "Hmm let me think about that"},
    {
        "type": "tool_use",
        "input": {"fav_color": "green"},
        "id": "foo",
        "name": "color_picker",
    },
]
```

If set to `True`, the chat model will be tested using content blocks of this
form.

```
@property
def supports_anthropic_inputs(self) -> bool:
    return False
```

`supported_usage_metadata_details`

Property controlling what usage metadata details are emitted in both `invoke`
and `stream`.

`usage_metadata` is an optional dict attribute on `AIMessage` objects that track
input and output tokens.

[See more](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.messages.ai.UsageMetadata).

It includes optional keys `input_token_details` and `output_token_details`
that can track usage details associated with special types of tokens, such as
cached, audio, or reasoning.

Only needs to be overridden if these details are supplied.

`supports_model_override`

Boolean property indicating whether the chat model supports overriding the
model name at runtime via kwargs.

If `True`, the model accepts a `model` kwarg in `invoke()`, `stream()`, etc.
that overrides the model specified at initialization. This enables dynamic
model selection without creating new chat model instances.

Defaults to `False`.

```
@property
def supports_model_override(self) -> bool:
    return True
```

`model_override_value`

Alternative model name to use when testing model override.

Should return a valid model name that differs from the default model.
Required if `supports_model_override` is `True`.

```
@property
def model_override_value(self) -> str:
    return "gpt-4o-mini"  # e.g. if default is "gpt-4o"
```

`enable_vcr_tests`

Property controlling whether to enable select tests that rely on
[VCR](https://vcrpy.readthedocs.io/en/latest/) caching of HTTP calls, such
as benchmarking tests.

To enable these tests, follow these steps:

1. Override the `enable_vcr_tests` property to return `True`:

```
@property
def enable_vcr_tests(self) -> bool:
    return True
```

2. Configure VCR to exclude sensitive headers and other information from
   cassettes.

Warning

VCR will by default record authentication headers and other sensitive
information in cassettes. Read below for how to configure what
information is recorded in cassettes.

To add configuration to VCR, add a `conftest.py` file to the `tests/`
directory and implement the `vcr_config` fixture there.

`langchain-tests` excludes the headers `'authorization'`,
`'x-api-key'`, and `'api-key'` from VCR cassettes. To pick up this
configuration, you will need to add `conftest.py` as shown below. You can
also exclude additional headers, override the default exclusions, or apply
other customizations to the VCR configuration. See example below:

```
import pytest
from langchain_tests.conftest import base_vcr_config

_EXTRA_HEADERS = [
    # Specify additional headers to redact
    ("user-agent", "PLACEHOLDER"),
]

def remove_response_headers(response: dict) -> dict:
    # If desired, remove or modify headers in the response.
    response["headers"] = {}
    return response

@pytest.fixture(scope="session")
def vcr_config() -> dict:
    """Extend the default configuration from langchain_tests."""
    config = base_vcr_config()
    config.setdefault("filter_headers", []).extend(_EXTRA_HEADERS)
    config["before_record_response"] = remove_response_headers

    return config
```

Compressing cassettes

`langchain-tests` includes a custom VCR serializer that compresses
cassettes using gzip. To use it, register the `yaml.gz` serializer
to your VCR fixture and enable this serializer in the config. See
example below:

```
import pytest
from langchain_tests.conftest import (
    CustomPersister,
    CustomSerializer,
)
from langchain_tests.conftest import base_vcr_config
from vcr import VCR

_EXTRA_HEADERS = [
    # Specify additional headers to redact
    ("user-agent", "PLACEHOLDER"),
]

def remove_response_headers(response: dict) -> dict:
    # If desired, remove or modify headers in the response.
    response["headers"] = {}
    return response

@pytest.fixture(scope="session")
def vcr_config() -> dict:
    """Extend the default configuration from langchain_tests."""
    config = base_vcr_config()
    config.setdefault("filter_headers", []).extend(_EXTRA_HEADERS)
    config["before_record_response"] = remove_response_headers
    # New: enable serializer and set file extension
    config["serializer"] = "yaml.gz"
    config["path_transformer"] = VCR.ensure_suffix(".yaml.gz")

    return config

def pytest_recording_configure(config: dict, vcr: VCR) -> None:
    vcr.register_persister(CustomPersister())
    vcr.register_serializer("yaml.gz", CustomSerializer())
```

You can inspect the contents of the compressed cassettes (e.g., to
ensure no sensitive information is recorded) using

```
gunzip -k /path/to/tests/cassettes/TestClass_test.yaml.gz
```

...or by using the serializer:

```
from langchain_tests.conftest import (
    CustomPersister,
    CustomSerializer,
)

cassette_path = "/path/to/tests/cassettes/TestClass_test.yaml.gz"
requests, responses = CustomPersister().load_cassette(
    path, CustomSerializer()
)
```

3. Run tests to generate VCR cassettes.

```
uv run python -m pytest tests/integration_tests/test_chat_models.py::TestMyModel::test_stream_time
```

```
This will generate a VCR cassette for the test in
`tests/integration_tests/cassettes/`.
```

Warning

You should inspect the generated cassette to ensure that it does not
contain sensitive information. If it does, you can modify the
`vcr_config` fixture to exclude headers or modify the response
before it is recorded.

```
You can then commit the cassette to your repository. Subsequent test runs
will use the cassette instead of making HTTP calls.
```

**Testing initialization from environment variables**

Some unit tests may require testing initialization from environment variables.
These tests can be enabled by overriding the `init_from_env_params`
property (see below).

`init_from_env_params`

This property is used in unit tests to test initialization from
environment variables. It should return a tuple of three dictionaries
that specify the environment variables, additional initialization args,
and expected instance attributes to check.

Defaults to empty dicts. If not overridden, the test is skipped.

Example:

```
@property
def init_from_env_params(self) -> Tuple[dict, dict, dict]:
    return (
        {
            "MY_API_KEY": "api_key",
        },
        {
            "model": "bird-brain-001",
        },
        {
            "my_api_key": "api_key",
        },
    )
```


```
ChatModelUnitTests()
```

## Bases

`ChatModelTests`

## Attributes

[attribute

standard\_chat\_model\_params: dict[str, Any]

Standard chat model parameters.](/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/standard_chat_model_params)[attribute

init\_from\_env\_params: tuple[dict[str, str], dict[str, Any], dict[str, Any]]

Init from env params.

Environment variables, additional initialization args, and expected instance
attributes for testing initialization from environment variables.](/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/init_from_env_params)

## Methods

[method

test\_init

Test model initialization. This should pass for all integrations.

Troubleshooting

If this test fails, ensure that:

1. `chat_model_params` is specified and the model can be initialized
   from those params;
2. The model accommodates
   [standard parameters](https://docs.langchain.com/oss/python/langchain/models#parameters).](/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_init)[method

test\_init\_from\_env

Test initialization from environment variables.

Relies on the `init_from_env_params` property. Test is skipped if that
property is not set.

Troubleshooting

If this test fails, ensure that `init_from_env_params` is specified
correctly and that model parameters are properly set from environment
variables during initialization.](/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_init_from_env)[method

test\_init\_streaming

Test that model can be initialized with `streaming=True`.

This is for backward-compatibility purposes.

Troubleshooting

If this test fails, ensure that the model can be initialized with a
boolean `streaming` parameter.](/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_init_streaming)[method

test\_bind\_tool\_pydantic

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
of `with_structured_output`.](/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_bind_tool_pydantic)[method

test\_with\_structured\_output

Test `with_structured_output` method.

Test is skipped if the `has_structured_output` property on the test class is
False.

Troubleshooting

If this test fails, ensure that the model's `bind_tools` method
properly handles Pydantic V2 models.

`langchain_core` implements a [utility function](https://reference.langchain.com/python/langchain_core/utils/?h=convert_to_op#langchain_core.utils.function_calling.convert_to_openai_tool).
that will accommodate most formats.

See [example implementation](https://github.com/langchain-ai/langchain/blob/master/libs/partners/openai/langchain_openai/chat_models/base.py).
of `with_structured_output`.](/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_with_structured_output)[method

test\_standard\_params

Test that model properly generates standard parameters.

These are used for tracing purposes.

Troubleshooting

If this test fails, check that the model accommodates [standard parameters](https://docs.langchain.com/oss/python/langchain/models#parameters).

Check also that the model class is named according to convention
(e.g., `ChatProviderName`).](/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_standard_params)[method

test\_serdes

Test serialization and deserialization of the model.

Test is skipped if the `is_lc_serializable` property on the chat model class
is not overwritten to return `True`.

Troubleshooting

If this test fails, check that the `init_from_env_params` property is
correctly set on the test class.](/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_serdes)[method

test\_init\_time

Test initialization time of the chat model.

If this test fails, check that
we are not introducing undue overhead in the model's initialization.](/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_init_time)

## Inherited from[ChatModelTests](/python/langchain-tests/unit_tests/chat_models/ChatModelTests)

### Attributes

[Achat\_model\_class: type[BaseChatModel]

—

The chat model class to test, e.g., `ChatParrotLink`.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/chat_model_class)[Achat\_model\_params: dict[str, Any]

—

Initialization parameters for the chat model.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/chat_model_params)[Ahas\_tool\_calling: bool

—

Whether the model supports tool calling.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/has_tool_calling)[Ahas\_tool\_choice: bool

—

Whether the model supports tool calling.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/has_tool_choice)[Ahas\_structured\_output: bool

—

Whether the chat model supports structured output.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/has_structured_output)[Astructured\_output\_kwargs: dict[str, Any]

—

Additional kwargs to pass to `with_structured_output()` in tests.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/structured_output_kwargs)[Asupports\_json\_mode: bool

—

Whether the chat model supports JSON mode.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_json_mode)[Asupports\_image\_inputs: bool

—

Supports image inputs.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_image_inputs)[Asupports\_image\_urls: bool

—

Supports image inputs from URLs.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_image_urls)[Asupports\_pdf\_inputs: bool

—

Whether the chat model supports PDF inputs, defaults to `False`.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_pdf_inputs)[Asupports\_audio\_inputs: bool

—

Supports audio inputs.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_audio_inputs)[Asupports\_video\_inputs: bool

—

Supports video inputs.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_video_inputs)[Areturns\_usage\_metadata: bool

—

Returns usage metadata.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/returns_usage_metadata)[Asupports\_anthropic\_inputs: bool

—

Whether the chat model supports Anthropic-style inputs.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_anthropic_inputs)[Asupports\_image\_tool\_message: bool

—

Supports image `ToolMessage` objects.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_image_tool_message)[Asupports\_pdf\_tool\_message: bool

—

Supports PDF `ToolMessage` objects.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_pdf_tool_message)[Aenable\_vcr\_tests: bool

—

Whether to enable VCR tests for the chat model.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/enable_vcr_tests)[Asupported\_usage\_metadata\_details: dict[Literal['invoke', 'stream'], list[Literal['audio\_input', 'audio\_output', 'reasoning\_output', 'cache\_read\_input', 'cache\_creation\_input']]]

—

Supported usage metadata details.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supported_usage_metadata_details)[Asupports\_model\_override: bool

—

Whether the model supports overriding the model name at runtime.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_model_override)[Amodel\_override\_value: str | None

—

Alternative model name to use when testing model override.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/model_override_value)

### Methods

[Mmodel

—

Model fixture.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/model)[Mmy\_adder\_tool

—

Adder tool fixture.](/python/langchain-tests/unit_tests/chat_models/ChatModelTests/my_adder_tool)

## Inherited from[BaseStandardTests](/python/langchain-tests/base/BaseStandardTests)

### Methods

[Mtest\_no\_overrides\_DO\_NOT\_OVERRIDE

—

Test that no standard tests are overridden.](/python/langchain-tests/base/BaseStandardTests/test_no_overrides_DO_NOT_OVERRIDE)


