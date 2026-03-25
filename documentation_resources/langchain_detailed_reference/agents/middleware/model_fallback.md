<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/model_fallback -->

Modulev1.2.13 (latest)●Since v1.0

# model\_fallback

Model fallback middleware for agents.

## Attributes

[attribute

ResponseT](/python/langchain/agents/middleware/model_fallback/ResponseT)

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
for supported model parameters to use as `**kwargs`.](/python/langchain/agents/middleware/model_fallback/init_chat_model)

## Classes

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/model_fallback/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/model_fallback/AgentState)[class

ModelRequest

Model request information for the agent.](/python/langchain/agents/middleware/model_fallback/ModelRequest)[class

ModelResponse

Response from model execution including messages and optional structured output.

The result will usually contain a single `AIMessage`, but may include an additional
`ToolMessage` if the model used a tool for structured output.](/python/langchain/agents/middleware/model_fallback/ModelResponse)[class

ModelFallbackMiddleware

Automatic fallback to alternative models on errors.

Retries failed model calls with alternative models in sequence until
success or all models exhausted. Primary model specified in `create_agent`.](/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware)


