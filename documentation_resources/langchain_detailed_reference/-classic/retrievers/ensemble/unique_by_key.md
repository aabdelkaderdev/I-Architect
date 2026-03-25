<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/ensemble/unique_by_key -->

Functionv1.2.13 (latest)●Since v1.0

# unique\_by\_key

Yield unique elements of an iterable based on a key function.


```
unique_by_key(
    iterable: Iterable[T],
    key: Callable[[T], H],
) -> Iterator[T]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `iterable`\* | `Iterable[T]` | The iterable to filter. |
| `key`\* | `Callable[[T], H]` | A function that returns a hashable key for each element. |


