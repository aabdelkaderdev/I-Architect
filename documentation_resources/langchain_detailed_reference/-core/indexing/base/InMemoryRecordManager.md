<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/InMemoryRecordManager -->

Classv1.2.21 (latest)●Since v0.2

# InMemoryRecordManager

An in-memory record manager for testing purposes.


```
InMemoryRecordManager(
    self,
    namespace: str,
)
```

## Bases

`RecordManager`

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

records: dict[str, \_Record]](/python/langchain-core/indexing/base/InMemoryRecordManager/records)[attribute

namespace: namespace](/python/langchain-core/indexing/base/InMemoryRecordManager/namespace)

## Methods

[method

create\_schema

In-memory schema creation is simply ensuring the structure is initialized.](/python/langchain-core/indexing/base/InMemoryRecordManager/create_schema)[method

acreate\_schema

In-memory schema creation is simply ensuring the structure is initialized.](/python/langchain-core/indexing/base/InMemoryRecordManager/acreate_schema)[method

get\_time](/python/langchain-core/indexing/base/InMemoryRecordManager/get_time)[method

aget\_time](/python/langchain-core/indexing/base/InMemoryRecordManager/aget_time)[method

update

Upsert records into the database.](/python/langchain-core/indexing/base/InMemoryRecordManager/update)[method

aupdate

Async upsert records into the database.](/python/langchain-core/indexing/base/InMemoryRecordManager/aupdate)[method

exists

Check if the provided keys exist in the database.](/python/langchain-core/indexing/base/InMemoryRecordManager/exists)[method

aexists

Async check if the provided keys exist in the database.](/python/langchain-core/indexing/base/InMemoryRecordManager/aexists)[method

list\_keys

List records in the database based on the provided filters.](/python/langchain-core/indexing/base/InMemoryRecordManager/list_keys)[method

alist\_keys

Async list records in the database based on the provided filters.](/python/langchain-core/indexing/base/InMemoryRecordManager/alist_keys)[method

delete\_keys

Delete specified records from the database.](/python/langchain-core/indexing/base/InMemoryRecordManager/delete_keys)[method

adelete\_keys

Async delete specified records from the database.](/python/langchain-core/indexing/base/InMemoryRecordManager/adelete_keys)


