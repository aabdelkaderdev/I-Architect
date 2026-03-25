<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory -->

Modulev1.2.13 (latest)●Since v1.0

# agent\_token\_buffer\_memory

Memory used to save agent output AND intermediate steps.

## Functions

[function

format\_to\_openai\_function\_messages

Convert (AgentAction, tool output) tuples into FunctionMessages.](/python/langchain-classic/agents/format_scratchpad/openai_functions/format_to_openai_function_messages)[function

format\_to\_tool\_messages

Convert (AgentAction, tool output) tuples into `ToolMessage` objects.](/python/langchain-classic/agents/format_scratchpad/tools/format_to_tool_messages)

## Classes

[class

AgentTokenBufferMemory

Memory used to save agent output AND intermediate steps.](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory)[deprecatedclass

BaseChatMemory

Abstract base class for chat memory.

**ATTENTION** This abstraction was created prior to when chat models had
native tool calling capabilities.
It does **NOT** support native tool calling capabilities for chat models and
will fail SILENTLY if used with a chat model that has native tool calling.

DO NOT USE THIS ABSTRACTION FOR NEW CODE.](/python/langchain-classic/memory/chat_memory/BaseChatMemory)


