<!-- Source: https://reference.langchain.com/python/langchain-core/_api/deprecation/rename_parameter -->

Functionv1.2.21 (latest)●Since v0.2

# rename\_parameter

Decorator indicating that parameter *old* of *func* is renamed to *new*.

The actual implementation of *func* should use *new*, not *old*. If *old* is passed
to *func*, a `DeprecationWarning` is emitted, and its value is used, even if *new*
is also passed by keyword.


```
rename_parameter(
  *,
  since: str,
  removal: str,
  old: str,
  new: str
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]
```

**Example:**

```
@_api.rename_parameter("3.1", "bad_name", "good_name")
def func(good_name): ...
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `since`\* | `str` | The version in which the parameter was renamed. |
| `removal`\* | `str` | The version in which the old parameter will be removed. |
| `old`\* | `str` | The old parameter name. |
| `new`\* | `str` | The new parameter name. |


