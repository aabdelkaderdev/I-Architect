<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/configurable/prefix_config_spec -->

Functionv1.2.21 (latest)●Since v0.1

# prefix\_config\_spec

Prefix the id of a `ConfigurableFieldSpec`.

This is useful when a `RunnableConfigurableAlternatives` is used as a
`ConfigurableField` of another `RunnableConfigurableAlternatives`.


```
prefix_config_spec(
    spec: ConfigurableFieldSpec,
    prefix: str,
) -> ConfigurableFieldSpec
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `spec`\* | `ConfigurableFieldSpec` | The `ConfigurableFieldSpec` to prefix. |
| `prefix`\* | `str` | The prefix to add. |


