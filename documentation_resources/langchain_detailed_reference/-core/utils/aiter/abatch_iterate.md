<!-- Source: https://reference.langchain.com/python/langchain-core/utils/aiter/abatch_iterate -->

Functionv1.2.21 (latest)●Since v0.2

# abatch\_iterate

Utility batching function for async iterables.


```
abatch_iterate(
    size: int,
    iterable: AsyncIterable[T],
) -> AsyncIterator[list[T]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `size`\* | `int` | The size of the batch. |
| `iterable`\* | `AsyncIterable[T]` | The async iterable to batch. |


