<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/tool_selection -->

Modulev1.2.13 (latest)●Since v1.0

# tool\_selection

LLM-based tool selector middleware.

## Attributes

[attribute

ResponseT](/python/langchain/agents/middleware/tool_selection/ResponseT)[attribute

logger](/python/langchain/agents/middleware/tool_selection/logger)[attribute

DEFAULT\_SYSTEM\_PROMPT: str](/python/langchain/agents/middleware/tool_selection/DEFAULT_SYSTEM_PROMPT)

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
for supported model parameters to use as `**kwargs`.](/python/langchain/agents/middleware/tool_selection/init_chat_model)

## Classes

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/tool_selection/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/tool_selection/AgentState)[class

ModelRequest

Model request information for the agent.](/python/langchain/agents/middleware/tool_selection/ModelRequest)[class

ModelResponse

Response from model execution including messages and optional structured output.

The result will usually contain a single `AIMessage`, but may include an additional
`ToolMessage` if the model used a tool for structured output.](/python/langchain/agents/middleware/tool_selection/ModelResponse)[class

LLMToolSelectorMiddleware

Uses an LLM to select relevant tools before calling the main model.

When an agent has many tools available, this middleware filters them down
to only the most relevant ones for the user's query. This reduces token usage
and helps the main model focus on the right tools.](/python/langchain/agents/middleware/tool_selection/LLMToolSelectorMiddleware)


