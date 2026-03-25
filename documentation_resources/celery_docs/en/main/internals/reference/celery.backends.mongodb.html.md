<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.mongodb.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.mongodb.html).

# `celery.backends.mongodb`

MongoDB result store backend.

class celery.backends.mongodb.MongoBackend(*app=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/mongodb.html#MongoBackend)
:   MongoDB result backend.

    Raises:
    :   [**celery.exceptions.ImproperlyConfigured**](../../reference/celery.exceptions.html#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured") – if module <https://pypi.org/project/pymongo/> is not available.

    as\_uri(*include\_password=False*)[[source]](../../_modules/celery/backends/mongodb.html#MongoBackend.as_uri)
    :   Return the backend as an URI.

        Parameters:
        :   **include\_password** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Password censored if disabled.

    cleanup()[[source]](../../_modules/celery/backends/mongodb.html#MongoBackend.cleanup)
    :   Delete expired meta-data.

    property collection
    :   Get the meta-data task collection.

    property database
    :   Get database from MongoDB connection.

        performs authentication if necessary.

    database\_name = 'celery'

    decode(*data*)[[source]](../../_modules/celery/backends/mongodb.html#MongoBackend.decode)

    encode(*data*)[[source]](../../_modules/celery/backends/mongodb.html#MongoBackend.encode)

    property expires\_delta

    property group\_collection
    :   Get the meta-data task collection.

    groupmeta\_collection = 'celery\_groupmeta'

    host = 'localhost'

    max\_pool\_size = 10

    mongo\_host = None

    options = None

    password = None

    port = 27017

    supports\_autoexpire = False
    :   If true the backend must automatically expire results.
        The daily backend\_cleanup periodic task won’t be triggered
        in this case.

    task\_result\_exists(*task\_id*)[[source]](../../_modules/celery/backends/mongodb.html#MongoBackend.task_result_exists)
    :   Check if a result exists in MongoDB for the given task ID.

        Added in version 5.7.0.

    taskmeta\_collection = 'celery\_taskmeta'

    user = None