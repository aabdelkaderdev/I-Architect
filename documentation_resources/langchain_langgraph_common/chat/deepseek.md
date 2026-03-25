<!-- Source: https://docs.langchain.com/oss/python/integrations/chat/deepseek -->

This will help you get started with DeepSeek’s hosted [chat models](/oss/python/langchain/models).

**API Reference**For detailed documentation of all features and configuration options, head to the [`ChatDeepSeek`](https://reference.langchain.com/python/langchain-deepseek/chat_models/ChatDeepSeek) API reference.

**DeepSeek’s models are open source and can be run locally (e.g. in [Ollama](/oss/python/integrations/chat/ollama)) or on other inference providers (e.g. [Fireworks](/oss/python/integrations/chat/fireworks), [Together](/oss/python/integrations/chat/together)) as well.**

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Serializable | [JS support](https://js.langchain.com/docs/integrations/chat/deepseek) | Downloads | Version |
| --- | --- | --- | --- | --- | --- |
| [`ChatDeepSeek`](https://reference.langchain.com/python/langchain-deepseek/chat_models/ChatDeepSeek) | [`langchain-deepseek`](https://reference.langchain.com/python/langchain-deepseek/) | beta | ✅ |  |  |

### [​](#model-features) Model features

| [Tool calling](/oss/python/langchain/tools) | [Structured output](/oss/python/langchain/structured-output) | [Image input](/oss/python/langchain/messages#multimodal) | Audio input | Video input | [Token-level streaming](/oss/python/langchain/streaming) | Native async | [Token usage](/oss/python/langchain/models#token-usage) | [Logprobs](/oss/python/langchain/models#log-probabilities) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |

**DeepSeek-R1, specified via `model="deepseek-reasoner"`, does not support tool calling or structured output. Those features [are supported](https://api-docs.deepseek.com/guides/function_calling) by DeepSeek-V3 (specified via `model="deepseek-chat"`).**

## [​](#setup) Setup

To access DeepSeek models you’ll need to create a/an DeepSeek account, get an API key, and install the `langchain-deepseek` integration package.

### [​](#credentials) Credentials

Head to [DeepSeek’s API Key page](https://platform.deepseek.com/api_keys) to sign up to DeepSeek and generate an API key. Once you’ve done this set the `DEEPSEEK_API_KEY` environment variable:

Copy

```
import getpass
import os

if not os.getenv("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")
```

To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
```

### [​](#installation) Installation

The LangChain DeepSeek integration lives in the `langchain-deepseek` package:

Copy

```
pip install -qU langchain-deepseek
```

## [​](#instantiation) Instantiation

Now we can instantiate our model object and generate chat completions:

Copy

```
from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
```

## [​](#invocation) Invocation

Copy

```
messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
ai_msg.content
```

---

## [​](#api-reference) API reference

For detailed documentation of all ChatDeepSeek features and configurations head to the [API Reference](https://python.langchain.com/api_reference/deepseek/chat_models/langchain_deepseek.chat_models.ChatDeepSeek.html).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/chat/deepseek.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.