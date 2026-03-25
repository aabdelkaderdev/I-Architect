<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/AgentExecutor/trim_intermediate_steps -->

Attributev1.2.13 (latest)●Since v1.0

# trim\_intermediate\_steps

How to trim the intermediate steps before returning them.
Defaults to -1, which means no trimming.


```
trim_intermediate_steps: int | Callable[[list[tuple[AgentAction, str]]], list[tuple[AgentAction, str]]] = 1
```


