<!-- Source: https://reference.langchain.com/python/langchain-core/_api/deprecation/deprecated -->

Functionv1.2.21 (latest)●Since v0.1

# deprecated

Decorator to mark a function, a class, or a property as deprecated.

When deprecating a classmethod, a staticmethod, or a property, the `@deprecated`
decorator should go *under* `@classmethod` and `@staticmethod` (i.e., `deprecated`
should directly decorate the underlying callable), but *over* `@property`.

When deprecating a class `C` intended to be used as a base class in a multiple
inheritance hierarchy, `C` *must* define an `__init__` method (if `C` instead
inherited its `__init__` from its own base class, then `@deprecated` would mess up
`__init__` inheritance when installing its own (deprecation-emitting) `C.__init__`).

Parameters are the same as for `warn_deprecated`, except that *obj\_type* defaults to
'class' if decorating a class, 'attribute' if decorating a property, and 'function'
otherwise.


```
deprecated(
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
) -> Callable[[T], T]
```

**Example:**

```
@deprecated("1.4.0")
def the_function_to_deprecate():
    pass
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


