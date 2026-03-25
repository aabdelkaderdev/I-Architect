<!-- Source: https://reference.langchain.com/python/langchain-core/utils/strings -->

Modulev1.2.21 (latest)●Since v0.1

# strings

String utilities.

## Functions

[function

stringify\_value

Stringify a value.](/python/langchain-core/utils/strings/stringify_value)[function

stringify\_dict

Stringify a dictionary.](/python/langchain-core/utils/strings/stringify_dict)[function

comma\_list

Convert an iterable to a comma-separated string.](/python/langchain-core/utils/strings/comma_list)[function

sanitize\_for\_postgres

Sanitize text by removing NUL bytes that are incompatible with PostgreSQL.

PostgreSQL text fields cannot contain `NUL (0x00)` bytes, which can cause
`psycopg.DataError` when inserting documents. This function removes or replaces
such characters to ensure compatibility.](/python/langchain-core/utils/strings/sanitize_for_postgres)


