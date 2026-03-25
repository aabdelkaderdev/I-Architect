<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/loading/load_agent -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# load\_agent

Unified method for loading an agent from LangChainHub or local fs.


```
load_agent(
  path: str | Path,
  **kwargs: Any = {}
) -> BaseSingleActionAgent | BaseMultiActionAgent
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `path`\* | `str | Path` | Path to the agent file. |
| `kwargs` | `Any` | Default:`{}`  Additional keyword arguments passed to the agent executor. |


