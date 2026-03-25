<!-- Source: https://reference.langchain.com/python/langchain-core/utils/aiter -->

Modulev1.2.21 (latest)●Since v0.1

# aiter

Asynchronous iterator utilities.

Adapted from
<https://github.com/maxfischer2781/asyncstdlib/blob/master/asyncstdlib/itertools.py>
MIT License.

## Attributes

[attribute

T](/python/langchain-core/utils/aiter/T)[attribute

atee: Tee](/python/langchain-core/utils/aiter/atee)

## Functions

[function

deprecated

Decorator to mark a function, a class, or a property as deprecated.

When deprecating a classmethod, a staticmethod, or a property, the `@deprecated`
decorator should go *under* `@classmethod` and `@staticmethod` (i.e., `deprecated`
should directly decorate the underlying callable), but *over* `@property`.

When deprecating a class `C` intended to be used as a base class in a multiple
inheritance hierarchy, `C` *must* define an `__init__` method (if `C` instead
inherited its `__init__` from its own base class, then `@deprecated` would mess up
`__init__` inheritance when installing its own (deprecation-emitting) `C.__init__`).

Parameters are the same as for `warn_deprecated`, except that *obj\_type* defaults to
'class' if decorating a class, 'attribute' if decorating a property, and 'function'
otherwise.](/python/langchain-core/_api/deprecation/deprecated)[function

tee\_peer

An individual iterator of a `tee`.

This function is a generator that yields items from the shared iterator
`iterator`. It buffers items until the least advanced iterator has yielded them as
well.

The buffer is shared with all other peers.](/python/langchain-core/utils/aiter/tee_peer)[function

abatch\_iterate

Utility batching function for async iterables.](/python/langchain-core/utils/aiter/abatch_iterate)[deprecatedfunction

py\_anext

Pure-Python implementation of `anext()` for testing purposes.

Closely matches the builtin `anext()` C implementation.

Can be used to compare the built-in implementation of the inner coroutines machinery
to C-implementation of `__anext__()` and `send()` or `throw()` on the returned
generator.](/python/langchain-core/utils/aiter/py_anext)

## Classes

[class

NoLock

Dummy lock that provides the proper interface but no protection.](/python/langchain-core/utils/aiter/NoLock)[class

Tee

Create `n` separate asynchronous iterators over `iterable`.

This splits a single `iterable` into multiple iterators, each providing
the same items in the same order.

All child iterators may advance separately but share the same items from `iterable`
-- when the most advanced iterator retrieves an item, it is buffered until the least
advanced iterator has yielded it as well.

A `tee` works lazily and can handle an infinite `iterable`, provided
that all iterators advance.

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
safe if there is only ever one single "most advanced" iterator.

To enforce sequential use of `anext`, provide a `lock`

- e.g. an `asyncio.Lock` instance in an `asyncio` application - and access is
  automatically synchronised.](/python/langchain-core/utils/aiter/Tee)[class

aclosing

Async context manager to wrap an `AsyncGenerator` that has a `aclose()` method.

Code like this:

```
async with aclosing(<module>.fetch(<arguments>)) as agen:
    <block>
```

...is equivalent to this:

```
agen = <module>.fetch(<arguments>)
try:
    <block>
finally:
    await agen.aclose()
```](/python/langchain-core/utils/aiter/aclosing)


