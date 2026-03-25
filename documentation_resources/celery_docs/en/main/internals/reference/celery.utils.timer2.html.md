<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.timer2.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.timer2.html).

# `celery.utils.timer2`

Scheduler for Python functions.

Note

This is used for the thread-based worker only,
not for amqp/redis/sqs/qpid where [`kombu.asynchronous.timer`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.asynchronous.timer.html#module-kombu.asynchronous.timer "(in Kombu v5.6)") is used.

class celery.utils.timer2.Entry(*fun*, *args=None*, *kwargs=None*)[[source]](../../_modules/kombu/asynchronous/timer.html#Entry)
:   Schedule Entry.

    args

    cancel()[[source]](../../_modules/kombu/asynchronous/timer.html#Entry.cancel)

    canceled

    property cancelled

    fun

    kwargs

    tref

celery.utils.timer2.Schedule
:   alias of [`Timer`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.asynchronous.timer.html#kombu.asynchronous.timer.Timer "(in Kombu v5.6)")

class celery.utils.timer2.Timer(*schedule: [Timer](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.asynchronous.timer.html#kombu.asynchronous.timer.Timer "(in Kombu v5.6)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *on\_error: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")[[[Exception](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)")], [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *on\_tick: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")[[[float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")], [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *on\_start: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")[[[Timer](#celery.utils.timer2.Timer "celery.utils.timer2.Timer")], [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *max\_interval: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../../_modules/celery/utils/timer2.html#Timer)
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

    call\_after(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Entry](#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")[[source]](../../_modules/celery/utils/timer2.html#Timer.call_after)

    call\_at(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Entry](#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")[[source]](../../_modules/celery/utils/timer2.html#Timer.call_at)

    call\_repeatedly(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Entry](#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")[[source]](../../_modules/celery/utils/timer2.html#Timer.call_repeatedly)

    cancel(*tref: [Entry](#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/timer2.html#Timer.cancel)

    clear() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/timer2.html#Timer.clear)

    empty() → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")[[source]](../../_modules/celery/utils/timer2.html#Timer.empty)

    ensure\_started() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/timer2.html#Timer.ensure_started)

    enter(*entry: [Entry](#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")*, *eta: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")*, *priority: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [Entry](#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")[[source]](../../_modules/celery/utils/timer2.html#Timer.enter)

    enter\_after(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Entry](#celery.utils.timer2.Timer.Entry "kombu.asynchronous.timer.Entry")[[source]](../../_modules/celery/utils/timer2.html#Timer.enter_after)

    exit\_after(*secs: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")*, *priority: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 10*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/timer2.html#Timer.exit_after)

    next() → [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")

    on\_tick: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")[[[float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")], [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None

    property queue: [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")

    run() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/timer2.html#Timer.run)
    :   Method representing the thread’s activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object’s constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

    running: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False

    stop() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/timer2.html#Timer.stop)

celery.utils.timer2.to\_timestamp(*d*, *default\_timezone=zoneinfo.ZoneInfo(key='UTC')*, *time=<built-in function monotonic>*)[[source]](../../_modules/kombu/asynchronous/timer.html#to_timestamp)
:   Convert datetime to timestamp.

    If d’ is already a timestamp, then that will be used.