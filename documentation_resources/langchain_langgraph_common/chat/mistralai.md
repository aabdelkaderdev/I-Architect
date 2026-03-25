<!-- Source: https://docs.langchain.com/oss/python/integrations/chat/mistralai -->

This will help you get started with Mistral [chat models](/oss/python/langchain/models). For detailed documentation of all `ChatMistralAI` features and configurations head to the [API reference](https://python.langchain.com/api_reference/mistralai/chat_models/langchain_mistralai.chat_models.ChatMistralAI.html). The `ChatMistralAI` class is built on top of the [Mistral API](https://docs.mistral.ai/api/). For a list of all the models supported by Mistral, check out [this page](https://docs.mistral.ai/getting-started/models/).

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Serializable | [JS support](https://js.langchain.com/docs/integrations/chat/mistral) | Downloads | Version |
| --- | --- | --- | --- | --- | --- |
| [ChatMistralAI](https://python.langchain.com/api_reference/mistralai/chat_models/langchain_mistralai.chat_models.ChatMistralAI.html) | [langchain-mistralai](https://python.langchain.com/api_reference/mistralai/index.html) | beta | ✅ |  |  |

### [​](#model-features) Model features

| [Tool calling](/oss/python/langchain/tools) | [Structured output](/oss/python/langchain/structured-output) | [Image input](/oss/python/langchain/messages#multimodal) | Audio input | Video input | [Token-level streaming](/oss/python/langchain/streaming) | Native async | [Token usage](/oss/python/langchain/models#token-usage) | [Logprobs](/oss/python/langchain/models#log-probabilities) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |

## [​](#setup) Setup

To access `ChatMistralAI` models you’ll need to create a Mistral account, get an API key, and install the `langchain-mistralai` integration package.

### [​](#credentials) Credentials

A valid [API key](https://console.mistral.ai/api-keys/) is needed to communicate with the API. Once you’ve done this set the MISTRAL\_API\_KEY environment variable:

Copy

```
import getpass
import os

if "MISTRAL_API_KEY" not in os.environ:
    os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter your Mistral API key: ")
```

To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
os.environ["LANGSMITH_TRACING"] = "true"
```

### [​](#installation) Installation

The LangChain Mistral integration lives in the `langchain-mistralai` package:

Copy

```
pip install -qU langchain-mistralai
```

## [​](#instantiation) Instantiation

Now we can instantiate our model object and generate chat completions:

Copy

```
from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
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
AIMessage(content='Sure, I\'d be happy to help you translate that sentence into French! The English sentence "I love programming" translates to "J\'aime programmer" in French. Let me know if you have any other questions or need further assistance!', response_metadata={'token_usage': {'prompt_tokens': 32, 'total_tokens': 84, 'completion_tokens': 52}, 'model': 'mistral-small', 'finish_reason': 'stop'}, id='run-64bac156-7160-4b68-b67e-4161f63e021f-0', usage_metadata={'input_tokens': 32, 'output_tokens': 52, 'total_tokens': 84})
```

Copy

```
print(ai_msg.content)
```

Copy

```
Sure, I'd be happy to help you translate that sentence into French! The English sentence "I love programming" translates to "J'aime programmer" in French. Let me know if you have any other questions or need further assistance!
```

---

## [​](#api-reference) API reference

Head to the [API reference](https://python.langchain.com/api_reference/mistralai/chat_models/langchain_mistralai.chat_models.ChatMistralAI.html) for detailed documentation of all attributes and methods.

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/chat/mistralai.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.