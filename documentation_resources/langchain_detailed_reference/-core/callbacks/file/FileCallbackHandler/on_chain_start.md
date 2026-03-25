<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/file/FileCallbackHandler/on_chain_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chain\_start

Print that we are entering a chain.


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
| `serialized`\* | `dict[str, Any]` | The serialized chain information. |
| `inputs`\* | `dict[str, Any]` | The inputs to the chain. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments that may contain `'name'`. |


