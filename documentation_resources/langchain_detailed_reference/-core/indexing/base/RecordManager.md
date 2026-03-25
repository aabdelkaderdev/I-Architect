<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/RecordManager -->

Classv1.2.21 (latest)●Since v0.1

# RecordManager

Abstract base class representing the interface for a record manager.

The record manager abstraction is used by the langchain indexing API.

The record manager keeps track of which documents have been
written into a `VectorStore` and when they were written.

The indexing API computes hashes for each document and stores the hash
together with the write time and the source id in the record manager.

On subsequent indexing runs, the indexing API can check the record manager
to determine which documents have already been indexed and which have not.

This allows the indexing API to avoid re-indexing documents that have
already been indexed, and to only index new documents.

The main benefit of this abstraction is that it works across many vectorstores.
To be supported, a `VectorStore` needs to only support the ability to add and
delete documents by ID. Using the record manager, the indexing API will
be able to delete outdated documents and avoid redundant indexing of documents
that have already been indexed.

The main constraints of this abstraction are:

1. It relies on the time-stamps to determine which documents have been
   indexed and which have not. This means that the time-stamps must be
   monotonically increasing. The timestamp should be the timestamp
   as measured by the server to minimize issues.
2. The record manager is currently implemented separately from the
   vectorstore, which means that the overall system becomes distributed
   and may create issues with consistency. For example, writing to
   record manager succeeds, but corresponding writing to `VectorStore` fails.


```
RecordManager(
    self,
    namespace: str,
)
```

## Bases

`ABC`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `namespace`\* | `str` | The namespace for the record manager. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| namespace | [str](https://docs.python.org/3/library/stdtypes.html#str) |

## Attributes

[attribute

namespace: namespace](/python/langchain-core/indexing/base/RecordManager/namespace)

## Methods

[method

create\_schema

Create the database schema for the record manager.](/python/langchain-core/indexing/base/RecordManager/create_schema)[method

acreate\_schema

Asynchronously create the database schema for the record manager.](/python/langchain-core/indexing/base/RecordManager/acreate_schema)[method

get\_time

Get the current server time as a high resolution timestamp!

It's important to get this from the server to ensure a monotonic clock,
otherwise there may be data loss when cleaning up old documents!](/python/langchain-core/indexing/base/RecordManager/get_time)[method

aget\_time

Asynchronously get the current server time as a high resolution timestamp.

It's important to get this from the server to ensure a monotonic clock,
otherwise there may be data loss when cleaning up old documents!](/python/langchain-core/indexing/base/RecordManager/aget_time)[method

update

Upsert records into the database.](/python/langchain-core/indexing/base/RecordManager/update)[method

aupdate

Asynchronously upsert records into the database.](/python/langchain-core/indexing/base/RecordManager/aupdate)[method

exists

Check if the provided keys exist in the database.](/python/langchain-core/indexing/base/RecordManager/exists)[method

aexists

Asynchronously check if the provided keys exist in the database.](/python/langchain-core/indexing/base/RecordManager/aexists)[method

list\_keys

List records in the database based on the provided filters.](/python/langchain-core/indexing/base/RecordManager/list_keys)[method

alist\_keys

Asynchronously list records in the database based on the provided filters.](/python/langchain-core/indexing/base/RecordManager/alist_keys)[method

delete\_keys

Delete specified records from the database.](/python/langchain-core/indexing/base/RecordManager/delete_keys)[method

adelete\_keys

Asynchronously delete specified records from the database.](/python/langchain-core/indexing/base/RecordManager/adelete_keys)


