<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/base/Chain/aprep_inputs -->

Methodv1.2.13 (latest)●Since v1.0

# aprep\_inputs

Prepare chain inputs, including adding inputs from memory.


```
aprep_inputs(
    self,
    inputs: dict[str, Any] | Any,
) -> dict[str, str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `inputs`\* | `dict[str, Any] | Any` | Dictionary of raw inputs, or single input if chain expects only one param. Should contain all inputs specified in `Chain.input_keys` except for inputs that will be set by the chain's memory. |


