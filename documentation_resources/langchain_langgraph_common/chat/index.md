<!-- Source: https://docs.langchain.com/oss/python/integrations/chat/index -->

[Chat models](/oss/python/langchain/models) are language models that use a sequence of [messages](/oss/python/langchain/messages) as inputs and return messages as outputs (as opposed to traditional, plaintext LLMs).

## [​](#featured-models) Featured models

**While these LangChain classes support the indicated advanced feature**, you may need to refer to provider-specific documentation to learn which hosted models or backends support the feature.

| Model | [Tool calling](/oss/python/langchain/tools) | [Structured output](/oss/python/langchain/structured-output) | [Multimodal](/oss/python/langchain/messages#multimodal) |
| --- | --- | --- | --- |
| [`ChatOpenAI`](/oss/python/integrations/chat/openai) | ✅ | ✅ | ✅ |
| [`ChatAnthropic`](/oss/python/integrations/chat/anthropic) | ✅ | ✅ | ✅ |
| [`ChatVertexAI`](/oss/python/integrations/chat/google_vertex_ai) (deprecated) | ✅ | ✅ | ✅ |
| [`ChatGoogleGenerativeAI`](/oss/python/integrations/chat/google_generative_ai) | ✅ | ✅ | ✅ |
| [`AzureChatOpenAI`](/oss/python/integrations/chat/azure_chat_openai) | ✅ | ✅ | ✅ |
| [`ChatGroq`](/oss/python/integrations/chat/groq) | ✅ | ✅ | ❌ |
| [`ChatBedrock`](/oss/python/integrations/chat/bedrock) | ✅ | ✅ | ❌ |
| [`ChatAmazonNova`](/oss/python/integrations/chat/amazon_nova) | ✅ | ❌ | ✅ |
| [`ChatHuggingFace`](/oss/python/integrations/chat/huggingface) | ✅ | ✅ | ❌ |
| [`ChatOllama`](/oss/python/integrations/chat/ollama) | ✅ | ✅ | ❌ |
| [`ChatWatsonx`](/oss/python/integrations/chat/ibm_watsonx) | ✅ | ✅ | ✅ |
| [`ChatXAI`](/oss/python/integrations/chat/xai) | ✅ | ✅ | ❌ |
| [`ChatNVIDIA`](/oss/python/integrations/chat/nvidia_ai_endpoints) | ✅ | ✅ | ✅ |
| [`ChatCohere`](/oss/python/integrations/chat/cohere) | ✅ | ✅ | ❌ |
| [`ChatMistralAI`](/oss/python/integrations/chat/mistralai) | ✅ | ✅ | ❌ |
| [`ChatTogether`](/oss/python/integrations/chat/together) | ✅ | ✅ | ❌ |
| [`ChatFireworks`](/oss/python/integrations/chat/fireworks) | ✅ | ✅ | ❌ |
| [`ChatLlamaCpp`](/oss/python/integrations/chat/llamacpp) | ✅ | ✅ | ❌ |
| [`ChatDeepSeek`](/oss/python/integrations/chat/deepseek) | ✅ | ✅ | ❌ |
| [`ChatDatabricks`](/oss/python/integrations/chat/databricks) | ✅ | ✅ | ❌ |
| [`ChatPerplexity`](/oss/python/integrations/chat/perplexity) | ❌ | ✅ | ✅ |
| [`ChatOpenRouter`](/oss/python/integrations/chat/openrouter) | ✅ | ✅ | ✅ |
| [`ChatLiteLLM`](/oss/python/integrations/chat/litellm) | ✅ | ✅ | ✅ |

### [​](#routers-&-proxies) Routers & proxies

Routers and proxies give you access to models from multiple providers through a single API and credential. They can simplify billing, let you switch between models without changing integrations, and offer features like automatic fallbacks.

| Provider | Integration | Description |
| --- | --- | --- |
| [OpenRouter](https://openrouter.ai/) | [`ChatOpenRouter`](/oss/python/integrations/chat/openrouter) | Unified access to models from OpenAI, Anthropic, Google, Meta, and more |
| [LiteLLM](https://www.litellm.ai/) | [`ChatLiteLLM`](/oss/python/integrations/chat/litellm) | Unified interface for OpenAI, Anthropic, Azure, Hugging Face, and more with routing and fallbacks |

## [​](#chat-completions-api) Chat Completions API

Certain model providers offer endpoints that are compatible with OpenAI’s [Chat Completions API](https://platform.openai.com/docs/api-reference/chat). In such cases, you can use [`ChatOpenAI`](/oss/python/integrations/chat/openai) with a custom `base_url` to connect to these endpoints for basic chat functionality.

`ChatOpenAI` targets [official OpenAI API specifications](https://github.com/openai/openai-openapi) only. Non-standard response fields from third-party providers (e.g., `reasoning_content`, `reasoning`, `reasoning_details`) **are not extracted or preserved**. Use a provider-specific package when you need access to non-standard features.For instance, OpenRouter has a dedicated LangChain integration. See the [`ChatOpenRouter` guide](/oss/python/integrations/chat/openrouter) for setup and usage.

## [​](#all-chat-models) All chat models

## Abso

View guide

## AI21 Labs

View guide

## AI/ML API

View guide

## Alibaba Cloud PAI EAS

View guide

## Amazon Nova

View guide

## Anthropic

View guide

## AzureAIOpenAIApiChatModel

View guide

## Azure OpenAI

View guide

## Azure ML Endpoint

View guide

## Baichuan Chat

View guide

## Baidu Qianfan

View guide

## Baseten

View guide

## AWS Bedrock

View guide

## Cerebras

View guide

## CloudflareWorkersAI

View guide

## Cohere

View guide

## ContextualAI

View guide

## Coze Chat

View guide

## Dappier AI

View guide

## Databricks

View guide

## DeepInfra

View guide

## DeepSeek

View guide

## Eden AI

View guide

## EverlyAI

View guide

## Featherless AI

View guide

## Fireworks

View guide

## ChatFriendli

View guide

## Google Gemini

View guide

## Google Cloud Vertex AI

View guide

## GPTRouter

View guide

## DigitalOcean Gradient

View guide

## GreenNode

View guide

## Groq

View guide

## ChatHuggingFace

View guide

## IBM watsonx.ai

View guide

## JinaChat

View guide

## Kinetica

View guide

## Konko

View guide

## LiteLLM

View guide

## Llama 2 Chat

View guide

## Llama API

View guide

## LlamaEdge

View guide

## Llama.cpp

View guide

## maritalk

View guide

## MiniMax

View guide

## MistralAI

View guide

## MLX

View guide

## ModelScope

View guide

## Moonshot

View guide

## Naver

View guide

## Nebius

View guide

## Netmind

View guide

## NVIDIA AI Endpoints

View guide

## ChatOCIModelDeployment

View guide

## OCIGenAI

View guide

## ChatOctoAI

View guide

## Ollama

View guide

## OpenAI

View guide

## OpenRouter

View guide

## Outlines

View guide

## Perplexity

View guide

## Pipeshift

View guide

## ChatPredictionGuard

View guide

## PremAI

View guide

## PromptLayer ChatOpenAI

View guide

## Qwen QwQ

View guide

## Qwen

View guide

## Reka

View guide

## RunPod Chat Model

View guide

## SambaNova

View guide

## ChatSeekrFlow

View guide

## Snowflake Cortex

View guide

## SparkLLM Chat

View guide

## Nebula (Symbl.ai)

View guide

## Tencent Hunyuan

View guide

## Together

View guide

## Tongyi Qwen

View guide

## Upstage

View guide

## vLLM Chat

View guide

## Volc Engine Maas

View guide

## ChatWriter

View guide

## xAI

View guide

## Xinference

View guide

## YandexGPT

View guide

## ChatYI

View guide

## Yuan2.0

View guide

## ZHIPU AI

View guide

If you’d like to contribute an integration, see [Contributing integrations](/oss/python/contributing#add-a-new-integration).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/chat/index.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.