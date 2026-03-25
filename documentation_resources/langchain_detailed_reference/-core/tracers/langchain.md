<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/langchain -->

Modulev1.2.21 (latest)●Since v0.1

# langchain

A tracer implementation that records to LangChain endpoint.

## Attributes

[attribute

Run: RunTree](/python/langchain-core/tracers/schemas/Run)[attribute

logger](/python/langchain-core/tracers/langchain/logger)

## Functions

[function

get\_runtime\_environment

Get information about the LangChain runtime environment.](/python/langchain-core/env/get_runtime_environment)[function

dumpd

Return a dict representation of an object.](/python/langchain-core/load/dump/dumpd)[function

add\_usage

Recursively add two UsageMetadata objects.](/python/langchain-core/messages/ai/add_usage)[function

run\_construct

Construct run without validation, compatible with both Pydantic v1 and v2.](/python/langchain-core/tracers/_compat/run_construct)[function

run\_to\_dict

Convert run to dict, compatible with both Pydantic v1 and v2.](/python/langchain-core/tracers/_compat/run_to_dict)[function

log\_error\_once

Log an error once.](/python/langchain-core/tracers/langchain/log_error_once)[function

wait\_for\_all\_tracers

Wait for all tracers to finish.](/python/langchain-core/tracers/langchain/wait_for_all_tracers)[function

get\_client

Get the client.](/python/langchain-core/tracers/langchain/get_client)

## Classes

[class

UsageMetadata

Usage metadata for a message, such as token counts.

This is a standard representation of token usage that is consistent across models.](/python/langchain-core/messages/ai/UsageMetadata)[class

BaseTracer

Base interface for tracers.](/python/langchain-core/tracers/base/BaseTracer)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

ChatGenerationChunk

`ChatGeneration` chunk.

`ChatGeneration` chunks can be concatenated with other `ChatGeneration` chunks.](/python/langchain-core/outputs/chat_generation/ChatGenerationChunk)[class

GenerationChunk

`GenerationChunk`, which can be concatenated with other `Generation` chunks.](/python/langchain-core/outputs/generation/GenerationChunk)[class

LangChainTracer

Implementation of the `SharedTracer` that `POSTS` to the LangChain endpoint.](/python/langchain-core/tracers/langchain/LangChainTracer)


