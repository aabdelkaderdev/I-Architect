<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/sql_database/query -->

Modulev1.2.13 (latest)●Since v1.0

# query

## Attributes

[attribute

PROMPT](/python/langchain-classic/chains/sql_database/prompt/PROMPT)[attribute

SQL\_PROMPTS: dict](/python/langchain-classic/chains/sql_database/prompt/SQL_PROMPTS)

## Functions

[function

create\_sql\_query\_chain

Create a chain that generates SQL queries.

*Security Note*: This chain generates SQL queries for the given database.

```
The SQLDatabase class provides a get_table_info method that can be used
to get column information as well as sample data from the table.

To mitigate risk of leaking sensitive data, limit permissions
to read and scope to the tables that are needed.

Optionally, use the SQLInputWithTables input type to specify which tables
are allowed to be accessed.

Control access to who can submit requests to this chain.

See https://docs.langchain.com/oss/python/security-policy for more information.
```](/python/langchain-classic/chains/sql_database/query/create_sql_query_chain)

## Classes

[class

SQLInput

Input for a SQL Chain.](/python/langchain-classic/chains/sql_database/query/SQLInput)[class

SQLInputWithTables

Input for a SQL Chain.](/python/langchain-classic/chains/sql_database/query/SQLInputWithTables)


