<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/output_parsers/xml -->

Modulev1.2.13 (latest)●Since v1.0

# xml

## Classes

[class

AgentOutputParser

Base class for parsing agent output into agent action/finish.](/python/langchain-classic/agents/agent/AgentOutputParser)[class

XMLAgentOutputParser

Parses tool invocations and final answers from XML-formatted agent output.

This parser extracts structured information from XML tags to determine whether
an agent should perform a tool action or provide a final answer. It includes
built-in escaping support to safely handle tool names and inputs
containing XML special characters.](/python/langchain-classic/agents/output_parsers/xml/XMLAgentOutputParser)


