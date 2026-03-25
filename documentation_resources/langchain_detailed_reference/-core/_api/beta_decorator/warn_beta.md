<!-- Source: https://reference.langchain.com/python/langchain-core/_api/beta_decorator/warn_beta -->

Functionv1.2.21 (latest)●Since v0.1

# warn\_beta

Display a standardized beta annotation.


```
warn_beta(
  *,
  message: str = '',
  name: str = '',
  obj_type: str = '',
  addendum: str = ''
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `message` | `str` | Default:`''`  Override the default beta message.  The %(name)s, %(obj\_type)s, %(addendum)s format specifiers will be replaced by the values of the respective arguments passed to this function. |
| `name` | `str` | Default:`''`  The name of the annotated object. |
| `obj_type` | `str` | Default:`''`  The object type being annotated. |
| `addendum` | `str` | Default:`''`  Additional text appended directly to the final message. |


