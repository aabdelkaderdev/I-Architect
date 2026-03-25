<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/self_ask_with_search/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Chain that does self-ask with search.

## Attributes

[attribute

PROMPT](/python/langchain-classic/agents/self_ask_with_search/prompt/PROMPT)

## Functions

[function

format\_log\_to\_str

Construct the scratchpad that lets the agent continue its thought process.](/python/langchain-classic/agents/format_scratchpad/log/format_log_to_str)[function

validate\_tools\_single\_input

Validate tools for single input.](/python/langchain-classic/agents/utils/validate_tools_single_input)[function

create\_self\_ask\_with\_search\_agent

Create an agent that uses self-ask with search prompting.](/python/langchain-classic/agents/self_ask_with_search/base/create_self_ask_with_search_agent)

## Classes

[class

AgentExecutor

Agent that is using tools.](/python/langchain-classic/agents/agent/AgentExecutor)[class

AgentOutputParser

Base class for parsing agent output into agent action/finish.](/python/langchain-classic/agents/agent/AgentOutputParser)[class

SelfAskOutputParser

Parses self-ask style LLM calls.

Expects output to be in one of two formats.

If the output signals that an action should be taken,
should be in the below format. This will result in an AgentAction
being returned.

```
Thoughts go here...
Follow up: what is the temperature in SF?
```

If the output signals that a final answer should be given,
should be in the below format. This will result in an AgentFinish
being returned.

```
Thoughts go here...
So the final answer is: The temperature is 100 degrees
```](/python/langchain-classic/agents/output_parsers/self_ask/SelfAskOutputParser)[deprecatedclass

Agent

Agent that calls the language model and deciding the action.

This is driven by a LLMChain. The prompt in the LLMChain MUST include
a variable called "agent\_scratchpad" where the agent can put its
intermediary work.](/python/langchain-classic/agents/agent/Agent)[deprecatedclass

AgentType

An enum for agent types.](/python/langchain-classic/agents/agent_types/AgentType)[deprecatedclass

SelfAskWithSearchAgent

Agent for the self-ask-with-search paper.](/python/langchain-classic/agents/self_ask_with_search/base/SelfAskWithSearchAgent)[deprecatedclass

SelfAskWithSearchChain

[Deprecated] Chain that does self-ask with search.](/python/langchain-classic/agents/self_ask_with_search/base/SelfAskWithSearchChain)


