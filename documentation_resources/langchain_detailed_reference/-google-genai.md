<!-- Source: https://reference.langchain.com/python/langchain-google-genai -->

## Description

# `langchain-google-genai`

LangChain integration for Google's Generative AI models, providing access to Gemini models via both the **Gemini Developer API** and **Vertex AI**.

Vertex AI consolidation

As of `langchain-google-genai` 4.0.0, this package uses the consolidated [`google-genai`](https://googleapis.github.io/python-genai/) SDK instead of the legacy [`google-ai-generativelanguage`](https://googleapis.dev/python/generativelanguage/latest/) SDK.

This migration brings support for Gemini models both via the Gemini Developer API and Gemini API in Vertex AI, superseding certain classes in `langchain-google-vertexai`, such as `ChatVertexAI`. Refer to [the provider docs](https://docs.langchain.com/oss/python/integrations/providers/google) and [release notes](https://github.com/langchain-ai/langchain-google/discussions/1422) for more information.

## Modules

> **Usage documentation**
> Refer to [the docs](https://docs.langchain.com/oss/python/integrations/providers/google) for a high-level guide on how to use each module. These reference pages contain auto-generated API documentation for each module, focusing on the "what" rather than the "how" or "why" (i.e. no end-to-end tutorials or conceptual overviews).

[`ChatGoogleGenerativeAI`

Gemini chat models (primary interface).](/python/integrations/langchain_google_genai/chat-google-generative-ai/)
[`GoogleGenerativeAI`

(Legacy) Google text completion abstraction.](/python/integrations/langchain_google_genai/google-generative-ai/)
[`GoogleGenerativeAIEmbeddings`

Gemini embedding models.](/python/integrations/langchain_google_genai/google-generative-ai-embeddings/)
[`create_context_cache`

Utility to create a context cache for reusing large content across requests.](/python/integrations/langchain_google_genai/create-context-cache/)
[`HarmCategory`

Enum for safety setting harm categories.](/python/integrations/langchain_google_genai/harm-category/)
[`HarmBlockThreshold`

Enum for safety setting blocking thresholds.](/python/integrations/langchain_google_genai/harm-block-threshold/)
[`Modality`

Enum for input/output modality configuration.](/python/integrations/langchain_google_genai/modality/)
[`MediaResolution`

Enum for media resolution settings.](/python/integrations/langchain_google_genai/media-resolution/)
[`ComputerUse`

Enum for computer use capabilities.](/python/integrations/langchain_google_genai/computer-use/)
[`Environment`

Enum for environment configuration.](/python/integrations/langchain_google_genai/environment/)