<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/BaseMultiActionAgent -->

Classv1.2.13 (latest)●Since v1.0

# BaseMultiActionAgent

Base Multi Action Agent class.


```
BaseMultiActionAgent()
```

## Bases

`BaseModel`

## Attributes

[attribute

return\_values: list[str]

Return values of the agent.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/return_values)[attribute

input\_keys: list[str]

Return the input keys.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/input_keys)

## Methods

[method

get\_allowed\_tools

Get allowed tools.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/get_allowed_tools)[method

plan

Given input, decided what to do.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/plan)[method

aplan

Async given input, decided what to do.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/aplan)[method

return\_stopped\_response

Return response when agent has been stopped due to max iterations.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/return_stopped_response)[method

dict

Return dictionary representation of agent.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/dict)[method

save

Save the agent.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/save)[method

tool\_run\_logging\_kwargs

Return logging kwargs for tool run.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/tool_run_logging_kwargs)


