<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/Agent -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# Agent

Agent that calls the language model and deciding the action.

This is driven by a LLMChain. The prompt in the LLMChain MUST include
a variable called "agent\_scratchpad" where the agent can put its
intermediary work.


```
Agent()
```

## Bases

`BaseSingleActionAgent`

## Attributes

[attribute

llm\_chain: LLMChain

LLMChain to use for agent.](/python/langchain-classic/agents/agent/Agent/llm_chain)[attribute

output\_parser: AgentOutputParser

Output parser to use for agent.](/python/langchain-classic/agents/agent/Agent/output_parser)[attribute

allowed\_tools: list[str] | None

Allowed tools for the agent. If `None`, all tools are allowed.](/python/langchain-classic/agents/agent/Agent/allowed_tools)[attribute

return\_values: list[str]

Return values of the agent.](/python/langchain-classic/agents/agent/Agent/return_values)[attribute

input\_keys: list[str]

Return the input keys.](/python/langchain-classic/agents/agent/Agent/input_keys)[attribute

observation\_prefix: str

Prefix to append the observation with.](/python/langchain-classic/agents/agent/Agent/observation_prefix)[attribute

llm\_prefix: str

Prefix to append the LLM call with.](/python/langchain-classic/agents/agent/Agent/llm_prefix)

## Methods

[method

dict

Return dictionary representation of agent.](/python/langchain-classic/agents/agent/Agent/dict)[method

get\_allowed\_tools

Get allowed tools.](/python/langchain-classic/agents/agent/Agent/get_allowed_tools)[method

plan

Given input, decided what to do.](/python/langchain-classic/agents/agent/Agent/plan)[method

aplan

Async given input, decided what to do.](/python/langchain-classic/agents/agent/Agent/aplan)[method

get\_full\_inputs

Create the full inputs for the LLMChain from intermediate steps.](/python/langchain-classic/agents/agent/Agent/get_full_inputs)[method

validate\_prompt

Validate that prompt matches format.](/python/langchain-classic/agents/agent/Agent/validate_prompt)[method

create\_prompt

Create a prompt for this class.](/python/langchain-classic/agents/agent/Agent/create_prompt)[method

from\_llm\_and\_tools

Construct an agent from an LLM and tools.](/python/langchain-classic/agents/agent/Agent/from_llm_and_tools)[method

return\_stopped\_response

Return response when agent has been stopped due to max iterations.](/python/langchain-classic/agents/agent/Agent/return_stopped_response)[method

tool\_run\_logging\_kwargs

Return logging kwargs for tool run.](/python/langchain-classic/agents/agent/Agent/tool_run_logging_kwargs)

## Inherited from[BaseSingleActionAgent](/python/langchain-classic/agents/agent/BaseSingleActionAgent)

### Methods

[Msave

—

Save the agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/save)


