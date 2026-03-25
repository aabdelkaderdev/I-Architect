<!-- Source: https://reference.langchain.com/python/langchain-core/tools/base/get_all_basemodel_annotations -->

Functionv1.2.21 (latest)●Since v0.2

# get\_all\_basemodel\_annotations

Get all annotations from a Pydantic `BaseModel` and its parents.


```
get_all_basemodel_annotations(
  cls: TypeBaseModel | Any,
  *,
  default_to_bound: bool = True
) -> dict[str, type | TypeVar]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `cls`\* | `TypeBaseModel | Any` | The Pydantic `BaseModel` class. |
| `default_to_bound` | `bool` | Default:`True`  Whether to default to the bound of a `TypeVar` if it exists. |


