<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.couchdb.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.couchdb.html).

# `celery.backends.couchdb`

CouchDB result store backend.

class celery.backends.couchdb.CouchBackend(*url=None*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/couchdb.html#CouchBackend)
:   CouchDB backend.

    Raises:
    :   [**celery.exceptions.ImproperlyConfigured**](../../reference/celery.exceptions.html#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured") – if module <https://pypi.org/project/pycouchdb/> is not available.

    property connection

    container = 'default'

    delete(*key*)[[source]](../../_modules/celery/backends/couchdb.html#CouchBackend.delete)

    get(*key*)[[source]](../../_modules/celery/backends/couchdb.html#CouchBackend.get)

    host = 'localhost'

    mget(*keys*)[[source]](../../_modules/celery/backends/couchdb.html#CouchBackend.mget)

    password = None

    port = 5984

    scheme = 'http'

    set(*key*, *value*)[[source]](../../_modules/celery/backends/couchdb.html#CouchBackend.set)

    username = None