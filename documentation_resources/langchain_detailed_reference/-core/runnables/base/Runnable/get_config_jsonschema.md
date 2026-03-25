<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/get_config_jsonschema -->

Methodv1.2.21 (latest)●Since v0.3

# get\_config\_jsonschema


```
get_config_jsonschema(
  self,
  *,
  include: Sequence[str] | None = None
) -> dict
```



[

[str](https://docs.python.org/3/library/stdtypes.html#str)

,

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

]

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `include` | `Sequence[str] | None` | Default:`None` |

Get a JSON schema that represents the config of the `Runnable`.

A list of fields to include in the config schema.