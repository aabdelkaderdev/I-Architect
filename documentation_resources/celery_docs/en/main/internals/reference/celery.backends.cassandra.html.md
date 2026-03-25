<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.cassandra.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.cassandra.html).

# `celery.backends.cassandra`

Apache Cassandra result store backend using the DataStax driver.

class celery.backends.cassandra.CassandraBackend(*servers=None*, *keyspace=None*, *table=None*, *entry\_ttl=None*, *port=None*, *bundle\_path=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/cassandra.html#CassandraBackend)
:   Cassandra/AstraDB backend utilizing DataStax driver.

    Raises:
    :   [**celery.exceptions.ImproperlyConfigured**](../../reference/celery.exceptions.html#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured") – if module <https://pypi.org/project/cassandra-driver/> is not available,
        or not-exactly-one of the [`cassandra_servers`](../../userguide/configuration.html#std-setting-cassandra_servers) and
        the [`cassandra_secure_bundle_path`](../../userguide/configuration.html#std-setting-cassandra_secure_bundle_path) settings is set.

    as\_uri(*include\_password=True*)[[source]](../../_modules/celery/backends/cassandra.html#CassandraBackend.as_uri)
    :   Return the backend as an URI, sanitizing the password or not.

    bundle\_path = None
    :   Location of the secure connect bundle zipfile (absolute path).

    servers = None
    :   `hostname`.

        Type:
        :   List of Cassandra servers with format

    supports\_autoexpire = True
    :   If true the backend must automatically expire results.
        The daily backend\_cleanup periodic task won’t be triggered
        in this case.