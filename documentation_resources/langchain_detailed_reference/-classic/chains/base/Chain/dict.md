<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/base/Chain/dict -->

Methodv1.2.13 (latest)●Since v1.0

# dict

Dictionary representation of chain.

Expects `Chain._chain_type` property to be implemented and for memory to be
null.


```
dict(
    self,
    **kwargs: Any = {},
) -> dict
```

**Example:**

```
chain.model_dump(exclude_unset=True)
# -> {"_type": "foo", "verbose": False, ...}
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `**kwargs` | `Any` | Default:`{}`  Keyword arguments passed to default `pydantic.BaseModel.dict` method. |


