<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/entity/SQLiteEntityStore -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# SQLiteEntityStore

SQLite-backed Entity store with safe query construction.


```
SQLiteEntityStore(
  self,
  session_id: str = 'default',
  db_file: str = 'entities.db',
  table_name: str = 'memory_store',
  *args: Any = (),
  **kwargs: Any = {}
)
```

## Bases

`BaseEntityStore`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `session_id` | `str` | Default:`'default'`  Unique identifier for the session. |
| `db_file` | `str` | Default:`'entities.db'`  Path to the SQLite database file. |
| `table_name` | `str` | Default:`'memory_store'`  Name of the table to store entities. |
| `*args` | `Any` | Default:`()`  Additional positional arguments. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| session\_id | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| db\_file | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| table\_name | [str](https://docs.python.org/3/library/stdtypes.html#str) |

## Attributes

[attribute

session\_id: str](/python/langchain-classic/memory/entity/SQLiteEntityStore/session_id)[attribute

table\_name: str](/python/langchain-classic/memory/entity/SQLiteEntityStore/table_name)[attribute

conn: Any](/python/langchain-classic/memory/entity/SQLiteEntityStore/conn)[attribute

model\_config](/python/langchain-classic/memory/entity/SQLiteEntityStore/model_config)[attribute

full\_table\_name: str

Returns the full table name with session ID.](/python/langchain-classic/memory/entity/SQLiteEntityStore/full_table_name)

## Methods

[method

get

Retrieves a value, safely quoting the table name.](/python/langchain-classic/memory/entity/SQLiteEntityStore/get)[method

set

Inserts or replaces a value, safely quoting the table name.](/python/langchain-classic/memory/entity/SQLiteEntityStore/set)[method

delete

Deletes a key-value pair, safely quoting the table name.](/python/langchain-classic/memory/entity/SQLiteEntityStore/delete)[method

exists

Checks for the existence of a key, safely quoting the table name.](/python/langchain-classic/memory/entity/SQLiteEntityStore/exists)[method

clear](/python/langchain-classic/memory/entity/SQLiteEntityStore/clear)


