<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/output_parsers/openai_tools -->

Modulev1.2.13 (latest)●Since v1.0

# openai\_tools

## Attributes

[attribute

OpenAIToolAgentAction: ToolAgentAction](/python/langchain-classic/agents/output_parsers/openai_tools/OpenAIToolAgentAction)

## Functions

[function

parse\_ai\_message\_to\_tool\_action

Parse an AI message potentially containing tool\_calls.](/python/langchain-classic/agents/output_parsers/tools/parse_ai_message_to_tool_action)[function

parse\_ai\_message\_to\_openai\_tool\_action

Parse an AI message potentially containing tool\_calls.](/python/langchain-classic/agents/output_parsers/openai_tools/parse_ai_message_to_openai_tool_action)

## Classes

[class

MultiActionAgentOutputParser

Base class for parsing agent output into agent actions/finish.

This is used for agents that can return multiple actions.](/python/langchain-classic/agents/agent/MultiActionAgentOutputParser)[class

ToolAgentAction

Tool agent action.](/python/langchain-classic/agents/output_parsers/tools/ToolAgentAction)[class

OpenAIToolsAgentOutputParser

Parses a message into agent actions/finish.

Is meant to be used with OpenAI models, as it relies on the specific
tool\_calls parameter from OpenAI to convey what tools to use.

If a tool\_calls parameter is passed, then that is used to get
the tool names and tool inputs.

If one is not passed, then the AIMessage is assumed to be the final output.](/python/langchain-classic/agents/output_parsers/openai_tools/OpenAIToolsAgentOutputParser)


