<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.gevent.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.gevent.html).

# `celery.concurrency.gevent`

Gevent execution pool.

class celery.concurrency.gevent.TaskPool(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool)
:   GEvent Pool.

    class Timer(*\*args*, *\*\*kwargs*)
    :   clear()

        property queue
        :   Snapshot of underlying datastructure.

    grow(*n=1*)[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.grow)

    is\_green = True
    :   set to true if pool uses greenlets.

    property num\_processes

    on\_apply(*target*, *args=None*, *kwargs=None*, *callback=None*, *accept\_callback=None*, *timeout=None*, *timeout\_callback=None*, *apply\_target=<function apply\_target>*, *\*\*\_*)[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.on_apply)

    on\_start()[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.on_start)

    on\_stop()[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.on_stop)

    shrink(*n=1*)[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.shrink)

    signal\_safe = False
    :   set to true if the pool can be shutdown from within
        a signal handler.

    task\_join\_will\_block = False

    terminate\_job(*pid*, *signal=None*)[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.terminate_job)