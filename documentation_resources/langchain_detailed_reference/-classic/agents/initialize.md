<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/initialize -->

Modulev1.2.13 (latest)●Since v1.0

# initialize

Load agent.

## Attributes

[attribute

AGENT\_DEPRECATION\_WARNING: str](/python/langchain-classic/_api/deprecation/AGENT_DEPRECATION_WARNING)[attribute

AGENT\_TO\_CLASS: dict[AgentType, AGENT\_TYPE]](/python/langchain-classic/agents/types/AGENT_TO_CLASS)

## Functions

[deprecatedfunction

load\_agent

Unified method for loading an agent from LangChainHub or local fs.](/python/langchain-classic/agents/loading/load_agent)[deprecatedfunction

initialize\_agent

Load an agent executor given tools and LLM.

Warning

This function is no deprecated in favor of
[`create_agent`](/python/langchain/agents/create_agent) from the `langchain`
package, which provides a more flexible agent factory with middleware
support, structured output, and integration with LangGraph.

For migration guidance, see
[Migrating to langchain v1](https://docs.langchain.com/oss/python/migrate/langchain-v1)
and
[Migrating from AgentExecutor](https://python.langchain.com/docs/how_to/migrate_agent/).](/python/langchain-classic/agents/initialize/initialize_agent)

## Classes

[class

AgentExecutor

Agent that is using tools.](/python/langchain-classic/agents/agent/AgentExecutor)[deprecatedclass

AgentType

An enum for agent types.](/python/langchain-classic/agents/agent_types/AgentType)


