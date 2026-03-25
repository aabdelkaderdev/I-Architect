<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/stdout/StdOutCallbackHandler/on_chain_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chain\_start

Print out that we are entering a chain.


```
on_chain_start(
  self,
  serialized: dict[str, Any],
  inputs: dict[str, Any],
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized chain. |
| `inputs`\* | `dict[str, Any]` | The inputs to the chain. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


