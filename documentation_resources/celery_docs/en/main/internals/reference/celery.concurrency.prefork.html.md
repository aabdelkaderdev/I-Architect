<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.prefork.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.prefork.html).

# `celery.concurrency.prefork`

Prefork execution pool.

Pool implementation using [`multiprocessing`](https://docs.python.org/dev/library/multiprocessing.html#module-multiprocessing "(in Python v3.15)").

class celery.concurrency.prefork.TaskPool(*limit=None*, *putlocks=True*, *forking\_enable=True*, *callbacks\_propagate=()*, *app=None*, *\*\*options*)[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool)
:   Multiprocessing Pool implementation.

    BlockingPool
    :   alias of `Pool`

    Pool
    :   alias of `AsynPool`

    did\_start\_ok()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.did_start_ok)

    property num\_processes

    on\_close()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.on_close)

    on\_start()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.on_start)

    on\_stop()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.on_stop)
    :   Gracefully stop the pool.

    on\_terminate()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.on_terminate)
    :   Force terminate the pool.

    register\_with\_event\_loop(*loop*)[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.register_with_event_loop)

    restart()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.restart)

    uses\_semaphore = True
    :   only used by multiprocessing pool

    write\_stats = None

celery.concurrency.prefork.process\_destructor(*pid*, *exitcode*)[[source]](../../_modules/celery/concurrency/prefork.html#process_destructor)
:   Pool child process destructor.

    Dispatch the [`worker_process_shutdown`](../../userguide/signals.html#std-signal-worker_process_shutdown) signal.

celery.concurrency.prefork.process\_initializer(*app*, *hostname*)[[source]](../../_modules/celery/concurrency/prefork.html#process_initializer)
:   Pool child process initializer.

    Initialize the child pool process to ensure the correct
    app instance is used and things like logging works.