<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/transform/BaseTransformOutputParser/atransform -->

Methodv1.2.21 (latest)●Since v0.1

# atransform

Async transform the input into the output format.


```
atransform(
  self,
  input: AsyncIterator[str | BaseMessage],
  config: RunnableConfig | None = None,
  **kwargs: Any = {}
) -> AsyncIterator[T]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `AsyncIterator[str | BaseMessage]` | The input to transform. |
| `config` | `RunnableConfig | None` | Default:`None`  The configuration to use for the transformation. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


