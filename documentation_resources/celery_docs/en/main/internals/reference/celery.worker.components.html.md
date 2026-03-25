<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.worker.components.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.worker.components.html).

# `celery.worker.components`

Worker-level Bootsteps.

class celery.worker.components.Beat(*w*, *beat=False*, *\*\*kwargs*)[[source]](../../_modules/celery/worker/components.html#Beat)
:   Step used to embed a beat process.

    Enabled when the `beat` argument is set.

    conditional = True

    create(*w*)[[source]](../../_modules/celery/worker/components.html#Beat.create)
    :   Create the step.

    label = 'Beat'

    name = 'celery.worker.components.Beat'

class celery.worker.components.Consumer(*parent*, *\*\*kwargs*)[[source]](../../_modules/celery/worker/components.html#Consumer)
:   Bootstep starting the Consumer blueprint.

    create(*w*)[[source]](../../_modules/celery/worker/components.html#Consumer.create)
    :   Create the step.

    last = True

    name = 'celery.worker.components.Consumer'

class celery.worker.components.Hub(*w*, *\*\*kwargs*)[[source]](../../_modules/celery/worker/components.html#Hub)
:   Worker starts the event loop.

    create(*w*)[[source]](../../_modules/celery/worker/components.html#Hub.create)
    :   Create the step.

    include\_if(*w*)[[source]](../../_modules/celery/worker/components.html#Hub.include_if)
    :   Return true if bootstep should be included.

        You can define this as an optional predicate that decides whether
        this step should be created.

    name = 'celery.worker.components.Hub'

    requires = (step:celery.worker.components.Timer{()},)

    start(*w*)[[source]](../../_modules/celery/worker/components.html#Hub.start)

    stop(*w*)[[source]](../../_modules/celery/worker/components.html#Hub.stop)

    terminate(*w*)[[source]](../../_modules/celery/worker/components.html#Hub.terminate)

class celery.worker.components.Pool(*w*, *autoscale=None*, *\*\*kwargs*)[[source]](../../_modules/celery/worker/components.html#Pool)
:   Bootstep managing the worker pool.

    Describes how to initialize the worker pool, and starts and stops
    the pool during worker start-up/shutdown.

    Adds attributes:

    > - autoscale
    > - pool
    > - max\_concurrency
    > - min\_concurrency

    close(*w*)[[source]](../../_modules/celery/worker/components.html#Pool.close)

    create(*w*)[[source]](../../_modules/celery/worker/components.html#Pool.create)
    :   Create the step.

    info(*w*)[[source]](../../_modules/celery/worker/components.html#Pool.info)

    name = 'celery.worker.components.Pool'

    register\_with\_event\_loop(*w*, *hub*)[[source]](../../_modules/celery/worker/components.html#Pool.register_with_event_loop)

    requires = (step:celery.worker.components.Hub{(step:celery.worker.components.Timer{()},)},)

    terminate(*w*)[[source]](../../_modules/celery/worker/components.html#Pool.terminate)

class celery.worker.components.StateDB(*w*, *\*\*kwargs*)[[source]](../../_modules/celery/worker/components.html#StateDB)
:   Bootstep that sets up between-restart state database file.

    create(*w*)[[source]](../../_modules/celery/worker/components.html#StateDB.create)
    :   Create the step.

    name = 'celery.worker.components.StateDB'

class celery.worker.components.Timer(*parent*, *\*\*kwargs*)[[source]](../../_modules/celery/worker/components.html#Timer)
:   Timer bootstep.

    create(*w*)[[source]](../../_modules/celery/worker/components.html#Timer.create)
    :   Create the step.

    name = 'celery.worker.components.Timer'

    on\_timer\_error(*exc*)[[source]](../../_modules/celery/worker/components.html#Timer.on_timer_error)

    on\_timer\_tick(*delay*)[[source]](../../_modules/celery/worker/components.html#Timer.on_timer_tick)