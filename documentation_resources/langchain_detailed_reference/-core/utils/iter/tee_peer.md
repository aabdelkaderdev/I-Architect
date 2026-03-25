<!-- Source: https://reference.langchain.com/python/langchain-core/utils/iter/tee_peer -->

Functionv1.2.21 (latest)●Since v0.1

# tee\_peer

An individual iterator of a `.tee`.

This function is a generator that yields items from the shared iterator `iterator`.
It buffers items until the least advanced iterator has yielded them as well. The
buffer is shared with all other peers.


```
tee_peer(
  iterator: Iterator[T],
  buffer: deque[T],
  peers: list[deque[T]],
  lock: AbstractContextManager[Any]
) -> Generator[T, None, None]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `iterator`\* | `Iterator[T]` | The shared iterator. |
| `buffer`\* | `deque[T]` | The buffer for this peer. |
| `peers`\* | `list[deque[T]]` | The buffers of all peers. |
| `lock`\* | `AbstractContextManager[Any]` | The lock to synchronise access to the shared buffers. |


