<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.database.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.database.html).

# `celery.backends.database`

SQLAlchemy result store backend.

class celery.backends.database.DatabaseBackend(*dburi=None*, *engine\_options=None*, *url=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/database.html#DatabaseBackend)
:   The database result backend.

    ResultSession(*session\_manager=None*)[[source]](../../_modules/celery/backends/database.html#DatabaseBackend.ResultSession)

    cleanup()[[source]](../../_modules/celery/backends/database.html#DatabaseBackend.cleanup)
    :   Delete expired meta-data.

    exception\_safe\_to\_retry(*exc*)[[source]](../../_modules/celery/backends/database.html#DatabaseBackend.exception_safe_to_retry)
    :   Check if an exception is safe to retry.

        Backends have to overload this method with correct predicates dealing with their exceptions.

        By default no exception is safe to retry, it’s up to backend implementation
        to define which exceptions are safe.

    property extended\_result

    on\_backend\_retryable\_error(*exc*)[[source]](../../_modules/celery/backends/database.html#DatabaseBackend.on_backend_retryable_error)
    :   Hook called before retrying a recoverable backend exception.

    subpolling\_interval = 0.5
    :   Time to sleep between polling each individual item
        in ResultSet.iterate. as opposed to the interval
        argument which is for each pass.

    task\_cls
    :   alias of [`Task`](celery.backends.database.models.html#celery.backends.database.models.Task "celery.backends.database.models.Task")

    task\_result\_exists(*task\_id*)[[source]](../../_modules/celery/backends/database.html#DatabaseBackend.task_result_exists)
    :   Check if a result exists in the database for the given task ID.

        Added in version 5.7.0.

    taskset\_cls
    :   alias of [`TaskSet`](celery.backends.database.models.html#celery.backends.database.models.TaskSet "celery.backends.database.models.TaskSet")