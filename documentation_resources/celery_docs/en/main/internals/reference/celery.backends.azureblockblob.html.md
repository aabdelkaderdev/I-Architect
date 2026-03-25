<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.azureblockblob.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.azureblockblob.html).

# `celery.backends.azureblockblob`

The Azure Storage Block Blob backend for Celery.

class celery.backends.azureblockblob.AzureBlockBlobBackend(*url=None*, *container\_name=None*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/azureblockblob.html#AzureBlockBlobBackend)
:   Azure Storage Block Blob backend for Celery.

    as\_uri(*include\_password=False*)[[source]](../../_modules/celery/backends/azureblockblob.html#AzureBlockBlobBackend.as_uri)
    :   Return the backend as an URI, sanitizing the password or not.

    delete(*key*)[[source]](../../_modules/celery/backends/azureblockblob.html#AzureBlockBlobBackend.delete)
    :   Delete the value at a given key.

        Parameters:
        :   **key** – The key of the value to delete.

    get(*key*)[[source]](../../_modules/celery/backends/azureblockblob.html#AzureBlockBlobBackend.get)
    :   Read the value stored at the given key.

        Parameters:
        :   **key** – The key for which to read the value.

    mget(*keys*)[[source]](../../_modules/celery/backends/azureblockblob.html#AzureBlockBlobBackend.mget)
    :   Read all the values for the provided keys.

        Parameters:
        :   **keys** – The list of keys to read.

    set(*key*, *value*)[[source]](../../_modules/celery/backends/azureblockblob.html#AzureBlockBlobBackend.set)
    :   Store a value for a given key.

        Parameters:
        :   - **key** – The key at which to store the value.
            - **value** – The value to store.