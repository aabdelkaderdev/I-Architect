<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/DeleteResponse -->

Classv1.2.21 (latest)●Since v0.2

# DeleteResponse

A generic response for delete operation.

The fields in this response are optional and whether the `VectorStore`
returns them or not is up to the implementation.


```
DeleteResponse()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| num\_deleted | [int](https://docs.python.org/3/library/functions.html#int) |
| succeeded | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[str](https://docs.python.org/3/library/stdtypes.html#str)] |
| failed | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[str](https://docs.python.org/3/library/stdtypes.html#str)] |
| num\_failed | [int](https://docs.python.org/3/library/functions.html#int) |

## Attributes

[attribute

num\_deleted: int

The number of items that were successfully deleted.

If returned, this should only include *actual* deletions.

If the ID did not exist to begin with,
it should not be included in this count.](/python/langchain-core/indexing/base/DeleteResponse/num_deleted)[attribute

succeeded: Sequence[str]

The IDs that were successfully deleted.

If returned, this should only include *actual* deletions.

If the ID did not exist to begin with,
it should not be included in this list.](/python/langchain-core/indexing/base/DeleteResponse/succeeded)[attribute

failed: Sequence[str]

The IDs that failed to be deleted.

Warning

Deleting an ID that does not exist is **NOT** considered a failure.](/python/langchain-core/indexing/base/DeleteResponse/failed)[attribute

num\_failed: int

The number of items that failed to be deleted.](/python/langchain-core/indexing/base/DeleteResponse/num_failed)


