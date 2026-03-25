<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/LLMSingleActionAgent -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# LLMSingleActionAgent

Base class for single action agents.


```
LLMSingleActionAgent()
```

## Bases

`BaseSingleActionAgent`

## Attributes

[attribute

llm\_chain: LLMChain

LLMChain to use for agent.](/python/langchain-classic/agents/agent/LLMSingleActionAgent/llm_chain)[attribute

output\_parser: AgentOutputParser

Output parser to use for agent.](/python/langchain-classic/agents/agent/LLMSingleActionAgent/output_parser)[attribute

stop: list[str]

List of strings to stop on.](/python/langchain-classic/agents/agent/LLMSingleActionAgent/stop)[attribute

input\_keys: list[str]

Return the input keys.](/python/langchain-classic/agents/agent/LLMSingleActionAgent/input_keys)

## Methods

[method

dict

Return dictionary representation of agent.](/python/langchain-classic/agents/agent/LLMSingleActionAgent/dict)[method

plan

Given input, decided what to do.](/python/langchain-classic/agents/agent/LLMSingleActionAgent/plan)[method

aplan

Async given input, decided what to do.](/python/langchain-classic/agents/agent/LLMSingleActionAgent/aplan)[method

tool\_run\_logging\_kwargs

Return logging kwargs for tool run.](/python/langchain-classic/agents/agent/LLMSingleActionAgent/tool_run_logging_kwargs)

## Inherited from[BaseSingleActionAgent](/python/langchain-classic/agents/agent/BaseSingleActionAgent)

### Attributes

[Areturn\_values: list[str]

—

Return values of the agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/return_values)

### Methods

[Mget\_allowed\_tools

—

Get allowed tools.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/get_allowed_tools)[Mreturn\_stopped\_response

—

Return response when agent has been stopped due to max iterations.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/return_stopped_response)[Mfrom\_llm\_and\_tools

—

Construct an agent from an LLM and tools.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/from_llm_and_tools)[Msave

—

Save the agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/save)


