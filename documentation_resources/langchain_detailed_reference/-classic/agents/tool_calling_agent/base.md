<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/tool_calling_agent/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

## Attributes

[attribute

MessageFormatter: Callable[[Sequence[tuple[AgentAction, str]]], list[BaseMessage]]](/python/langchain-classic/agents/tool_calling_agent/base/MessageFormatter)

## Functions

[function

format\_to\_tool\_messages

Convert (AgentAction, tool output) tuples into `ToolMessage` objects.](/python/langchain-classic/agents/format_scratchpad/tools/format_to_tool_messages)[function

create\_tool\_calling\_agent

Create an agent that uses tools.](/python/langchain-classic/agents/tool_calling_agent/base/create_tool_calling_agent)

## Classes

[class

ToolsAgentOutputParser

Parses a message into agent actions/finish.

If a tool\_calls parameter is passed, then that is used to get
the tool names and tool inputs.

If one is not passed, then the AIMessage is assumed to be the final output.](/python/langchain-classic/agents/output_parsers/tools/ToolsAgentOutputParser)


