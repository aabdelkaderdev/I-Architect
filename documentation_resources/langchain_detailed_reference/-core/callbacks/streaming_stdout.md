<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/streaming_stdout -->

Modulev1.2.21 (latest)●Since v0.1

# streaming\_stdout

Callback Handler streams to stdout on new llm token.

## Classes

[class

BaseCallbackHandler

Base callback handler.](/python/langchain-core/callbacks/base/BaseCallbackHandler)[class

AgentAction

Represents a request to execute an action by an agent.

The action consists of the name of the tool to execute and the input to pass
to the tool. The log is used to pass along extra information about the action.](/python/langchain-core/agents/AgentAction)[class

AgentFinish

Final return value of an `ActionAgent`.

Agents return an `AgentFinish` when they have reached a stopping condition.](/python/langchain-core/agents/AgentFinish)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

LLMResult

A container for results of an LLM call.

Both chat models and LLMs generate an `LLMResult` object. This object contains the
generated outputs and any additional information that the model provider wants to
return.](/python/langchain-core/outputs/llm_result/LLMResult)[class

StreamingStdOutCallbackHandler

Callback handler for streaming.](/python/langchain-core/callbacks/streaming_stdout/StreamingStdOutCallbackHandler)


