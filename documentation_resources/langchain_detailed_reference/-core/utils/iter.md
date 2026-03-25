<!-- Source: https://reference.langchain.com/python/langchain-core/utils/iter -->

Modulev1.2.21 (latest)●Since v0.1

# iter

Utilities for working with iterators.

## Attributes

[attribute

T](/python/langchain-core/utils/iter/T)[attribute

safetee: Tee](/python/langchain-core/utils/iter/safetee)

## Functions

[function

tee\_peer

An individual iterator of a `.tee`.

This function is a generator that yields items from the shared iterator `iterator`.
It buffers items until the least advanced iterator has yielded them as well. The
buffer is shared with all other peers.](/python/langchain-core/utils/iter/tee_peer)[function

batch\_iterate

Utility batching function.](/python/langchain-core/utils/iter/batch_iterate)

## Classes

[class

NoLock

Dummy lock that provides the proper interface but no protection.](/python/langchain-core/utils/iter/NoLock)[class

Tee

Create `n` separate asynchronous iterators over `iterable`.

This splits a single `iterable` into multiple iterators, each providing the same
items in the same order.

All child iterators may advance separately but share the same items from `iterable`
-- when the most advanced iterator retrieves an item, it is buffered until the least
advanced iterator has yielded it as well. A `tee` works lazily and can handle an
infinite `iterable`, provided that all iterators advance.

```
async def derivative(sensor_data):
    previous, current = a.tee(sensor_data, n=2)
    await a.anext(previous)  # advance one iterator
    return a.map(operator.sub, previous, current)
```

Unlike `itertools.tee`, `.tee` returns a custom type instead of a `tuple`. Like a
tuple, it can be indexed, iterated and unpacked to get the child iterators. In
addition, its `.tee.aclose` method immediately closes all children, and it can be
used in an `async with` context for the same effect.

If `iterable` is an iterator and read elsewhere, `tee` will *not* provide these
items. Also, `tee` must internally buffer each item until the last iterator has
yielded it; if the most and least advanced iterator differ by most data, using a
`list` is more efficient (but not lazy).

If the underlying iterable is concurrency safe (`anext` may be awaited concurrently)
the resulting iterators are concurrency safe as well. Otherwise, the iterators are
safe if there is only ever one single "most advanced" iterator. To enforce
sequential use of `anext`, provide a `lock`

- e.g., an `asyncio.Lock` instance in an `asyncio` application - and access is
  automatically synchronised.](/python/langchain-core/utils/iter/Tee)


