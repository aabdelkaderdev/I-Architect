<!-- Source: https://reference.langchain.com/python/langchain-core/agents/AgentFinish/log -->

Attributev1.2.21 (latest)●Since v0.1

# log

Additional information to log about the return value.

This is used to pass along the full LLM prediction, not just the parsed out
return value.

For example, if the full LLM prediction was `Final Answer: 2` you may want to just
return `2` as a return value, but pass along the full string as a `log` (for
debugging or observability purposes).


```
log: str
```


