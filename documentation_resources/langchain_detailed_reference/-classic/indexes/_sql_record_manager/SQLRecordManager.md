<!-- Source: https://reference.langchain.com/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager -->

Classv1.2.13 (latest)●Since v1.0

# SQLRecordManager


```
SQLRecordManager(
  self,
  namespace: str,
  *,
  engine: Engine | AsyncEngine | None = None,
```

## Bases

`RecordManager`

## Constructors

## Attributes

## Methods

## Inherited from[RecordManager](/python/langchain-core/indexing/base/RecordManager)(langchain\_core)

### Attributes

[Anamespace](/python/langchain-core/indexing/base/RecordManager/namespace)



db\_url

:

None

|

[str](https://docs.python.org/3/library/stdtypes.html#str)

|

[URL](/python/langchain-google-genai/_image_utils/Route/URL)

=

None

,

engine\_kwargs

:

[dict](https://docs.python.org/3/library/stdtypes.html#dict)

[

[str](https://docs.python.org/3/library/stdtypes.html#str)

,

Any

]

|

None

=

None

,

async\_mode

:

[bool](https://docs.python.org/3/library/functions.html#bool)

=

False

)

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `namespace`\* | `str` | The namespace associated with this record manager. |
| `engine` | `Engine | AsyncEngine | None` | Default:`None`  An already existing SQL Alchemy engine. |
| `db_url` | `None | str | URL` | Default:`None`  A database connection string used to create an SQL Alchemy engine. |
| `engine_kwargs` | `dict[str, Any] | None` | Default:`None` |
| `async_mode` | `bool` | Default:`False` |

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| namespace | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| engine | Engine | AsyncEngine | None |
| db\_url | None | [str](https://docs.python.org/3/library/stdtypes.html#str) | [URL](/python/langchain-google-genai/_image_utils/Route/URL) |
| engine\_kwargs | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None |
| async\_mode | [bool](https://docs.python.org/3/library/functions.html#bool) |

[attribute

engine: \_engine](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/engine)

[attribute

dialect](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/dialect)

[attribute

session\_factory: \_session\_factory](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/session_factory)

[method

create\_schema

Create the database schema.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/create_schema)

[method

acreate\_schema

Create the database schema.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/acreate_schema)

[method

get\_time

Get the current server time as a timestamp.

Please note it's critical that time is obtained from the server since
we want a monotonic clock.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/get_time)

[method

aget\_time

Get the current server time as a timestamp.

Please note it's critical that time is obtained from the server since
we want a monotonic clock.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/aget_time)

[method

update

Upsert records into the SQLite database.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/update)

[method

aupdate

Upsert records into the SQLite database.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/aupdate)

[method

exists

Check if the given keys exist in the SQLite database.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/exists)

[method

aexists

Check if the given keys exist in the SQLite database.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/aexists)

[method

list\_keys

List records in the SQLite database based on the provided date range.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/list_keys)

[method

alist\_keys

List records in the SQLite database based on the provided date range.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/alist_keys)

[method

delete\_keys

Delete records from the SQLite database.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/delete_keys)

[method

adelete\_keys

Delete records from the SQLite database.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/adelete_keys)

A SQL Alchemy based implementation of the record manager.

Additional keyword arguments to be passed when creating the
engine.

Whether to create an async engine. Driver should support async
operations. It only applies if `db_url` is provided.