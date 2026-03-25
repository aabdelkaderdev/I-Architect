<!-- Source: https://reference.langchain.com/python/langchain-core/utils/iter/batch_iterate -->

Functionv1.2.21 (latest)●Since v0.1

# batch\_iterate

Utility batching function.


```
batch_iterate(
    size: int | None,
    iterable: Iterable[T],
) -> Iterator[list[T]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `size`\* | `int | None` | The size of the batch.  If `None`, returns a single batch. |
| `iterable`\* | `Iterable[T]` | The iterable to batch. |


