<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/transform/BaseTransformOutputParser/transform -->

Methodv1.2.21 (latest)●Since v0.1

# transform

Transform the input into the output format.


```
transform(
  self,
  input: Iterator[str | BaseMessage],
  config: RunnableConfig | None = None,
  **kwargs: Any = {}
) -> Iterator[T]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `Iterator[str | BaseMessage]` | The input to transform. |
| `config` | `RunnableConfig | None` | Default:`None`  The configuration to use for the transformation. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


