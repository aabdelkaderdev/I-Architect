<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.arangodb.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.arangodb.html).

# `celery.backends.arangodb`

ArangoDb result store backend.

class celery.backends.arangodb.ArangoDbBackend(*url=None*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/arangodb.html#ArangoDbBackend)
:   ArangoDb backend.

    Sample url
    “arangodb://username:password@host:port/database/collection”
    *arangodb\_backend\_settings* is where the settings are present
    (in the app.conf)
    Settings should contain the host, port, username, password, database name,
    collection name else the default will be chosen.
    Default database name and collection name is celery.

    Raises:
    :   **celery.exceptions.ImproperlyConfigured:** – if module <https://pypi.org/project/pyArango/> is not available.

    cleanup()[[source]](../../_modules/celery/backends/arangodb.html#ArangoDbBackend.cleanup)
    :   Backend cleanup.

    collection = 'celery'

    property connection
    :   Connect to the arangodb server.

    database = 'celery'

    property db
    :   Database Object to the given database.

    delete(*key*)[[source]](../../_modules/celery/backends/arangodb.html#ArangoDbBackend.delete)

    property expires\_delta

    get(*key*)[[source]](../../_modules/celery/backends/arangodb.html#ArangoDbBackend.get)

    host = '127.0.0.1'

    http\_protocol = 'http'

    key\_t
    :   alias of [`str`](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

    mget(*keys*)[[source]](../../_modules/celery/backends/arangodb.html#ArangoDbBackend.mget)

    password = None

    port = '8529'

    set(*key*, *value*)[[source]](../../_modules/celery/backends/arangodb.html#ArangoDbBackend.set)

    username = None

    verify = False