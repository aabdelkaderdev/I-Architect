<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.threads.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.threads.html).

# `celery.utils.threads`

Threading primitives and utilities.

class celery.utils.threads.Local[[source]](../../_modules/celery/utils/threads.html#Local)
:   Local object.

class celery.utils.threads.LocalManager(*locals=None*, *ident\_func=None*)[[source]](../../_modules/celery/utils/threads.html#LocalManager)
:   Local objects cannot manage themselves.

    For that you need a local manager.
    You can pass a local manager multiple locals or add them
    later by appending them to `manager.locals`. Every time the manager
    cleans up, it will clean up all the data left in the locals for this
    context.

    The `ident_func` parameter can be added to override the default ident
    function for the wrapped locals.

    cleanup()[[source]](../../_modules/celery/utils/threads.html#LocalManager.cleanup)
    :   Manually clean up the data in the locals for this context.

        Call this at the end of the request or use `make_middleware()`.

    get\_ident()[[source]](../../_modules/celery/utils/threads.html#LocalManager.get_ident)
    :   Return context identifier.

        This is the identifier the local objects use internally
        for this context. You cannot override this method to change the
        behavior but use it to link other context local objects (such as
        SQLAlchemy’s scoped sessions) to the Werkzeug locals.

celery.utils.threads.LocalStack
:   alias of `_LocalStack`

class celery.utils.threads.bgThread(*name=None*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/threads.html#bgThread)
:   Background service thread.

    body()[[source]](../../_modules/celery/utils/threads.html#bgThread.body)

    on\_crash(*msg*, *\*fmt*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/threads.html#bgThread.on_crash)

    run()[[source]](../../_modules/celery/utils/threads.html#bgThread.run)
    :   Method representing the thread’s activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object’s constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

    stop()[[source]](../../_modules/celery/utils/threads.html#bgThread.stop)
    :   Graceful shutdown.

celery.utils.threads.default\_socket\_timeout(*timeout*)[[source]](../../_modules/celery/utils/threads.html#default_socket_timeout)
:   Context temporarily setting the default socket timeout.

celery.utils.threads.get\_ident()
:   getcurrent() -> greenlet

    Returns the current greenlet (i.e. the one which called this function).