<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/RunnableAgent/stream_runnable -->

Attributev1.2.13 (latest)●Since v1.0

# stream\_runnable

Whether to stream from the runnable or not.

If `True` then underlying LLM is invoked in a streaming fashion to make it possible
to get access to the individual LLM tokens when using stream\_log with the
`AgentExecutor`. If `False` then LLM is invoked in a non-streaming fashion and
individual LLM tokens will not be available in stream\_log.


```
stream_runnable: bool = True
```


