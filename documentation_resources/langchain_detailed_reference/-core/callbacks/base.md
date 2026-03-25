<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base -->

Modulev1.2.21 (latest)●Since v0.1

# base

Base callback handler for LangChain.

## Classes

[class

AgentAction

Represents a request to execute an action by an agent.

The action consists of the name of the tool to execute and the input to pass
to the tool. The log is used to pass along extra information about the action.](/python/langchain-core/agents/AgentAction)[class

AgentFinish

Final return value of an `ActionAgent`.

Agents return an `AgentFinish` when they have reached a stopping condition.](/python/langchain-core/agents/AgentFinish)[class

Document

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.](/python/langchain-core/documents/base/Document)[class

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

LLMResult

A container for results of an LLM call.

Both chat models and LLMs generate an `LLMResult` object. This object contains the
generated outputs and any additional information that the model provider wants to
return.](/python/langchain-core/outputs/llm_result/LLMResult)[class

RetrieverManagerMixin

Mixin for `Retriever` callbacks.](/python/langchain-core/callbacks/base/RetrieverManagerMixin)[class

LLMManagerMixin

Mixin for LLM callbacks.](/python/langchain-core/callbacks/base/LLMManagerMixin)[class

ChainManagerMixin

Mixin for chain callbacks.](/python/langchain-core/callbacks/base/ChainManagerMixin)[class

ToolManagerMixin

Mixin for tool callbacks.](/python/langchain-core/callbacks/base/ToolManagerMixin)[class

CallbackManagerMixin

Mixin for callback manager.](/python/langchain-core/callbacks/base/CallbackManagerMixin)[class

RunManagerMixin

Mixin for run manager.](/python/langchain-core/callbacks/base/RunManagerMixin)[class

BaseCallbackHandler

Base callback handler.](/python/langchain-core/callbacks/base/BaseCallbackHandler)[class

AsyncCallbackHandler

Base async callback handler.](/python/langchain-core/callbacks/base/AsyncCallbackHandler)[class

BaseCallbackManager

Base callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager)

## Type Aliases

[typeAlias

Callbacks: list[BaseCallbackHandler] | BaseCallbackManager | None](/python/langchain-core/callbacks/base/Callbacks)


