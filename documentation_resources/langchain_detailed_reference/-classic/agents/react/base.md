<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/react/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Chain that implements the ReAct paper from <https://arxiv.org/pdf/2210.03629.pdf>.

## Attributes

[attribute

AGENT\_DEPRECATION\_WARNING: str](/python/langchain-classic/_api/deprecation/AGENT_DEPRECATION_WARNING)[attribute

TEXTWORLD\_PROMPT](/python/langchain-classic/agents/react/textworld_prompt/TEXTWORLD_PROMPT)[attribute

WIKI\_PROMPT](/python/langchain-classic/agents/react/wiki_prompt/WIKI_PROMPT)

## Functions

[function

validate\_tools\_single\_input

Validate tools for single input.](/python/langchain-classic/agents/utils/validate_tools_single_input)

## Classes

[class

AgentExecutor

Agent that is using tools.](/python/langchain-classic/agents/agent/AgentExecutor)[class

AgentOutputParser

Base class for parsing agent output into agent action/finish.](/python/langchain-classic/agents/agent/AgentOutputParser)[class

ReActOutputParser

Output parser for the ReAct agent.](/python/langchain-classic/agents/react/output_parser/ReActOutputParser)[deprecatedclass

Agent

Agent that calls the language model and deciding the action.

This is driven by a LLMChain. The prompt in the LLMChain MUST include
a variable called "agent\_scratchpad" where the agent can put its
intermediary work.](/python/langchain-classic/agents/agent/Agent)[deprecatedclass

AgentType

An enum for agent types.](/python/langchain-classic/agents/agent_types/AgentType)[deprecatedclass

ReActDocstoreAgent

Agent for the ReAct chain.](/python/langchain-classic/agents/react/base/ReActDocstoreAgent)[deprecatedclass

DocstoreExplorer

Class to assist with exploration of a document store.](/python/langchain-classic/agents/react/base/DocstoreExplorer)[deprecatedclass

ReActTextWorldAgent

Agent for the ReAct TextWorld chain.](/python/langchain-classic/agents/react/base/ReActTextWorldAgent)[deprecatedclass

ReActChain

[Deprecated] Chain that implements the ReAct paper.](/python/langchain-classic/agents/react/base/ReActChain)


