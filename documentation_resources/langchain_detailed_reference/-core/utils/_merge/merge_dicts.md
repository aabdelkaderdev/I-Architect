<!-- Source: https://reference.langchain.com/python/langchain-core/utils/_merge/merge_dicts -->

Functionv1.2.21 (latest)●Since v0.1

# merge\_dicts

Merge dictionaries.

Merge many dicts, handling specific scenarios where a key exists in both
dictionaries but has a value of `None` in `'left'`. In such cases, the method uses
the value from `'right'` for that key in the merged dictionary.


```
merge_dicts(
    left: dict[str, Any],
    *others: dict[str, Any] = (),
) -> dict[str, Any]
```

**Example:**

If `left = {"function_call": {"arguments": None}}` and
`right = {"function_call": {"arguments": "{\n"}}`, then, after merging, for the
key `'function_call'`, the value from `'right'` is used, resulting in
`merged = {"function_call": {"arguments": "{\n"}}`.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `left`\* | `dict[str, Any]` | The first dictionary to merge. |
| `others` | `dict[str, Any]` | Default:`()`  The other dictionaries to merge. |


