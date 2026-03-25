<!-- Source: https://reference.langchain.com/python/langchain-core/load/dump/dumpd -->

Functionv1.2.21 (latest)●Since v0.1

# dumpd

Return a dict representation of an object.


```
dumpd(
    obj: Any,
) -> Any
```

**Note:**

Plain dicts containing an `'lc'` key are automatically escaped to prevent
confusion with LC serialization format. The escape marker is removed during
deserialization.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `obj`\* | `Any` | The object to dump. |


