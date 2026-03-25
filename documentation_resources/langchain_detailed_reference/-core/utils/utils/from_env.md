<!-- Source: https://reference.langchain.com/python/langchain-core/utils/utils/from_env -->

Functionv1.2.21 (latest)●Since v0.2

# from\_env

Create a factory method that gets a value from an environment variable.


```
from_env(
  key: str | Sequence[str],
  ,
  *,
  default: str | _NoDefaultType | None = _NoDefault,
  error_message: str | None = None
) -> Callable[[], str] | Callable[[], str | None]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `key`\* | `str | Sequence[str]` | The environment variable to look up.  If a list of keys is provided, the first key found in the environment will be used. If no key is found, the default value will be used if set, otherwise an error will be raised. |
| `default` | `str | _NoDefaultType | None` | Default:`_NoDefault`  The default value to return if the environment variable is not set. |
| `error_message` | `str | None` | Default:`None`  The error message which will be raised if the key is not found and no default value is provided.  This will be raised as a ValueError. |


