<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests -->

Modulev1.1.4 (latest)●Since v1.1

# integration\_tests

Integration tests for LangChain components.

## Attributes

[attribute

modules: list](/python/langchain-tests/integration_tests/modules)

## Classes

[class

BaseStoreAsyncTests](/python/langchain-tests/integration_tests/base_store/BaseStoreAsyncTests)[class

BaseStoreSyncTests](/python/langchain-tests/integration_tests/base_store/BaseStoreSyncTests)[class

AsyncCacheTestSuite](/python/langchain-tests/integration_tests/cache/AsyncCacheTestSuite)[class

SyncCacheTestSuite](/python/langchain-tests/integration_tests/cache/SyncCacheTestSuite)[class

ChatModelIntegrationTests](/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests)[class

EmbeddingsIntegrationTests](/python/langchain-tests/integration_tests/embeddings/EmbeddingsIntegrationTests)[class

RetrieversIntegrationTests](/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests)[class

ToolsIntegrationTests](/python/langchain-tests/integration_tests/tools/ToolsIntegrationTests)[class

VectorStoreIntegrationTests](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests)[class

SandboxIntegrationTests](/python/langchain-tests/integration_tests/sandboxes/SandboxIntegrationTests)

## Modules



[module

chat\_models](/python/langchain-tests/integration_tests/chat_models)

[module

embeddings](/python/langchain-tests/integration_tests/embeddings)

[module

cache](/python/langchain-tests/integration_tests/cache)

[module

base\_store](/python/langchain-tests/integration_tests/base_store)

[module

retrievers](/python/langchain-tests/integration_tests/retrievers)

[module

indexer](/python/langchain-tests/integration_tests/indexer)

[module

sandboxes](/python/langchain-tests/integration_tests/sandboxes)

[module

vectorstores](/python/langchain-tests/integration_tests/vectorstores)

[module

tools](/python/langchain-tests/integration_tests/tools)

Test suite for checking the key-value API of a `BaseStore`.

This test suite verifies the basic key-value API of a `BaseStore`.

The test suite is designed for synchronous key-value stores.

Implementers should subclass this test suite and provide a fixture
that returns an empty key-value store for each test.

Test suite for checking the key-value API of a `BaseStore`.

This test suite verifies the basic key-value API of a `BaseStore`.

The test suite is designed for synchronous key-value stores.

Implementers should subclass this test suite and provide a fixture
that returns an empty key-value store for each test.

Test suite for checking the `BaseCache` API of a caching layer for LLMs.

Verifies the basic caching API of a caching layer for LLMs.

The test suite is designed for synchronous caching layers.

Implementers should subclass this test suite and provide a fixture that returns an
empty cache for each test.

Test suite for checking the `BaseCache` API of a caching layer for LLMs.

This test suite verifies the basic caching API of a caching layer for LLMs.

The test suite is designed for synchronous caching layers.

Implementers should subclass this test suite and provide a fixture
that returns an empty cache for each test.

Base class for retrievers integration tests.

Base class for tools integration tests.

Standard integration tests for a `SandboxBackendProtocol` implementation.

Base class for chat model integration tests.

Test subclasses must implement the `chat_model_class` and
`chat_model_params` properties to specify what model to test and its
initialization parameters.

```
from typing import Type

from langchain_tests.integration_tests import ChatModelIntegrationTests
from my_package.chat_models import MyChatModel

class TestMyChatModelIntegration(ChatModelIntegrationTests):
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

By default, this is determined by whether the chat model's
`with_structured_output` method is overridden. If the base implementation is
intended to be used, this method should be overridden.

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

Defaults to `False`.

JSON mode constrains the model to output valid JSON without enforcing
a specific schema (unlike `'function_calling'` or `'json_schema'` methods).

When using JSON mode, you must prompt the model to output JSON in your
message.

Example

```
structured_llm = llm.with_structured_output(MySchema, method="json_mode")
structured_llm.invoke("... Return the result as JSON.")
```

See docs for [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output).

```
@property
def supports_json_mode(self) -> bool:
    return True
```

`supports_image_inputs`

Boolean property indicating whether the chat model supports image inputs.

Defaults to `False`.

If set to `True`, the chat model will be tested by inputting an
`ImageContentBlock` with the shape:

```
{
    "type": "image",
    "base64": "<base64 image data>",
    "mime_type": "image/jpeg",  # or appropriate MIME type
}
```

In addition to OpenAI-style content blocks:

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
form

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

...as well as the LangChain `ImageContentBlock` format:

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

If set to `True`, the chat model will be tested by inputting a
`FileContentBlock` with the shape:

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

If set to `True`, the chat model will be tested by inputting an
`AudioContentBlock` with the shape:

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

Models supporting `usage_metadata` should also return the name of the underlying
model in the `response_metadata` of the `AIMessage`.

`supports_anthropic_inputs`

Boolean property indicating whether the chat model supports Anthropic-style
inputs.

Defaults to `False`.

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
    return True
```

