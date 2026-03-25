<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/AgentExecutor/early_stopping_method -->

Attributev1.2.13 (latest)●Since v1.0

# early\_stopping\_method

The method to use for early stopping if the agent never
returns `AgentFinish`. Either 'force' or 'generate'.

`"force"` returns a string saying that it stopped because it met a
time or iteration limit.

`"generate"` calls the agent's LLM Chain one final time to generate
a final answer based on the previous steps.


```
early_stopping_method: str = 'force'
```


