<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/output_parsers/openai_functions -->

Modulev1.2.13 (latest)●Since v1.0

# openai\_functions

## Classes

[class

AgentOutputParser

Base class for parsing agent output into agent action/finish.](/python/langchain-classic/agents/agent/AgentOutputParser)[class

OpenAIFunctionsAgentOutputParser

Parses a message into agent action/finish.

Is meant to be used with OpenAI models, as it relies on the specific
function\_call parameter from OpenAI to convey what tools to use.

If a function\_call parameter is passed, then that is used to get
the tool and tool input.

If one is not passed, then the AIMessage is assumed to be the final output.](/python/langchain-classic/agents/output_parsers/openai_functions/OpenAIFunctionsAgentOutputParser)


