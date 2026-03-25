<!-- Source: https://reference.langchain.com/python/langchain-core/_api/deprecation/warn_deprecated -->

Functionv1.2.21 (latest)●Since v0.1

# warn\_deprecated

Display a standardized deprecation.


```
warn_deprecated(
  since: str,
  *,
  message: str = '',
  name: str = '',
  alternative: str = '',
  alternative_import: str = '',
  pending: bool = False,
  obj_type: str = '',
  addendum: str = '',
  removal: str = '',
  package: str = ''
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `since`\* | `str` | The release at which this API became deprecated. |
| `message` | `str` | Default:`''`  Override the default deprecation message.  The `%(since)s`, `%(name)s`, `%(alternative)s`, `%(obj_type)s`, `%(addendum)s`, and `%(removal)s` format specifiers will be replaced by the values of the respective arguments passed to this function. |
| `name` | `str` | Default:`''`  The name of the deprecated object. |
| `alternative` | `str` | Default:`''`  An alternative API that the user may use in place of the deprecated API.  The deprecation warning will tell the user about this alternative if provided. |
| `alternative_import` | `str` | Default:`''`  An alternative import that the user may use instead. |
| `pending` | `bool` | Default:`False`  If `True`, uses a `PendingDeprecationWarning` instead of a `DeprecationWarning`.  Cannot be used together with removal. |
| `obj_type` | `str` | Default:`''`  The object type being deprecated. |
| `addendum` | `str` | Default:`''`  Additional text appended directly to the final message. |
| `removal` | `str` | Default:`''`  The expected removal version.  With the default (an empty string), a removal version is automatically computed from since. Set to other Falsy values to not schedule a removal date.  Cannot be used together with pending. |
| `package` | `str` | Default:`''`  The package of the deprecated object. |


