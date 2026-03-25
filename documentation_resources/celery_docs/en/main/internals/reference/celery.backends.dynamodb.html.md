<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.dynamodb.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.dynamodb.html).

# `celery.backends.dynamodb`

AWS DynamoDB result store backend.

class celery.backends.dynamodb.DynamoDBBackend(*url=None*, *table\_name=None*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/dynamodb.html#DynamoDBBackend)
:   AWS DynamoDB result backend.

    Raises:
    :   [**celery.exceptions.ImproperlyConfigured**](../../reference/celery.exceptions.html#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured") – if module <https://pypi.org/project/boto3/> is not available.

    aws\_region = None
    :   AWS region (default)

    property client

    delete(*key*)[[source]](../../_modules/celery/backends/dynamodb.html#DynamoDBBackend.delete)

    endpoint\_url = None
    :   The endpoint URL that is passed to boto3 (local DynamoDB) (default)

    get(*key*)[[source]](../../_modules/celery/backends/dynamodb.html#DynamoDBBackend.get)

    implements\_incr = True

    incr(*key: [bytes](https://docs.python.org/dev/library/stdtypes.html#bytes "(in Python v3.15)")*) → [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")[[source]](../../_modules/celery/backends/dynamodb.html#DynamoDBBackend.incr)
    :   Atomically increase the chord\_count and return the new count

    mget(*keys*)[[source]](../../_modules/celery/backends/dynamodb.html#DynamoDBBackend.mget)

    read\_capacity\_units = 1
    :   Read Provisioned Throughput (default)

    set(*key*, *value*)[[source]](../../_modules/celery/backends/dynamodb.html#DynamoDBBackend.set)

    supports\_autoexpire = True
    :   If true the backend must automatically expire results.
        The daily backend\_cleanup periodic task won’t be triggered
        in this case.

    table\_name = 'celery'
    :   default DynamoDB table name (default)

    time\_to\_live\_seconds = None
    :   Item time-to-live in seconds (default)

    write\_capacity\_units = 1
    :   Write Provisioned Throughput (default)