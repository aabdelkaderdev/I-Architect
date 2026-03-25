<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent_toolkits/conversational_retrieval/openai_functions -->

Modulev1.2.13 (latest)●Since v1.0

# openai\_functions

## Functions

[function

create\_conversational\_retrieval\_agent

A convenience method for creating a conversational retrieval agent.](/python/langchain-classic/agents/agent_toolkits/conversational_retrieval/openai_functions/create_conversational_retrieval_agent)

## Classes

[class

AgentExecutor

Agent that is using tools.](/python/langchain-classic/agents/agent/AgentExecutor)[class

AgentTokenBufferMemory

Memory used to save agent output AND intermediate steps.](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory)[deprecatedclass

OpenAIFunctionsAgent

An Agent driven by OpenAIs function powered API.](/python/langchain-classic/agents/openai_functions_agent/base/OpenAIFunctionsAgent)[deprecatedclass

BaseMemory

Abstract base class for memory in Chains.

Memory refers to state in Chains. Memory can be used to store information about
past executions of a Chain and inject that information into the inputs of
future executions of the Chain. For example, for conversational Chains Memory
can be used to store conversations and automatically add them to future model
prompts so that the model has the necessary context to respond coherently to
the latest input.](/python/langchain-classic/base_memory/BaseMemory)[deprecatedclass

ConversationTokenBufferMemory

Conversation chat memory with token limit.

Keeps only the most recent messages in the conversation under the constraint
that the total number of tokens in the conversation does not exceed a certain limit.](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory)


