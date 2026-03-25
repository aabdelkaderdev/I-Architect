<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.thread.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.thread.html).

# `celery.concurrency.thread`

Thread execution pool.

class celery.concurrency.thread.TaskPool(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../../_modules/celery/concurrency/thread.html#TaskPool)
:   Thread Task Pool.

    body\_can\_be\_buffer = True

    limit: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")

    on\_apply(*target: TargetFunction*, *args: [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[Any, ...] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *kwargs: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), Any] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *callback: Callable[..., Any] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *accept\_callback: Callable[..., Any] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *\*\*\_: Any*) → ApplyResult[[source]](../../_modules/celery/concurrency/thread.html#TaskPool.on_apply)

    on\_stop() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/concurrency/thread.html#TaskPool.on_stop)

    signal\_safe = False
    :   set to true if the pool can be shutdown from within
        a signal handler.