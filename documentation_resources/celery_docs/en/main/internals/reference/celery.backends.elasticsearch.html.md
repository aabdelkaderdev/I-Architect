<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.elasticsearch.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.elasticsearch.html).

# `celery.backends.elasticsearch`

Elasticsearch result store backend.

class celery.backends.elasticsearch.ElasticsearchBackend(*url=None*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend)
:   Elasticsearch Backend.

    Raises:
    :   [**celery.exceptions.ImproperlyConfigured**](../../reference/celery.exceptions.html#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured") – if module <https://pypi.org/project/elasticsearch/> is not available.

    decode(*payload*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.decode)

    delete(*key*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.delete)

    doc\_type = None

    encode(*data*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.encode)

    es\_max\_retries = 3

    es\_retry\_on\_timeout = False

    es\_timeout = 10

    exception\_safe\_to\_retry(*exc*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.exception_safe_to_retry)
    :   Check if an exception is safe to retry.

        Backends have to overload this method with correct predicates dealing with their exceptions.

        By default no exception is safe to retry, it’s up to backend implementation
        to define which exceptions are safe.

    get(*key*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.get)

    host = 'localhost'

    index = 'celery'

    mget(*keys*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.mget)

    password = None

    port = 9200

    scheme = 'http'

    property server

    set(*key*, *value*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.set)

    username = None