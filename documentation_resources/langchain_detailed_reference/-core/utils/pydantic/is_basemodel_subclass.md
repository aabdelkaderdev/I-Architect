<!-- Source: https://reference.langchain.com/python/langchain-core/utils/pydantic/is_basemodel_subclass -->

Functionv1.2.21 (latest)●Since v0.2

# is\_basemodel\_subclass

Check if the given class is a subclass of Pydantic `BaseModel`.

Check if the given class is a subclass of any of the following:

- `pydantic.BaseModel` in Pydantic 2.x
- `pydantic.v1.BaseModel` in Pydantic 2.x


```
is_basemodel_subclass(
    cls: type,
) -> bool
```


