<!-- Source: https://reference.langchain.com/python/langchain-core/load/dump/dumps -->

Functionv1.2.21 (latest)●Since v0.1

# dumps

Return a JSON string representation of an object.


```
dumps(
  obj: Any,
  *,
  pretty: bool = False,
  **kwargs: Any = {}
) -> str
```

**Note:**

Plain dicts containing an `'lc'` key are automatically escaped to prevent
confusion with LC serialization format. The escape marker is removed during
deserialization.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `obj`\* | `Any` | The object to dump. |
| `pretty` | `bool` | Default:`False`  Whether to pretty print the json.  If `True`, the json will be indented by either 2 spaces or the amount provided in the `indent` kwarg. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments to pass to `json.dumps` |


