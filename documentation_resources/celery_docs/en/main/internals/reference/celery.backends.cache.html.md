<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.cache.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.cache.html).

# `celery.backends.cache`

Memcached and in-memory cache result backend.

class celery.backends.cache.CacheBackend(*app*, *expires=None*, *backend=None*, *options=None*, *url=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/cache.html#CacheBackend)
:   Cache result backend.

    as\_uri(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/cache.html#CacheBackend.as_uri)
    :   Return the backend as an URI.

        This properly handles the case of multiple servers.

    property client

    delete(*key*)[[source]](../../_modules/celery/backends/cache.html#CacheBackend.delete)

    expire(*key*, *value*)[[source]](../../_modules/celery/backends/cache.html#CacheBackend.expire)

    get(*key*)[[source]](../../_modules/celery/backends/cache.html#CacheBackend.get)

    implements\_incr = True

    incr(*key*)[[source]](../../_modules/celery/backends/cache.html#CacheBackend.incr)

    mget(*keys*)[[source]](../../_modules/celery/backends/cache.html#CacheBackend.mget)

    servers = None

    set(*key*, *value*)[[source]](../../_modules/celery/backends/cache.html#CacheBackend.set)

    supports\_autoexpire = True
    :   If true the backend must automatically expire results.
        The daily backend\_cleanup periodic task won’t be triggered
        in this case.

    supports\_native\_join = True
    :   If true the backend must implement `get_many()`.