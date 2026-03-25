<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.base.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.base.html).

# `celery.backends.base`

Result backend base classes.

- [`BaseBackend`](#celery.backends.base.BaseBackend "celery.backends.base.BaseBackend") defines the interface.
- [`KeyValueStoreBackend`](#celery.backends.base.KeyValueStoreBackend "celery.backends.base.KeyValueStoreBackend") is a common base class
  :   using K/V semantics like \_get and \_put.

class celery.backends.base.BaseBackend(*app*, *serializer=None*, *max\_cached\_results=None*, *accept=None*, *expires=None*, *expires\_type=None*, *url=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/base.html#BaseBackend)
:   Base (synchronous) result backend.

class celery.backends.base.DisabledBackend(*app*, *serializer=None*, *max\_cached\_results=None*, *accept=None*, *expires=None*, *expires\_type=None*, *url=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/base.html#DisabledBackend)
:   Dummy result backend.

    as\_uri(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/base.html#DisabledBackend.as_uri)
    :   Return the backend as an URI, sanitizing the password or not.

    ensure\_chords\_allowed()[[source]](../../_modules/celery/backends/base.html#DisabledBackend.ensure_chords_allowed)

    get\_many(*\*args*, *\*\*kwargs*)

    get\_result(*\*args*, *\*\*kwargs*)
    :   Get the result of a task.

    get\_state(*\*args*, *\*\*kwargs*)
    :   Get the state of a task.

    get\_status(*\*args*, *\*\*kwargs*)
    :   Get the state of a task.

    get\_task\_meta\_for(*\*args*, *\*\*kwargs*)

    get\_traceback(*\*args*, *\*\*kwargs*)
    :   Get the traceback for a failed task.

    store\_result(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/base.html#DisabledBackend.store_result)
    :   Update task state and result.

        if always\_retry\_backend\_operation is activated, in the event of a recoverable exception,
        then retry operation with an exponential backoff until a limit has been reached.

    wait\_for(*\*args*, *\*\*kwargs*)
    :   Wait for task and return its result.

        If the task raises an exception, this exception
        will be re-raised by [`wait_for()`](#celery.backends.base.DisabledBackend.wait_for "celery.backends.base.DisabledBackend.wait_for").

        Raises:
        :   [**celery.exceptions.TimeoutError**](../../reference/celery.exceptions.html#celery.exceptions.TimeoutError "celery.exceptions.TimeoutError") – If timeout is not `None`, and the operation
            takes longer than timeout seconds.

class celery.backends.base.KeyValueStoreBackend(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/base.html#KeyValueStoreBackend)
:   Result backend base class for key/value stores.