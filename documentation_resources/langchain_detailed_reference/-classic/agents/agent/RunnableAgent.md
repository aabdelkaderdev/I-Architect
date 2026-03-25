<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/RunnableAgent -->

Classv1.2.13 (latest)●Since v1.0

# RunnableAgent

Agent powered by Runnables.


```
RunnableAgent()
```

## Bases

`BaseSingleActionAgent`

## Attributes

[attribute

runnable: Runnable[dict, AgentAction | AgentFinish]

Runnable to call to get agent action.](/python/langchain-classic/agents/agent/RunnableAgent/runnable)[attribute

input\_keys\_arg: list[str]](/python/langchain-classic/agents/agent/RunnableAgent/input_keys_arg)[attribute

return\_keys\_arg: list[str]](/python/langchain-classic/agents/agent/RunnableAgent/return_keys_arg)[attribute

stream\_runnable: bool

Whether to stream from the runnable or not.

If `True` then underlying LLM is invoked in a streaming fashion to make it possible
to get access to the individual LLM tokens when using stream\_log with the
`AgentExecutor`. If `False` then LLM is invoked in a non-streaming fashion and
individual LLM tokens will not be available in stream\_log.](/python/langchain-classic/agents/agent/RunnableAgent/stream_runnable)[attribute

model\_config](/python/langchain-classic/agents/agent/RunnableAgent/model_config)[attribute

return\_values: list[str]

Return values of the agent.](/python/langchain-classic/agents/agent/RunnableAgent/return_values)[attribute

input\_keys: list[str]

Return the input keys.](/python/langchain-classic/agents/agent/RunnableAgent/input_keys)

## Methods

[method

plan

Based on past history and current inputs, decide what to do.](/python/langchain-classic/agents/agent/RunnableAgent/plan)[method

aplan

Async based on past history and current inputs, decide what to do.](/python/langchain-classic/agents/agent/RunnableAgent/aplan)

## Inherited from[BaseSingleActionAgent](/python/langchain-classic/agents/agent/BaseSingleActionAgent)

### Methods

[Mget\_allowed\_tools

—

Get allowed tools.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/get_allowed_tools)[Mreturn\_stopped\_response

—

Return response when agent has been stopped due to max iterations.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/return_stopped_response)[Mfrom\_llm\_and\_tools

—

Construct an agent from an LLM and tools.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/from_llm_and_tools)[Mdict

—

Return dictionary representation of agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/dict)[Msave

—

Save the agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/save)[Mtool\_run\_logging\_kwargs

—

Return logging kwargs for tool run.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/tool_run_logging_kwargs)


