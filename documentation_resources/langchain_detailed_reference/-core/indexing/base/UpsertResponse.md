<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/UpsertResponse -->

Classv1.2.21 (latest)●Since v0.2

# UpsertResponse

A generic response for upsert operations.

The upsert response will be used by abstractions that implement an upsert
operation for content that can be upserted by ID.

Upsert APIs that accept inputs with IDs and generate IDs internally
will return a response that includes the IDs that succeeded and the IDs
that failed.

If there are no failures, the failed list will be empty, and the order
of the IDs in the succeeded list will match the order of the input documents.

If there are failures, the response becomes ill defined, and a user of the API
cannot determine which generated ID corresponds to which input document.

It is recommended for users explicitly attach the IDs to the items being
indexed to avoid this issue.


```
UpsertResponse()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| succeeded | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] |
| failed | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] |

## Attributes

[attribute

succeeded: list[str]

The IDs that were successfully indexed.](/python/langchain-core/indexing/base/UpsertResponse/succeeded)[attribute

failed: list[str]

The IDs that failed to index.](/python/langchain-core/indexing/base/UpsertResponse/failed)


