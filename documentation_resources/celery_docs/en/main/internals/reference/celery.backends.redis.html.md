<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.redis.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.redis.html).

# `celery.backends.redis`

Redis result store backend.

class celery.backends.redis.RedisBackend(*host=None*, *port=None*, *db=None*, *password=None*, *max\_connections=None*, *url=None*, *connection\_pool=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend)
:   Redis task result store.

    It makes use of the following commands:
    GET, MGET, DEL, INCRBY, EXPIRE, SET, SETEX

    property ConnectionPool

    class ResultConsumer(*\*args*, *\*\*kwargs*)
    :   cancel\_for(*task\_id*)

        consume\_from(*task\_id*)

        drain\_events(*timeout=None*)

        on\_after\_fork()

        on\_state\_change(*meta*, *message*)

        on\_wait\_for\_pending(*result*, *\*\*kwargs*)

        start(*initial\_task\_id*, *\*\*kwargs*)

        stop()

    add\_to\_chord(*group\_id*, *result*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.add_to_chord)

    apply\_chord(*header\_result\_args*, *body*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.apply_chord)

    property client

    connection\_class\_ssl
    :   alias of `SSLConnection`

    delete(*key*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.delete)

    ensure(*fun*, *args*, *\*\*policy*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.ensure)

    exception\_safe\_to\_retry(*exc*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.exception_safe_to_retry)
    :   Check if an exception is safe to retry.

        Backends have to overload this method with correct predicates dealing with their exceptions.

        By default no exception is safe to retry, it’s up to backend implementation
        to define which exceptions are safe.

    expire(*key*, *value*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.expire)

    forget(*task\_id*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.forget)

    get(*key*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.get)

    incr(*key*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.incr)

    max\_connections = None
    :   Maximum number of connections in the pool.

    mget(*keys*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.mget)

    on\_chord\_part\_return(*request*, *state*, *result*, *propagate=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.on_chord_part_return)

    on\_connection\_error(*max\_retries*, *exc*, *intervals*, *retries*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.on_connection_error)

    on\_task\_call(*producer*, *task\_id*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.on_task_call)

    redis = <module 'redis' from '/home/docs/checkouts/readthedocs.org/user\_builds/celery/envs/main/lib/python3.11/site-packages/redis/\_\_init\_\_.py'>
    :   <https://pypi.org/project/redis/> client module.

    property retry\_policy
    :   dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object’s

        > (key, value) pairs

        dict(iterable) -> new dictionary initialized as if via:
        :   d = {}
            for k, v in iterable:

            > d[k] = v

        dict([\*\*](#id1)kwargs) -> new dictionary initialized with the name=value pairs
        :   in the keyword argument list. For example: dict(one=1, two=2)

    set(*key*, *value*, *\*\*retry\_policy*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.set)

    set\_chord\_size(*group\_id*, *chord\_size*)[[source]](../../_modules/celery/backends/redis.html#RedisBackend.set_chord_size)

    supports\_autoexpire = True
    :   If true the backend must automatically expire results.
        The daily backend\_cleanup periodic task won’t be triggered
        in this case.

    supports\_native\_join = True
    :   If true the backend must implement `get_many()`.

class celery.backends.redis.SentinelBackend(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/redis.html#SentinelBackend)
:   Redis sentinel task result store.

    as\_uri(*include\_password=False*)[[source]](../../_modules/celery/backends/redis.html#SentinelBackend.as_uri)
    :   Return the server addresses as URIs, sanitizing the password or not.

    connection\_class\_ssl
    :   alias of `SentinelManagedSSLConnection`

    sentinel = <module 'redis.sentinel' from '/home/docs/checkouts/readthedocs.org/user\_builds/celery/envs/main/lib/python3.11/site-packages/redis/sentinel.py'>