<!-- Source: https://reference.langchain.com/python/langchain-core/utils/pydantic/is_basemodel_instance -->

Functionv1.2.21 (latest)●Since v0.2

# is\_basemodel\_instance

Check if the given class is an instance of Pydantic `BaseModel`.

Check if the given class is an instance of any of the following:

- `pydantic.BaseModel` in Pydantic 2.x
- `pydantic.v1.BaseModel` in Pydantic 2.x


```
is_basemodel_instance(
    obj: Any,
) -> bool
```


