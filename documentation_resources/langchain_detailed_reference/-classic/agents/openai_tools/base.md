<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_tools/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

## Functions

[function

format\_to\_openai\_tool\_messages](/python/langchain-classic/agents/openai_tools/base/format_to_openai_tool_messages)[function

create\_openai\_tools\_agent

Create an agent that uses OpenAI tools.](/python/langchain-classic/agents/openai_tools/base/create_openai_tools_agent)

## Classes

[class

OpenAIToolsAgentOutputParser

Parses a message into agent actions/finish.

Is meant to be used with OpenAI models, as it relies on the specific
tool\_calls parameter from OpenAI to convey what tools to use.

If a tool\_calls parameter is passed, then that is used to get
the tool names and tool inputs.

If one is not passed, then the AIMessage is assumed to be the final output.](/python/langchain-classic/agents/output_parsers/openai_tools/OpenAIToolsAgentOutputParser)


