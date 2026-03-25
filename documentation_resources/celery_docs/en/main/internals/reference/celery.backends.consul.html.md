<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.consul.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.consul.html).

# celery.backends.consul

Consul result store backend.

- [`ConsulBackend`](#celery.backends.consul.ConsulBackend "celery.backends.consul.ConsulBackend") implements KeyValueStoreBackend to store results
  :   in the key-value store of Consul.

class celery.backends.consul.ConsulBackend(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/consul.html#ConsulBackend)
:   Consul.io K/V store backend for Celery.

    client()[[source]](../../_modules/celery/backends/consul.html#ConsulBackend.client)

    consistency = 'consistent'

    consul = None

    delete(*key*)[[source]](../../_modules/celery/backends/consul.html#ConsulBackend.delete)

    get(*key*)[[source]](../../_modules/celery/backends/consul.html#ConsulBackend.get)

    mget(*keys*)[[source]](../../_modules/celery/backends/consul.html#ConsulBackend.mget)

    path = None

    set(*key*, *value*)[[source]](../../_modules/celery/backends/consul.html#ConsulBackend.set)
    :   Set a key in Consul.

        Before creating the key it will create a session inside Consul
        where it creates a session with a TTL

        The key created afterwards will reference to the session’s ID.

        If the session expires it will remove the key so that results
        can auto expire from the K/V store

    supports\_autoexpire = True
    :   If true the backend must automatically expire results.
        The daily backend\_cleanup periodic task won’t be triggered
        in this case.