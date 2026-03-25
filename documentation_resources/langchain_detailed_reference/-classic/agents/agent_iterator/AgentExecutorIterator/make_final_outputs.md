<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/make_final_outputs -->

Methodv1.2.13 (latest)●Since v1.0

# make\_final\_outputs

Make final outputs for the iterator.


```
make_final_outputs(
  self,
  outputs: dict[str, Any],
  run_manager: CallbackManagerForChainRun | AsyncCallbackManagerForChainRun
) -> AddableDict
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `outputs`\* | `dict[str, Any]` | The outputs from the agent executor. |
| `run_manager`\* | `CallbackManagerForChainRun | AsyncCallbackManagerForChainRun` | The run manager to use for callbacks. |


