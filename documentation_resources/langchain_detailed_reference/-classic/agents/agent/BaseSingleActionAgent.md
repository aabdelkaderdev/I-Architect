<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/BaseSingleActionAgent -->

Classv1.2.13 (latest)●Since v1.0

# BaseSingleActionAgent

Base Single Action Agent class.


```
BaseSingleActionAgent()
```

## Bases

`BaseModel`

## Attributes

[attribute

return\_values: list[str]

Return values of the agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/return_values)[attribute

input\_keys: list[str]

Return the input keys.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/input_keys)

## Methods

[method

get\_allowed\_tools

Get allowed tools.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/get_allowed_tools)[method

plan

Given input, decided what to do.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/plan)[method

aplan

Async given input, decided what to do.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/aplan)[method

return\_stopped\_response

Return response when agent has been stopped due to max iterations.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/return_stopped_response)[method

from\_llm\_and\_tools

Construct an agent from an LLM and tools.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/from_llm_and_tools)[method

dict

Return dictionary representation of agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/dict)[method

save

Save the agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/save)[method

tool\_run\_logging\_kwargs

Return logging kwargs for tool run.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/tool_run_logging_kwargs)


