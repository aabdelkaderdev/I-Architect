<!-- Source: https://reference.langchain.com/python/langchain-core/agents -->

Modulev1.2.21 (latest)●Since v0.1

# agents

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

The schemas for the agents themselves are defined in `langchain.agents.agent`.

## Classes

[class

Serializable

Serializable base class.

This class is used to serialize objects to JSON.

It relies on the following methods and properties:

- [`is_lc_serializable`](/python/langchain-core/load/serializable/Serializable/is_lc_serializable): Is this class serializable?

  By design, even if a class inherits from `Serializable`, it is not serializable
  by default. This is to prevent accidental serialization of objects that should
  not be serialized.
- [`get_lc_namespace`](/python/langchain-core/load/serializable/Serializable/get_lc_namespace): Get the namespace of the LangChain object.

  During deserialization, this namespace is used to identify
  the correct class to instantiate.

  Please see the `Reviver` class in `langchain_core.load.load` for more details.

  During deserialization an additional mapping is handle classes that have moved
  or been renamed across package versions.
- [`lc_secrets`](/python/langchain-core/load/serializable/Serializable/lc_secrets): A map of constructor argument names to secret ids.
- [`lc_attributes`](/python/langchain-core/load/serializable/Serializable/lc_attributes): List of additional attribute names that should be included
  as part of the serialized representation.](/python/langchain-core/load/serializable/Serializable)[class

AIMessage

Message from an AI.

An `AIMessage` is returned from a chat model as a response to a prompt.

This message represents the output of the model and consists of both
the raw output as returned by the model and standardized fields
(e.g., tool calls, usage metadata) added by the LangChain framework.](/python/langchain-core/messages/ai/AIMessage)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

FunctionMessage

Message for passing the result of executing a tool back to a model.

`FunctionMessage` are an older version of the `ToolMessage` schema, and
do not contain the `tool_call_id` field.

The `tool_call_id` field is used to associate the tool call request with the
tool call response. Useful in situations where a chat model is able
to request multiple tool calls in parallel.](/python/langchain-core/messages/function/FunctionMessage)[class

HumanMessage

Message from the user.

A `HumanMessage` is a message that is passed in from a user to the model.](/python/langchain-core/messages/human/HumanMessage)[class

AgentAction

Represents a request to execute an action by an agent.

The action consists of the name of the tool to execute and the input to pass
to the tool. The log is used to pass along extra information about the action.](/python/langchain-core/agents/AgentAction)[class

AgentActionMessageLog

Representation of an action to be executed by an agent.

This is similar to `AgentAction`, but includes a message log consisting of
chat messages.

This is useful when working with `ChatModels`, and is used to reconstruct
conversation history from the agent's perspective.](/python/langchain-core/agents/AgentActionMessageLog)[class

AgentStep

Result of running an `AgentAction`.](/python/langchain-core/agents/AgentStep)[class

AgentFinish

Final return value of an `ActionAgent`.

Agents return an `AgentFinish` when they have reached a stopping condition.](/python/langchain-core/agents/AgentFinish)


