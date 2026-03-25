<!-- Source: https://docs.langchain.com/oss/python/integrations/chat/fireworks -->

This doc helps you get started with Fireworks AI [chat models](/oss/python/langchain/models). For a list of all models served by Fireworks see the [Fireworks docs](https://fireworks.ai/models).

**API Reference**For detailed documentation of all features and configuration options, head to the [`ChatFireworks`](https://reference.langchain.com/python/langchain-fireworks/chat_models/ChatFireworks) API reference.

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Serializable | JS/TS Support | Downloads | Version |
| --- | --- | --- | --- | --- | --- |
| [`ChatFireworks`](https://reference.langchain.com/python/langchain-fireworks/chat_models/ChatFireworks) | [`langchain-fireworks`](https://reference.langchain.com/python/langchain-fireworks/) | beta | ✅ [(npm)](https://js.langchain.com/docs/integrations/chat/fireworks) |  |  |

### [​](#model-features) Model features

| [Tool calling](/oss/python/langchain/tools) | [Structured output](/oss/python/langchain/structured-output) | [Image input](/oss/python/langchain/messages#multimodal) | Audio input | Video input | [Token-level streaming](/oss/python/langchain/streaming) | Native async | [Token usage](/oss/python/langchain/models#token-usage) | [Logprobs](/oss/python/langchain/models#log-probabilities) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |

## [​](#setup) Setup

To access Fireworks models you’ll need to create a Fireworks account, get an API key, and install the `langchain-fireworks` integration package.

### [​](#credentials) Credentials

Head to [fireworks.ai](https://app.fireworks.ai/login) to sign up to Fireworks and generate an API key. Once you’ve done this set the FIREWORKS\_API\_KEY environment variable:

Copy

```
import getpass
import os

if "FIREWORKS_API_KEY" not in os.environ:
    os.environ["FIREWORKS_API_KEY"] = getpass.getpass("Enter your Fireworks API key: ")
```

To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
os.environ["LANGSMITH_TRACING"] = "true"
```

### [​](#installation) Installation

The LangChain Fireworks integration lives in the `langchain-fireworks` package:

Copy

```
pip install -qU langchain-fireworks
```

## [​](#instantiation) Instantiation

Now we can instantiate our model object and generate chat completions:

Copy

```
from langchain_fireworks import ChatFireworks

llm = ChatFireworks(
    model="accounts/fireworks/models/kimi-k2-instruct-0905",
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
ai_msg
```

Copy

```
AIMessage(content="J'adore la programmation.", additional_kwargs={}, response_metadata={'token_usage': {'prompt_tokens': 31, 'total_tokens': 41, 'completion_tokens': 10}, 'system_fingerprint': '', 'finish_reason': 'stop', 'logprobs': None, 'model_provider': 'fireworks', 'model_name': 'accounts/fireworks/models/kimi-k2-instruct-0905'}, id='lc_run--a2bdeca3-6394-4c80-97ad-2fc8db9f54bb-0', usage_metadata={'input_tokens': 31, 'output_tokens': 10, 'total_tokens': 41})
```

Copy

```
print(ai_msg.content)
```

Copy

```
J'adore la programmation.
```

## [​](#api-reference) API reference

For detailed documentation of all features and configuration options, head to the [`ChatFireworks`](https://reference.langchain.com/python/langchain-fireworks/chat_models/ChatFireworks) API reference.

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/chat/fireworks.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.