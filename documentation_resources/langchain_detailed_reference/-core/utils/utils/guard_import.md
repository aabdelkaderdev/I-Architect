<!-- Source: https://reference.langchain.com/python/langchain-core/utils/utils/guard_import -->

Functionv1.2.21 (latest)●Since v0.1

# guard\_import

Dynamically import a module.

Raise an exception if the module is not installed.


```
guard_import(
  module_name: str,
  *,
  pip_name: str | None = None,
  package: str | None = None
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `module_name`\* | `str` | The name of the module to import. |
| `pip_name` | `str | None` | Default:`None`  The name of the module to install with pip. |
| `package` | `str | None` | Default:`None`  The package to import the module from. |


