<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.couchbase.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.couchbase.html).

# `celery.backends.couchbase`

Couchbase result store backend.

class celery.backends.couchbase.CouchbaseBackend(*url=None*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/couchbase.html#CouchbaseBackend)
:   Couchbase backend.

    Raises:
    :   [**celery.exceptions.ImproperlyConfigured**](../../reference/celery.exceptions.html#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured") – if module <https://pypi.org/project/couchbase/> is not available.

    bucket = 'default'

    property connection

    delete(*key*)[[source]](../../_modules/celery/backends/couchbase.html#CouchbaseBackend.delete)

    get(*key*)[[source]](../../_modules/celery/backends/couchbase.html#CouchbaseBackend.get)

    host = 'localhost'

    key\_t
    :   alias of [`str`](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

    mget(*keys*)[[source]](../../_modules/celery/backends/couchbase.html#CouchbaseBackend.mget)

    password = None

    port = 8091

    quiet = False

    set(*key*, *value*)[[source]](../../_modules/celery/backends/couchbase.html#CouchbaseBackend.set)

    supports\_autoexpire = True
    :   If true the backend must automatically expire results.
        The daily backend\_cleanup periodic task won’t be triggered
        in this case.

    timeout = 2.5

    username = None