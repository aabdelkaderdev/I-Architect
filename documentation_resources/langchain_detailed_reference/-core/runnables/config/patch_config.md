<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/config/patch_config -->

Functionv1.2.21 (latest)●Since v0.1

# patch\_config

Patch a config with new values.


```
patch_config(
  config: RunnableConfig | None,
  *,
  callbacks: BaseCallbackManager | None = None,
  recursion_limit: int | None = None,
  max_concurrency: int | None = None,
  run_name: str | None = None,
  configurable: dict[str, Any] | None = None
) -> RunnableConfig
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `config`\* | `RunnableConfig | None` | The config to patch. |
| `callbacks` | `BaseCallbackManager | None` | Default:`None`  The callbacks to set. |
| `recursion_limit` | `int | None` | Default:`None`  The recursion limit to set. |
| `max_concurrency` | `int | None` | Default:`None`  The max concurrency to set. |
| `run_name` | `str | None` | Default:`None`  The run name to set. |
| `configurable` | `dict[str, Any] | None` | Default:`None`  The configurable to set. |


