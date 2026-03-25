<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/RunnableMultiActionAgent -->

Classv1.2.13 (latest)●Since v1.0

# RunnableMultiActionAgent

Agent powered by Runnables.


```
RunnableMultiActionAgent()
```

## Bases

`BaseMultiActionAgent`

## Attributes

[attribute

runnable: Runnable[dict, list[AgentAction] | AgentFinish]

Runnable to call to get agent actions.](/python/langchain-classic/agents/agent/RunnableMultiActionAgent/runnable)[attribute

input\_keys\_arg: list[str]](/python/langchain-classic/agents/agent/RunnableMultiActionAgent/input_keys_arg)[attribute

return\_keys\_arg: list[str]](/python/langchain-classic/agents/agent/RunnableMultiActionAgent/return_keys_arg)[attribute

stream\_runnable: bool

Whether to stream from the runnable or not.

If `True` then underlying LLM is invoked in a streaming fashion to make it possible
to get access to the individual LLM tokens when using stream\_log with the
`AgentExecutor`. If `False` then LLM is invoked in a non-streaming fashion and
individual LLM tokens will not be available in stream\_log.](/python/langchain-classic/agents/agent/RunnableMultiActionAgent/stream_runnable)[attribute

model\_config](/python/langchain-classic/agents/agent/RunnableMultiActionAgent/model_config)[attribute

return\_values: list[str]

Return values of the agent.](/python/langchain-classic/agents/agent/RunnableMultiActionAgent/return_values)[attribute

input\_keys: list[str]

Return the input keys.](/python/langchain-classic/agents/agent/RunnableMultiActionAgent/input_keys)

## Methods

[method

plan

Based on past history and current inputs, decide what to do.](/python/langchain-classic/agents/agent/RunnableMultiActionAgent/plan)[method

aplan

Async based on past history and current inputs, decide what to do.](/python/langchain-classic/agents/agent/RunnableMultiActionAgent/aplan)

## Inherited from[BaseMultiActionAgent](/python/langchain-classic/agents/agent/BaseMultiActionAgent)

### Methods

[Mget\_allowed\_tools

—

Get allowed tools.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/get_allowed_tools)[Mreturn\_stopped\_response

—

Return response when agent has been stopped due to max iterations.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/return_stopped_response)[Mdict

—

Return dictionary representation of agent.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/dict)[Msave

—

Save the agent.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/save)[Mtool\_run\_logging\_kwargs

—

Return logging kwargs for tool run.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/tool_run_logging_kwargs)


