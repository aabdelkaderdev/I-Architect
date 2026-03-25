<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.eventlet.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.eventlet.html).

# `celery.concurrency.eventlet`

Eventlet execution pool.

class celery.concurrency.eventlet.TaskPool(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool)
:   Eventlet Task Pool.

    class Timer(*\*args*, *\*\*kwargs*)
    :   Eventlet Timer.

        cancel(*tref*)

        clear()

        property queue
        :   Snapshot of underlying datastructure.

    grow(*n=1*)[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.grow)

    is\_green = True
    :   set to true if pool uses greenlets.

    on\_apply(*target*, *args=None*, *kwargs=None*, *callback=None*, *accept\_callback=None*, *\*\*\_*)[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.on_apply)

    on\_start()[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.on_start)

    on\_stop()[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.on_stop)

    shrink(*n=1*)[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.shrink)

    signal\_safe = False
    :   set to true if the pool can be shutdown from within
        a signal handler.

    task\_join\_will\_block = False

    terminate\_job(*pid*, *signal=None*)[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.terminate_job)