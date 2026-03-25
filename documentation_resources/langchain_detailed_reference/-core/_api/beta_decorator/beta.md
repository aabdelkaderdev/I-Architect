<!-- Source: https://reference.langchain.com/python/langchain-core/_api/beta_decorator/beta -->

Functionv1.2.21 (latest)●Since v0.1

# beta

Decorator to mark a function, a class, or a property as beta.

When marking a classmethod, a staticmethod, or a property, the `@beta` decorator
should go *under* `@classmethod` and `@staticmethod` (i.e., `beta` should directly
decorate the underlying callable), but *over* `@property`.

When marking a class `C` intended to be used as a base class in a multiple
inheritance hierarchy, `C` *must* define an `__init__` method (if `C` instead
inherited its `__init__` from its own base class, then `@beta` would mess up
`__init__` inheritance when installing its own (annotation-emitting) `C.__init__`).


```
beta(
  *,
  message: str = '',
  name: str = '',
  obj_type: str = '',
  addendum: str = ''
) -> Callable[[T], T]
```

**Example:**

```
@beta
def the_function_to_annotate():
    pass
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `message` | `str` | Default:`''`  Override the default beta message.  The %(since)s, %(name)s, %(alternative)s, %(obj\_type)s, %(addendum)s, and %(removal)s format specifiers will be replaced by the values of the respective arguments passed to this function. |
| `name` | `str` | Default:`''`  The name of the beta object. |
| `obj_type` | `str` | Default:`''`  The object type being beta. |
| `addendum` | `str` | Default:`''`  Additional text appended directly to the final message. |


