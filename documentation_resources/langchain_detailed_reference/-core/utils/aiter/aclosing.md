<!-- Source: https://reference.langchain.com/python/langchain-core/utils/aiter/aclosing -->

Classv1.2.21 (latest)●Since v0.2

# aclosing

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
```


```
aclosing(
    self,
    thing: AsyncGenerator[Any, Any] | AsyncIterator[Any],
)
```

## Bases

`AbstractAsyncContextManager`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `thing`\* | `AsyncGenerator[Any, Any] | AsyncIterator[Any]` | The resource to wrap. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| thing | [AsyncGenerator](https://docs.python.org/3/library/typing.html#typing.AsyncGenerator)[[Any](https://docs.python.org/3/library/typing.html#typing.Any), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | [AsyncIterator](https://docs.python.org/3/library/typing.html#typing.AsyncIterator)[[Any](https://docs.python.org/3/library/typing.html#typing.Any)] |

## Attributes

[attribute

thing: thing](/python/langchain-core/utils/aiter/aclosing/thing)


