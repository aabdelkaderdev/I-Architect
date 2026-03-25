<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/structured/StructuredPrompt/pipe -->

Methodv1.2.21 (latest)●Since v0.1

# pipe

Pipe the structured prompt to a language model.


```
pipe(
  self,
  *others: Runnable[Any, Other] | Callable[[Iterator[Any]], Iterator[Other]] | Callable[[AsyncIterator[Any]], AsyncIterator[Other]] | Callable[[Any], Other] | Mapping[str, Runnable[Any, Other] | Callable[[Any], Other] | Any] = (),
  name: str | None = None
) -> RunnableSerializable[dict, Other]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `others` | `Runnable[Any, Other] | Callable[[Iterator[Any]], Iterator[Other]] | Callable[[AsyncIterator[Any]], AsyncIterator[Other]] | Callable[[Any], Other] | Mapping[str, Runnable[Any, Other] | Callable[[Any], Other] | Any]` | Default:`()`  The language model to pipe the structured prompt to. |
| `name` | `str | None` | Default:`None`  The name of the pipeline. |


