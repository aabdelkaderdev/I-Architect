<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_functions_agent/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Module implements an agent that uses OpenAI's APIs function enabled API.

## Functions

[function

format\_to\_openai\_function\_messages

Convert (AgentAction, tool output) tuples into FunctionMessages.](/python/langchain-classic/agents/format_scratchpad/openai_functions/format_to_openai_function_messages)[function

create\_openai\_functions\_agent

Create an agent that uses OpenAI function calling.](/python/langchain-classic/agents/openai_functions_agent/base/create_openai_functions_agent)

## Classes

[class

BaseSingleActionAgent

Base Single Action Agent class.](/python/langchain-classic/agents/agent/BaseSingleActionAgent)[class

OpenAIFunctionsAgentOutputParser

Parses a message into agent action/finish.

Is meant to be used with OpenAI models, as it relies on the specific
function\_call parameter from OpenAI to convey what tools to use.

If a function\_call parameter is passed, then that is used to get
the tool and tool input.

If one is not passed, then the AIMessage is assumed to be the final output.](/python/langchain-classic/agents/output_parsers/openai_functions/OpenAIFunctionsAgentOutputParser)[deprecatedclass

OpenAIFunctionsAgent

An Agent driven by OpenAIs function powered API.](/python/langchain-classic/agents/openai_functions_agent/base/OpenAIFunctionsAgent)


