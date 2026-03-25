<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.contrib.testing.worker.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.testing.worker.html).

# `celery.contrib.testing.worker`

## 

Embedded workers for integration tests.

class celery.contrib.testing.worker.TestWorkController(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController)
:   Worker that can synchronize on being fully started.

    class QueueHandler(*queue*)[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.QueueHandler)
    :   handleError(*record*)[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.QueueHandler.handleError)
        :   Handle errors which occur during an emit() call.

            This method should be called from handlers when an exception is
            encountered during an emit() call. If raiseExceptions is false,
            exceptions get silently ignored. This is what is mostly wanted
            for a logging system - most users will not care about errors in
            the logging system, they are more interested in application errors.
            You could, however, replace this with a custom handler if you wish.
            The record which was being processed is passed in to this method.

        prepare(*record*)[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.QueueHandler.prepare)
        :   Prepare a record for queuing. The object returned by this method is
            enqueued.

            The base implementation formats the record to merge the message and
            arguments, and removes unpickleable items from the record in-place.
            Specifically, it overwrites the record’s msg and
            message attributes with the merged message (obtained by
            calling the handler’s format method), and sets the args,
            exc\_info and exc\_text attributes to None.

            You might want to override this method if you want to convert
            the record to a dict or JSON string, or send a modified copy
            of the record while leaving the original intact.

    ensure\_started() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.ensure_started)
    :   Wait for worker to be fully up and running.

        Warning

        Worker must be started within a thread for this to work,
        or it will block forever.

    logger\_queue = None

    on\_consumer\_ready(*consumer: [Consumer](celery.worker.consumer.consumer.html#celery.worker.consumer.consumer.Consumer "celery.worker.consumer.consumer.Consumer")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.on_consumer_ready)
    :   Callback called when the Consumer blueprint is fully started.

    start()[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.start)

celery.contrib.testing.worker.setup\_app\_for\_worker(*app: [Celery](celery.html#celery.Celery "celery.app.base.Celery")*, *loglevel: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*, *logfile: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/worker.html#setup_app_for_worker)
:   Setup the app to be used for starting an embedded worker.

celery.contrib.testing.worker.start\_worker(*app: [Celery](celery.html#celery.Celery "celery.app.base.Celery")*, *concurrency: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 1*, *pool: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'solo'*, *loglevel: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 'error'*, *logfile: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = None*, *perform\_ping\_check: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*, *ping\_task\_timeout: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") = 10.0*, *shutdown\_timeout: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") = 10.0*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/worker.html#start_worker)
:   Start embedded worker.

    Yields:
    :   *celery.app.worker.Worker* – worker instance.