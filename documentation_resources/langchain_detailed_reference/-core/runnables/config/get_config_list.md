<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/config/get_config_list -->

Functionv1.2.21 (latest)●Since v0.1

# get\_config\_list

Get a list of configs from a single config or a list of configs.

It is useful for subclasses overriding batch() or abatch().


```
get_config_list(
  config: RunnableConfig | Sequence[RunnableConfig] | None,
  length: int
) -> list[RunnableConfig]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `config`\* | `RunnableConfig | Sequence[RunnableConfig] | None` | The config or list of configs. |
| `length`\* | `int` | The length of the list. |


