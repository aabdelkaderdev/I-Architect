<!-- Source: https://reference.langchain.com/python/langchain-core/utils/_merge/merge_obj -->

Functionv1.2.21 (latest)●Since v0.2

# merge\_obj

Merge two objects.

It handles specific scenarios where a key exists in both dictionaries but has a
value of `None` in `'left'`. In such cases, the method uses the value from `'right'`
for that key in the merged dictionary.


```
merge_obj(
    left: Any,
    right: Any,
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `left`\* | `Any` | The first object to merge. |
| `right`\* | `Any` | The other object to merge. |


