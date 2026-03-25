<!-- Source: https://reference.langchain.com/python/langchain-core/langchain_core -->

Modulev1.2.21 (latest)●Since v0.1

# langchain\_core

`langchain-core` defines the base abstractions for the LangChain ecosystem.

The interfaces for core components like chat models, LLMs, vector stores, retrievers,
and more are defined here. The universal invocation protocol (Runnables) along with
a syntax for combining components are also defined here.

**No third-party integrations are defined here.** The dependencies are kept purposefully
very lightweight.

## Attributes

[attribute

VERSION: str](/python/langchain-core/version/VERSION)

## Functions

[function

surface\_langchain\_beta\_warnings

Unmute LangChain beta warnings.](/python/langchain-core/_api/beta_decorator/surface_langchain_beta_warnings)[function

surface\_langchain\_deprecation\_warnings

Unmute LangChain deprecation warnings.](/python/langchain-core/_api/deprecation/surface_langchain_deprecation_warnings)

## Modules

[module

version

langchain-core version information and utilities.](/python/langchain-core/version)[module

agents

Schema definitions for representing agent actions, observations, and return values.

Warning

The schema definitions are provided for backwards compatibility.

Warning

New agents should be built using the
[`langchain` library](https://pypi.org/project/langchain/), which provides a
simpler and more flexible way to define agents.

See docs on [building agents](https://docs.langchain.com/oss/python/langchain/agents).

Agents use language models to choose a sequence of actions to take.

A basic agent works in the following manner:

1. Given a prompt an agent uses an LLM to request an action to take
   (e.g., a tool to run).
2. The agent executes the action (e.g., runs the tool), and receives an observation.
3. The agent returns the observation to the LLM, which can then be used to generate
   the next action.
4. When the agent reaches a stopping condition, it returns a final return value.

The schemas for the agents themselves are defined in `langchain.agents.agent`.](/python/langchain-core/agents)[module

chat\_history

Chat message history stores a history of the message interactions in a chat.](/python/langchain-core/chat_history)[module

retrievers

**Retriever** class returns `Document` objects given a text **query**.

It is more general than a vector store. A retriever does not need to be able to
store documents, only to return (or retrieve) it. Vector stores can be used as
the backbone of a retriever, but there are other types of retrievers as well.](/python/langchain-core/retrievers)[module

cross\_encoders

Cross Encoder interface.](/python/langchain-core/cross_encoders)[module

stores

**Store** implements the key-value stores and storage helpers.

Module provides implementations of various key-value stores that conform
to a simple key-value interface.

The primary goal of these storages is to support implementation of caching.](/python/langchain-core/stores)[module

sys\_info

Print information about the system and langchain packages for debugging purposes.](/python/langchain-core/sys_info)[module

chat\_sessions

**Chat Sessions** are a collection of messages and function calls.](/python/langchain-core/chat_sessions)[module

globals

Global values and configuration that apply to all of LangChain.](/python/langchain-core/globals)[module

caches

Optional caching layer for language models.

Distinct from provider-based [prompt caching](https://docs.langchain.com/oss/python/langchain/models#prompt-caching).

Beta feature

This is a beta feature. Please be wary of deploying experimental code to production
unless you've taken appropriate precautions.

A cache is useful for two reasons:

1. It can save you money by reducing the number of API calls you make to the LLM
   provider if you're often requesting the same completion multiple times.
2. It can speed up your application by reducing the number of API calls you make to the
   LLM provider.](/python/langchain-core/caches)[module

exceptions

Custom **exceptions** for LangChain.](/python/langchain-core/exceptions)[module

env

Utilities for getting information about the runtime environment.](/python/langchain-core/env)[module

structured\_query

Internal representation of a structured query language.](/python/langchain-core/structured_query)[module

chat\_loaders

Chat loaders.](/python/langchain-core/chat_loaders)[module

rate\_limiters

Interface for a rate limiter and an in-memory rate limiter.](/python/langchain-core/rate_limiters)[module

prompt\_values

**Prompt values** for language model prompts.

Prompt values are used to represent different pieces of prompts. They can be used to
represent text, images, or chat message pieces.](/python/langchain-core/prompt_values)[module

messages

**Messages** are objects used in prompts and chat conversations.](/python/langchain-core/messages)[module

document\_loaders

Document loaders.](/python/langchain-core/document_loaders)[module

prompts

A prompt is the input to the model.

Prompt is often constructed from multiple components and prompt values. Prompt classes
and functions make constructing and working with prompts easy.](/python/langchain-core/prompts)[module

documents

Documents module for data retrieval and processing workflows.

This module provides core abstractions for handling data in retrieval-augmented
generation (RAG) pipelines, vector stores, and document processing workflows.

Documents vs. message content

This module is distinct from `langchain_core.messages.content`, which provides
multimodal content blocks for **LLM chat I/O** (text, images, audio, etc. within
messages).

**Key distinction:**

- **Documents** (this module): For **data retrieval and processing workflows**

  - Vector stores, retrievers, RAG pipelines
  - Text chunking, embedding, and semantic search
  - Example: Chunks of a PDF stored in a vector database
- **Content Blocks** (`messages.content`): For **LLM conversational I/O**

  - Multimodal message content sent to/from models
  - Tool calls, reasoning, citations within chat
  - Example: An image sent to a vision model in a chat message (via
    [`ImageContentBlock`](/python/langchain-core/messages/content/ImageContentBlock))

While both can represent similar data types (text, files), they serve different
architectural purposes in LangChain applications.](/python/langchain-core/documents)[module

embeddings

Embeddings.](/python/langchain-core/embeddings)[module

vectorstores

Vector stores.](/python/langchain-core/vectorstores)[module

tracers

Tracers are classes for tracing runs.](/python/langchain-core/tracers)[module

indexing

Code to help indexing data into a vectorstore.

This package contains helper logic to help deal with indexing data into
a `VectorStore` while avoiding duplicated content and over-writing content
if it's unchanged.](/python/langchain-core/indexing)[module

example\_selectors

Example selectors.

**Example selector** implements logic for selecting examples to include them in prompts.
This allows us to select examples that are most relevant to the input.](/python/langchain-core/example_selectors)[module

utils

Utility functions for LangChain.

These functions do not depend on any other LangChain module.](/python/langchain-core/utils)[module

callbacks

Callback handlers allow listening to events in LangChain.](/python/langchain-core/callbacks)[module

language\_models

Core language model abstractions.

LangChain has two main classes to work with language models: chat models and
"old-fashioned" LLMs (string-in, string-out).

**Chat models**

Language models that use a sequence of messages as inputs and return chat messages
as outputs (as opposed to using plain text).

Chat models support the assignment of distinct roles to conversation messages, helping
to distinguish messages from the AI, users, and instructions such as system messages.

The key abstraction for chat models is
[`BaseChatModel`](/python/langchain-core/language_models/chat_models/BaseChatModel). Implementations should
inherit from this class.

See existing [chat model integrations](https://docs.langchain.com/oss/python/integrations/chat).

**LLMs (legacy)**

Language models that takes a string as input and returns a string.

These are traditionally older models (newer models generally are chat models).

Although the underlying models are string in, string out, the LangChain wrappers also
allow these models to take messages as input. This gives them the same interface as
chat models. When messages are passed in as input, they will be formatted into a string
under the hood before being passed to the underlying model.](/python/langchain-core/language_models)[module

outputs

Output classes.

Used to represent the output of a language model call and the output of a chat.

The top container for information is the `LLMResult` object. `LLMResult` is used by both
chat models and LLMs. This object contains the output of the language model and any
additional information that the model provider wants to return.

When invoking models via the standard runnable methods (e.g. invoke, batch, etc.):

- Chat models will return `AIMessage` objects.
- LLMs will return regular text strings.

In addition, users can access the raw output of either LLMs or chat models via
callbacks. The `on_chat_model_end` and `on_llm_end` callbacks will return an `LLMResult`
object containing the generated outputs and any additional information returned by the
model provider.

In general, if information is already available in the AIMessage object, it is
recommended to access it from there rather than from the `LLMResult` object.](/python/langchain-core/outputs)[module

output\_parsers

`OutputParser` classes parse the output of an LLM call into structured data.

Structured output

Output parsers emerged as an early solution to the challenge of obtaining structured
output from LLMs.

Today, most LLMs support [structured output](https://docs.langchain.com/oss/python/langchain/models#structured-outputs)
natively. In such cases, using output parsers may be unnecessary, and you should
leverage the model's built-in capabilities for structured output. Refer to the
[documentation of your chosen model](https://docs.langchain.com/oss/python/integrations/providers/overview)
for guidance on how to achieve structured output directly.

Output parsers remain valuable when working with models that do not support
structured output natively, or when you require additional processing or validation
of the model's output beyond its inherent capabilities.](/python/langchain-core/output_parsers)[module

runnables

LangChain **Runnable** and the **LangChain Expression Language (LCEL)**.

The LangChain Expression Language (LCEL) offers a declarative method to build
production-grade programs that harness the power of LLMs.

Programs created using LCEL and LangChain `Runnable` objects inherently suppor
synchronous asynchronous, batch, and streaming operations.

Support for **async** allows servers hosting LCEL based programs to scale bette for
higher concurrent loads.

**Batch** operations allow for processing multiple inputs in parallel.

**Streaming** of intermediate outputs, as they're being generated, allows for creating
more responsive UX.

This module contains schema and implementation of LangChain `Runnable` object
primitives.](/python/langchain-core/runnables)[module

load

**Load** module helps with serialization and deserialization.](/python/langchain-core/load)[module

tools

Tools are classes that an Agent uses to interact with the world.

Each tool has a description. Agent uses the description to choose the righ tool for the
job.](/python/langchain-core/tools)


