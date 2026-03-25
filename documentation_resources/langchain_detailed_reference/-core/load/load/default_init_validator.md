<!-- Source: https://reference.langchain.com/python/langchain-core/load/load/default_init_validator -->

Functionv1.2.21 (latest)●Since v0.3

# default\_init\_validator

Default init validator that blocks jinja2 templates.

This is the default validator used by `load()` and `loads()` when no custom
validator is provided.


```
default_init_validator(
    class_path: tuple[str, ...],
    kwargs: dict[str, Any],
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `class_path`\* | `tuple[str, ...]` | The class path tuple being deserialized. |
| `kwargs`\* | `dict[str, Any]` | The kwargs dict for the class constructor. |


