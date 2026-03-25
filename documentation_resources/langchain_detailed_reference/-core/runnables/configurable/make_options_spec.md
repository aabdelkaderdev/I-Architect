<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/configurable/make_options_spec -->

Functionv1.2.21 (latest)●Since v0.1

# make\_options\_spec

Make options spec.

Make a `ConfigurableFieldSpec` for a `ConfigurableFieldSingleOption` or
`ConfigurableFieldMultiOption`.


```
make_options_spec(
  spec: ConfigurableFieldSingleOption | ConfigurableFieldMultiOption,
  description: str | None
) -> ConfigurableFieldSpec
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `spec`\* | `ConfigurableFieldSingleOption | ConfigurableFieldMultiOption` | The `ConfigurableFieldSingleOption` or `ConfigurableFieldMultiOption`. |
| `description`\* | `str | None` | The description to use if the spec does not have one. |


