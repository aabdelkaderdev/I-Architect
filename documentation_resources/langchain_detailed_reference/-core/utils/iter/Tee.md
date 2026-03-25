<!-- Source: https://reference.langchain.com/python/langchain-core/utils/iter/Tee -->

Classv1.2.21 (latest)●Since v0.1

# Tee

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
  automatically synchronised.


```
Tee(
  self,
  iterable: Iterator[T],
  n: int = 2,
  *,
  lock: AbstractContextManager[Any] | None = None
)
```

## Bases

`Generic[T]`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `iterable`\* | `Iterator[T]` | The iterable to split. |
| `n` | `int` | Default:`2`  The number of iterators to create. |
| `lock` | `AbstractContextManager[Any] | None` | Default:`None`  The lock to synchronise access to the shared buffers. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| iterable | [Iterator](https://docs.python.org/3/library/typing.html#typing.Iterator)[[T](/python/langchain-core/runnables/retry/T)] |
| n | [int](https://docs.python.org/3/library/functions.html#int) |
| lock | [AbstractContextManager](https://docs.python.org/3/library/contextlib.html#contextlib.AbstractContextManager)[[Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None |

## Methods

[method

close

Close all child iterators.](/python/langchain-core/utils/iter/Tee/close)


