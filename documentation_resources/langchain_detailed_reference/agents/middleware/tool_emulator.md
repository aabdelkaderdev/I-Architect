<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/tool_emulator -->

Modulev1.2.13 (latest)●Since v1.0

# tool\_emulator

Tool emulator middleware for testing.

## Functions

[function

init\_chat\_model

Initialize a chat model from any supported provider using a unified interface.

**Two main use cases:**

1. **Fixed model** – specify the model upfront and get a ready-to-use chat model.
2. **Configurable model** – choose to specify parameters (including model name) at
   runtime via `config`. Makes it easy to switch between models/providers without
   changing your code

Installation requirements

Requires the integration package for the chosen model provider to be installed.

See the `model_provider` parameter below for specific package names
(e.g., `pip install langchain-openai`).

Refer to the [provider integration's API reference](https://docs.langchain.com/oss/python/integrations/providers)
for supported model parameters to use as `**kwargs`.](/python/langchain/agents/middleware/tool_emulator/init_chat_model)

## Classes

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/tool_emulator/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/tool_emulator/AgentState)[class

LLMToolEmulator

Emulates specified tools using an LLM instead of executing them.

This middleware allows selective emulation of tools for testing purposes.

By default (when `tools=None`), all tools are emulated. You can specify which
tools to emulate by passing a list of tool names or `BaseTool` instances.](/python/langchain/agents/middleware/tool_emulator/LLMToolEmulator)


