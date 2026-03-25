<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/BaseMultiActionAgent/save -->

Methodv1.2.13 (latest)●Since v1.0

# save

Save the agent.


```
save(
    self,
    file_path: Path | str,
) -> None
```

Example:

```
# If working with agent executor
agent.agent.save(file_path="path/agent.yaml")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `file_path`\* | `Path | str` | Path to file to save the agent to. |