`supported_usage_metadata_details`

Property controlling what usage metadata details are emitted in both invoke
and stream.

Defaults to `{"invoke": [], "stream": []}`.

`usage_metadata` is an optional dict attribute on `AIMessage` objects that track
input and output tokens.

[See more](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.messages.ai.UsageMetadata).

It includes optional keys `input_token_details` and `output_token_details`
that can track usage details associated with special types of tokens, such as
cached, audio, or reasoning.

Only needs to be overridden if these details are supplied.

`enable_vcr_tests`

Property controlling whether to enable select tests that rely on
[VCR](https://vcrpy.readthedocs.io/en/latest/) caching of HTTP calls, such
as benchmarking tests.

Defaults to `False`.

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

Base class for embeddings integration tests.

Test subclasses must implement the `embeddings_class` property to specify the
embeddings model to be tested. You can also override the
`embedding_model_params` property to specify initialization parameters.

```
from typing import Type

from langchain_tests.integration_tests import EmbeddingsIntegrationTests
from my_package.embeddings import MyEmbeddingsModel

class TestMyEmbeddingsModelIntegration(EmbeddingsIntegrationTests):
    @property
    def embeddings_class(self) -> Type[MyEmbeddingsModel]:
        # Return the embeddings model class to test here
        return MyEmbeddingsModel

    @property
    def embedding_model_params(self) -> dict:
        # Return initialization parameters for the model.
        return {"model": "model-001"}
```

Note

API references for individual test methods include troubleshooting tips.

Base class for vector store integration tests.

Implementers should subclass this test suite and provide a fixture
that returns an empty vector store for each test.

The fixture should use the `get_embeddings` method to get a pre-defined
embeddings model that should be used for this test suite.

Here is a template:

```
from typing import Generator

import pytest
from langchain_core.vectorstores import VectorStore
from langchain_parrot_link.vectorstores import ParrotVectorStore
from langchain_tests.integration_tests.vectorstores import VectorStoreIntegrationTests

class TestParrotVectorStore(VectorStoreIntegrationTests):
    @pytest.fixture()
    def vectorstore(self) -> Generator[VectorStore, None, None]:  # type: ignore
        """Get an empty vectorstore."""
        store = ParrotVectorStore(self.get_embeddings())
        # note: store should be EMPTY at this point
        # if you need to delete data, you may do so here
        try:
            yield store
        finally:
            # cleanup operations, or deleting data
            pass
```

In the fixture, before the `yield` we instantiate an empty vector store. In the
`finally` block, we call whatever logic is necessary to bring the vector store
to a clean state.

```
from typing import Generator

import pytest
from langchain_core.vectorstores import VectorStore
from langchain_tests.integration_tests.vectorstores import VectorStoreIntegrationTests

from langchain_chroma import Chroma

class TestChromaStandard(VectorStoreIntegrationTests):
    @pytest.fixture()
    def vectorstore(self) -> Generator[VectorStore, None, None]:  # type: ignore
        """Get an empty VectorStore for unit tests."""
        store = Chroma(embedding_function=self.get_embeddings())
        try:
            yield store
        finally:
            store.delete_collection()
            pass
```

Note that by default we enable both sync and async tests. To disable either,
override the `has_sync` or `has_async` properties to `False` in the
subclass. For example:

```
class TestParrotVectorStore(VectorStoreIntegrationTests):
    @pytest.fixture()
    def vectorstore(self) -> Generator[VectorStore, None, None]:  # type: ignore
        ...

    @property
    def has_async(self) -> bool:
        return False
```

Note

API references for individual test methods include troubleshooting tips.

Integration tests for chat models.

Integration tests for embeddings.

Standard tests for the `BaseCache` abstraction.

We don't recommend implementing externally managed `BaseCache` abstractions at this
time.

Standard tests for the `BaseStore` abstraction.

We don't recommend implementing externally managed `BaseStore` abstractions at this
time.

Integration tests for retrievers.

Test suite to check index implementations.

Standard tests for the `DocumentIndex` abstraction

We don't recommend implementing externally managed `DocumentIndex` abstractions at this
time.

Test suite to test `VectorStore` integrations.

Integration tests for tools.

Integration tests for the deepagents sandbox backend abstraction.

Implementers should subclass this test suite and provide a fixture that returns a
clean `SandboxBackendProtocol` instance.

Example:

```
from __future__ import annotations

from collections.abc import Iterator

import pytest
from deepagents.backends.protocol import SandboxBackendProtocol
from langchain_tests.integration_tests import SandboxIntegrationTests

from my_pkg import make_sandbox

class TestMySandboxStandard(SandboxIntegrationTests):
    @pytest.fixture(scope="class")
    def sandbox(self) -> Iterator[SandboxBackendProtocol]:
        backend = make_sandbox()
        try:
            yield backend
        finally:
            backend.delete()
```