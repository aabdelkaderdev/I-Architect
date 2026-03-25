<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/base/Chain/aprep_outputs -->

Methodv1.2.13 (latest)●Since v1.0

# aprep\_outputs

Validate and prepare chain outputs, and save info about this run to memory.


```
aprep_outputs(
  self,
  inputs: dict[str, str],
  outputs: dict[str, str],
  return_only_outputs: bool = False
) -> dict[str, str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `inputs`\* | `dict[str, str]` | Dictionary of chain inputs, including any inputs added by chain memory. |
| `outputs`\* | `dict[str, str]` | Dictionary of initial chain outputs. |
| `return_only_outputs` | `bool` | Default:`False`  Whether to only return the chain outputs. If `False`, inputs are also added to the final outputs. |


