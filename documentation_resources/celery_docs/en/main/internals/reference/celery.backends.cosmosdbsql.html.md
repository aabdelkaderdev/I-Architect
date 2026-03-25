<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.cosmosdbsql.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.cosmosdbsql.html).

# `celery.backends.cosmosdbsql`

The CosmosDB/SQL backend for Celery (experimental).

class celery.backends.cosmosdbsql.CosmosDBSQLBackend(*url=None*, *database\_name=None*, *collection\_name=None*, *consistency\_level=None*, *max\_retry\_attempts=None*, *max\_retry\_wait\_time=None*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/cosmosdbsql.html#CosmosDBSQLBackend)
:   CosmosDB/SQL backend for Celery.

    delete(*key*)[[source]](../../_modules/celery/backends/cosmosdbsql.html#CosmosDBSQLBackend.delete)
    :   Delete the value at a given key.

        Parameters:
        :   **key** – The key of the value to delete.

    get(*key*)[[source]](../../_modules/celery/backends/cosmosdbsql.html#CosmosDBSQLBackend.get)
    :   Read the value stored at the given key.

        Parameters:
        :   **key** – The key for which to read the value.

    mget(*keys*)[[source]](../../_modules/celery/backends/cosmosdbsql.html#CosmosDBSQLBackend.mget)
    :   Read all the values for the provided keys.

        Parameters:
        :   **keys** – The list of keys to read.

    set(*key*, *value*)[[source]](../../_modules/celery/backends/cosmosdbsql.html#CosmosDBSQLBackend.set)
    :   Store a value for a given key.

        Parameters:
        :   - **key** – The key at which to store the value.
            - **value** – The value to store.