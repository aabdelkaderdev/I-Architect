<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.base.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.base.html).

# `celery.concurrency.base`

Base Execution Pool.

class celery.concurrency.base.BasePool(*limit=None*, *putlocks=True*, *forking\_enable=True*, *callbacks\_propagate=()*, *app=None*, *\*\*options*)[[source]](../../_modules/celery/concurrency/base.html#BasePool)
:   Task pool.

    CLOSE = 2

    RUN = 1

    TERMINATE = 3

    class Timer(*schedule: [Timer](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.asynchronous.timer.html#kombu.asynchronous.timer.Timer "(in Kombu v5.6)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *on\_error: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")[[[Exception](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)")], [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *on\_tick: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")[[[float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")], [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *on\_start: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")[[[Timer](celery.utils.timer2.html#celery.utils.timer2.Timer "celery.utils.timer2.Timer")], [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *max\_interval: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)
    :   Timer thread.

        Note

        This is only used for transports not supporting AsyncIO.

        class Entry(*fun*, *args=None*, *kwargs=None*)
        :   Schedule Entry.

            args

            cancel()

            canceled

            property cancelled

            fun

            kwargs

            tref

        Schedule
        :   alias of [`Timer`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.asynchronous.timer.html#kombu.asynchronous.timer.Timer "(in Kombu v5.6)")

        call\_after(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Entry](celery.utils.timer2.html#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")

        call\_at(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Entry](celery.utils.timer2.html#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")

        call\_repeatedly(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Entry](celery.utils.timer2.html#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")

        cancel(*tref: [Entry](celery.utils.timer2.html#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")

        clear() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")

        empty() → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")

        ensure\_started() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")

        enter(*entry: [Entry](celery.utils.timer2.html#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")*, *eta: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")*, *priority: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [Entry](celery.utils.timer2.html#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")

        enter\_after(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Entry](celery.utils.timer2.html#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")

        exit\_after(*secs: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")*, *priority: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 10*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")

        next() → [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")

        on\_tick: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")[[[float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")], [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None

        property queue: [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")

        run() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
        :   Method representing the thread’s activity.

            You may override this method in a subclass. The standard run() method
            invokes the callable object passed to the object’s constructor as the
            target argument, if any, with sequential and keyword arguments taken
            from the args and kwargs arguments, respectively.

        running: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False

        stop() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")

    property active

    apply\_async(*target*, *args=None*, *kwargs=None*, *\*\*options*)[[source]](../../_modules/celery/concurrency/base.html#BasePool.apply_async)
    :   Equivalent of the `apply()` built-in function.

        Callbacks should optimally return as soon as possible since
        otherwise the thread which handles the result will get blocked.

    body\_can\_be\_buffer = False

    close()[[source]](../../_modules/celery/concurrency/base.html#BasePool.close)

    did\_start\_ok()[[source]](../../_modules/celery/concurrency/base.html#BasePool.did_start_ok)

    flush()[[source]](../../_modules/celery/concurrency/base.html#BasePool.flush)

    property info

    is\_green = False
    :   set to true if pool uses greenlets.

    maintain\_pool(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/concurrency/base.html#BasePool.maintain_pool)

    property num\_processes

    on\_apply(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/concurrency/base.html#BasePool.on_apply)

    on\_close()[[source]](../../_modules/celery/concurrency/base.html#BasePool.on_close)

    on\_hard\_timeout(*job*)[[source]](../../_modules/celery/concurrency/base.html#BasePool.on_hard_timeout)

    on\_soft\_timeout(*job*)[[source]](../../_modules/celery/concurrency/base.html#BasePool.on_soft_timeout)

    on\_start()[[source]](../../_modules/celery/concurrency/base.html#BasePool.on_start)

    on\_stop()[[source]](../../_modules/celery/concurrency/base.html#BasePool.on_stop)

    on\_terminate()[[source]](../../_modules/celery/concurrency/base.html#BasePool.on_terminate)

    register\_with\_event\_loop(*loop*)[[source]](../../_modules/celery/concurrency/base.html#BasePool.register_with_event_loop)

    restart()[[source]](../../_modules/celery/concurrency/base.html#BasePool.restart)

    signal\_safe = True
    :   set to true if the pool can be shutdown from within
        a signal handler.

    start()[[source]](../../_modules/celery/concurrency/base.html#BasePool.start)

    stop()[[source]](../../_modules/celery/concurrency/base.html#BasePool.stop)

    task\_join\_will\_block = True

    terminate()[[source]](../../_modules/celery/concurrency/base.html#BasePool.terminate)

    terminate\_job(*pid*, *signal=None*)[[source]](../../_modules/celery/concurrency/base.html#BasePool.terminate_job)

    uses\_semaphore = False
    :   only used by multiprocessing pool

celery.concurrency.base.apply\_target(*target*, *args=()*, *kwargs=None*, *callback=None*, *accept\_callback=None*, *pid=None*, *getpid=<built-in function getpid>*, *propagate=()*, *monotonic=<built-in function monotonic>*, *\*\*\_*)[[source]](../../_modules/celery/concurrency/base.html#apply_target)
:   Apply function within pool context.