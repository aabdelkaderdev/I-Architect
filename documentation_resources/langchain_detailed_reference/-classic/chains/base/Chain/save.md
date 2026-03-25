<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/base/Chain/save -->

Methodv1.2.13 (latest)●Since v1.0

# save

Save the chain.

Expects `Chain._chain_type` property to be implemented and for memory to be
null.


```
save(
    self,
    file_path: Path | str,
) -> None
```

**Example:**

```
chain.save(file_path="path/chain.yaml")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `file_path`\* | `Path | str` | Path to file to save the chain to. |


