<!-- Source: https://reference.langchain.com/python/langchain-core/utils/aiter/tee_peer -->

Functionv1.2.21 (latest)●Since v0.1

# tee\_peer

An individual iterator of a `tee`.

This function is a generator that yields items from the shared iterator
`iterator`. It buffers items until the least advanced iterator has yielded them as
well.

The buffer is shared with all other peers.


```
tee_peer(
  iterator: AsyncIterator[T],
  buffer: deque[T],
  peers: list[deque[T]],
  lock: AbstractAsyncContextManager[Any]
) -> AsyncGenerator[T, None]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `iterator`\* | `AsyncIterator[T]` | The shared iterator. |
| `buffer`\* | `deque[T]` | The buffer for this peer. |
| `peers`\* | `list[deque[T]]` | The buffers of all peers. |
| `lock`\* | `AbstractAsyncContextManager[Any]` | The lock to synchronise access to the shared buffers. |


