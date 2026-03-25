<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/mrkl/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Attempt to implement MRKL systems as described in arxiv.org/pdf/2205.00445.pdf.

## Attributes

[attribute

AGENT\_DEPRECATION\_WARNING: str](/python/langchain-classic/_api/deprecation/AGENT_DEPRECATION_WARNING)[attribute

FORMAT\_INSTRUCTIONS: str](/python/langchain-classic/agents/mrkl/prompt/FORMAT_INSTRUCTIONS)[attribute

PREFIX: str](/python/langchain-classic/agents/mrkl/prompt/PREFIX)[attribute

SUFFIX: str](/python/langchain-classic/agents/mrkl/prompt/SUFFIX)

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

MRKLOutputParser

MRKL Output parser for the chat agent.](/python/langchain-classic/agents/mrkl/output_parser/MRKLOutputParser)[class

ChainConfig

Configuration for a chain to use in MRKL system.](/python/langchain-classic/agents/mrkl/base/ChainConfig)[deprecatedclass

Agent

Agent that calls the language model and deciding the action.

This is driven by a LLMChain. The prompt in the LLMChain MUST include
a variable called "agent\_scratchpad" where the agent can put its
intermediary work.](/python/langchain-classic/agents/agent/Agent)[deprecatedclass

AgentType

An enum for agent types.](/python/langchain-classic/agents/agent_types/AgentType)[deprecatedclass

ZeroShotAgent

Agent for the MRKL chain.](/python/langchain-classic/agents/mrkl/base/ZeroShotAgent)[deprecatedclass

MRKLChain

Chain that implements the MRKL system.](/python/langchain-classic/agents/mrkl/base/MRKLChain)


