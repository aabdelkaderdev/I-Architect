<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/conversational_chat/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

An agent designed to hold a conversation in addition to using tools.

## Attributes

[attribute

PREFIX: str](/python/langchain-classic/agents/conversational_chat/prompt/PREFIX)[attribute

SUFFIX: str](/python/langchain-classic/agents/conversational_chat/prompt/SUFFIX)[attribute

TEMPLATE\_TOOL\_RESPONSE: str](/python/langchain-classic/agents/conversational_chat/prompt/TEMPLATE_TOOL_RESPONSE)

## Functions

[function

validate\_tools\_single\_input

Validate tools for single input.](/python/langchain-classic/agents/utils/validate_tools_single_input)

## Classes

[class

AgentOutputParser

Base class for parsing agent output into agent action/finish.](/python/langchain-classic/agents/agent/AgentOutputParser)[class

ConvoOutputParser

Output parser for the conversational agent.](/python/langchain-classic/agents/conversational_chat/output_parser/ConvoOutputParser)[deprecatedclass

Agent

Agent that calls the language model and deciding the action.

This is driven by a LLMChain. The prompt in the LLMChain MUST include
a variable called "agent\_scratchpad" where the agent can put its
intermediary work.](/python/langchain-classic/agents/agent/Agent)[deprecatedclass

ConversationalChatAgent

An agent designed to hold a conversation in addition to using tools.](/python/langchain-classic/agents/conversational_chat/base/ConversationalChatAgent)


