<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/with_types -->

Methodv1.2.21 (latest)●Since v0.1

# with\_types

Bind input and output types to a `Runnable`, returning a new `Runnable`.


```
with_types(
  self,
  *,
  input_type: type[Input] | None = None,
  output_type: type[Output] | None = None
) -> Runnable[Input, Output]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input_type` | `type[Input] | None` | Default:`None`  The input type to bind to the `Runnable`. |
| `output_type` | `type[Output] | None` | Default:`None`  The output type to bind to the `Runnable`. |


