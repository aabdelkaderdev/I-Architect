<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/context/register_configure_hook -->

Functionv1.2.21 (latest)●Since v0.1

# register\_configure\_hook

Register a configure hook.


```
register_configure_hook(
  context_var: ContextVar[Any | None],
  inheritable: bool,
  handle_class: type[BaseCallbackHandler] | None = None,
  env_var: str | None = None
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `context_var`\* | `ContextVar[Any | None]` | The context variable. |
| `inheritable`\* | `bool` | Whether the context variable is inheritable. |
| `handle_class` | `type[BaseCallbackHandler] | None` | Default:`None`  The callback handler class. |
| `env_var` | `str | None` | Default:`None`  The environment variable. |


