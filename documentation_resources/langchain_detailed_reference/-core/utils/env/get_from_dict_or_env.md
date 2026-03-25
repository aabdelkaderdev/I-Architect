<!-- Source: https://reference.langchain.com/python/langchain-core/utils/env/get_from_dict_or_env -->

Functionv1.2.21 (latest)●Since v0.1

# get\_from\_dict\_or\_env

Get a value from a dictionary or an environment variable.


```
get_from_dict_or_env(
  data: dict[str, Any],
  key: str | list[str],
  env_key: str,
  default: str | None = None
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `data`\* | `dict[str, Any]` | The dictionary to look up the key in. |
| `key`\* | `str | list[str]` | The key to look up in the dictionary.  This can be a list of keys to try in order. |
| `env_key`\* | `str` | The environment variable to look up if the key is not in the dictionary. |
| `default` | `str | None` | Default:`None`  The default value to return if the key is not in the dictionary or the environment. |


