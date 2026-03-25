<!-- Source: https://reference.langchain.com/python/langchain-core/utils/utils/secret_from_env -->

Functionv1.2.21 (latest)●Since v0.2

# secret\_from\_env

Secret from env.


```
secret_from_env(
  key: str | Sequence[str],
  ,
  *,
  default: str | _NoDefaultType | None = _NoDefault,
  error_message: str | None = None
) -> Callable[[], SecretStr | None] | Callable[[], SecretStr]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `key`\* | `str | Sequence[str]` | The environment variable to look up. |
| `default` | `str | _NoDefaultType | None` | Default:`_NoDefault`  The default value to return if the environment variable is not set. |
| `error_message` | `str | None` | Default:`None`  The error message which will be raised if the key is not found and no default value is provided.  This will be raised as a `ValueError`. |


