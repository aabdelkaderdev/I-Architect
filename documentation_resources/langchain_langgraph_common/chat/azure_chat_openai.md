<!-- Source: https://docs.langchain.com/oss/python/integrations/chat/azure_chat_openai -->

You can find information about Azure OpenAI’s latest models and their costs, context windows, and supported input types in the [Azure docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models).

**Azure OpenAI vs OpenAI**Azure OpenAI refers to OpenAI models hosted on the [Microsoft Azure platform](https://azure.microsoft.com/en-us/products/ai-services/openai-service). OpenAI also provides its own model APIs. To access OpenAI services directly, use the [`ChatOpenAI` integration](/oss/python/integrations/chat/openai).

**Azure OpenAI v1 API**Azure OpenAI’s [v1 API](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/api-version-lifecycle?tabs=python#next-generation-api-1) (Generally Available as of August 2025) allows you to use `ChatOpenAI` directly with Azure endpoints. This provides a unified interface and native support for Microsoft Entra ID authentication with automatic token refresh.See the [ChatOpenAI Azure section](/oss/python/integrations/chat/openai#using-with-azure-openai) for details on using `ChatOpenAI` with Azure’s v1 API.`AzureChatOpenAI` is still currently supported for traditional Azure OpenAI API versions and scenarios requiring Azure-specific configurations, but we recommend using `ChatOpenAI` or the `AzureAIOpenAIApiChatModel` in [LangChain Azure AI](https://docs.langchain.com/oss/python/integrations/providers/azure_ai) going forward.

[`AzureChatOpenAI`](https://reference.langchain.com/python/langchain-openai/chat_models/azure/AzureChatOpenAI) shares the same underlying base implementation as [`ChatOpenAI`](https://reference.langchain.com/python/langchain-openai/chat_models/base/ChatOpenAI),
which interfaces with OpenAI services directly.This page serves as a quickstart for authenticating and connecting your Azure OpenAI service to a LangChain chat model.Visit the [`ChatOpenAI` docs](/oss/python/integrations/chat/openai) for details on available
features, or head to the [`AzureChatOpenAI`](https://reference.langchain.com/python/langchain-openai/chat_models/azure/AzureChatOpenAI) API reference.

**API Reference**For detailed documentation of all features and configuration options, head to the [`AzureChatOpenAI`](https://reference.langchain.com/python/langchain-openai/chat_models/azure/AzureChatOpenAI) API reference.

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Serializable | JS/TS Support | Downloads | Latest Version |
| --- | --- | --- | --- | --- | --- |
| [`AzureChatOpenAI`](https://reference.langchain.com/python/langchain-openai/chat_models/azure/AzureChatOpenAI) | [`langchain-openai`](https://reference.langchain.com/python/langchain-openai/) | beta | ✅ [(npm)](https://js.langchain.com/docs/integrations/chat/openai) |  |  |

### [​](#model-features) Model features

| [Tool calling](/oss/python/langchain/tools) | [Structured output](/oss/python/langchain/structured-output) | [Image input](/oss/python/langchain/messages#multimodal) | Audio input | Video input | [Token-level streaming](/oss/python/langchain/streaming) | Native async | [Token usage](/oss/python/langchain/models#token-usage) | [Logprobs](/oss/python/langchain/models#log-probabilities) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |

## [​](#setup) Setup

To access [`AzureChatOpenAI`](https://reference.langchain.com/python/langchain-openai/chat_models/azure/AzureChatOpenAI) models you’ll need to create an Azure account, create a deployment of an Azure OpenAI model, get the name and endpoint for your deployment, get an Azure OpenAI API key, and install the `langchain-openai` integration package.

### [​](#installation) Installation

pip

uv

Copy

```
pip install -U langchain-openai
```

### [​](#credentials) Credentials

Head to the [Azure docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line%2Cpython-new&pivots=programming-language-python) to create your deployment and generate an API key. Once you’ve done this set the `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` environment variables:

Copy

```
import getpass
import os

if "AZURE_OPENAI_API_KEY" not in os.environ:
    os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass(
        "Enter your AzureOpenAI API key: "
    )
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://YOUR-ENDPOINT.openai.azure.com/"
```

To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
os.environ["LANGSMITH_TRACING"] = "true"
```

## [​](#instantiation) Instantiation

Now we can instantiate our model object and generate chat completions.

- Replace `azure_deployment` with the name of your deployment,
- You can find the latest supported `api_version` here: [learn.microsoft.com/en-us/azure/ai-services/openai/reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference).

Copy

```
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_deployment="gpt-35-turbo",  # or your deployment
    api_version="2023-06-01-preview",  # or your api version
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
AIMessage(content="J'adore la programmation.", response_metadata={'token_usage': {'completion_tokens': 8, 'prompt_tokens': 31, 'total_tokens': 39}, 'model_name': 'gpt-35-turbo', 'system_fingerprint': None, 'prompt_filter_results': [{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}], 'finish_reason': 'stop', 'logprobs': None, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}, id='run-bea4b46c-e3e1-4495-9d3a-698370ad963d-0', usage_metadata={'input_tokens': 31, 'output_tokens': 8, 'total_tokens': 39})
```

Copy

```
print(ai_msg.content)
```

Copy

```
J'adore la programmation.
```

## [​](#streaming-usage-metadata) Streaming usage metadata

OpenAI’s Chat Completions API does not stream token usage statistics by default (see the [OpenAI API reference for stream options](https://platform.openai.com/docs/api-reference/completions/create#completions-create-stream_options)).
To recover token counts when streaming with [`ChatOpenAI`](https://reference.langchain.com/python/langchain-openai/chat_models/base/ChatOpenAI) or `AzureChatOpenAI`, set `stream_usage=True` as an initialization parameter or on invocation:

Copy

```
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(model="gpt-4.1-mini", stream_usage=True)
```

## [​](#specifying-model-version) Specifying model version

Azure OpenAI responses contain `model_name` response metadata property, which is name of the model used to generate the response. However unlike native OpenAI responses, it does not contain the specific version of the model, which is set on the deployment in Azure. e.g. it does not distinguish between `gpt-35-turbo-0125` and `gpt-35-turbo-0301`. This makes it tricky to know which version of the model was used to generate the response, which as result can lead to e.g. wrong total cost calculation with `OpenAICallbackHandler`.
To solve this problem, you can pass `model_version` parameter to [`AzureChatOpenAI`](https://reference.langchain.com/python/langchain-openai/chat_models/azure/AzureChatOpenAI) class, which will be added to the model name in the llm output. This way you can easily distinguish between different versions of the model.

Copy

```
pip install -qU langchain-community
```

Copy

```
from langchain_community.callbacks import get_openai_callback

with get_openai_callback() as cb:
    llm.invoke(messages)
    print(
        f"Total Cost (USD): ${format(cb.total_cost, '.6f')}"
    )  # without specifying the model version, flat-rate 0.002 USD per 1k input and output tokens is used
```

Copy

```
Total Cost (USD): $0.000063
```

Copy

```
llm_0301 = AzureChatOpenAI(
    azure_deployment="gpt-35-turbo",  # or your deployment
    api_version="2023-06-01-preview",  # or your api version
    model_version="0301",
)
with get_openai_callback() as cb:
    llm_0301.invoke(messages)
    print(f"Total Cost (USD): ${format(cb.total_cost, '.6f')}")
```

Copy

```
Total Cost (USD): $0.000074
```

---

## [​](#api-reference) API reference

For detailed documentation of all features and configuration options, head to the [`AzureChatOpenAI`](https://reference.langchain.com/python/langchain-openai/chat_models/azure/AzureChatOpenAI) API reference.

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/chat/azure_chat_openai.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.