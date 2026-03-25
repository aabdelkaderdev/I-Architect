<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.html).

# `celery.worker`

Worker implementation.

class celery.worker.WorkController(*app=None*, *hostname=None*, *\*\*kwargs*)[[source]](../_modules/celery/worker/worker.html#WorkController)
:   Unmanaged worker instance.

    class Blueprint(*steps=None*, *name=None*, *on\_start=None*, *on\_close=None*, *on\_stopped=None*)[[source]](../_modules/celery/worker/worker.html#WorkController.Blueprint)
    :   Worker bootstep blueprint.

        default\_steps = {'celery.worker.autoscale:WorkerComponent', 'celery.worker.components:Beat', 'celery.worker.components:Consumer', 'celery.worker.components:Hub', 'celery.worker.components:Pool', 'celery.worker.components:StateDB', 'celery.worker.components:Timer'}

        name = 'Worker'

    app = None

    blueprint = None

    exitcode = None
    :   contains the exit code if a [`SystemExit`](https://docs.python.org/dev/library/exceptions.html#SystemExit "(in Python v3.15)") event is handled.

    info()[[source]](../_modules/celery/worker/worker.html#WorkController.info)

    on\_after\_init(*\*\*kwargs*)[[source]](../_modules/celery/worker/worker.html#WorkController.on_after_init)

    on\_before\_init(*\*\*kwargs*)[[source]](../_modules/celery/worker/worker.html#WorkController.on_before_init)

    on\_close()[[source]](../_modules/celery/worker/worker.html#WorkController.on_close)

    on\_consumer\_ready(*consumer*)[[source]](../_modules/celery/worker/worker.html#WorkController.on_consumer_ready)

    on\_init\_blueprint()[[source]](../_modules/celery/worker/worker.html#WorkController.on_init_blueprint)

    on\_start()[[source]](../_modules/celery/worker/worker.html#WorkController.on_start)

    on\_stopped()[[source]](../_modules/celery/worker/worker.html#WorkController.on_stopped)

    pidlock = None

    pool = None

    prepare\_args(*\*\*kwargs*)[[source]](../_modules/celery/worker/worker.html#WorkController.prepare_args)

    register\_with\_event\_loop(*hub*)[[source]](../_modules/celery/worker/worker.html#WorkController.register_with_event_loop)

    reload(*modules=None*, *reload=False*, *reloader=None*)[[source]](../_modules/celery/worker/worker.html#WorkController.reload)

    rusage()[[source]](../_modules/celery/worker/worker.html#WorkController.rusage)

    semaphore = None

    setup\_defaults(*concurrency=None*, *loglevel='WARN'*, *logfile=None*, *task\_events=None*, *pool=None*, *consumer\_cls=None*, *timer\_cls=None*, *timer\_precision=None*, *autoscaler\_cls=None*, *pool\_putlocks=None*, *pool\_restarts=None*, *optimization=None*, *O=None*, *statedb=None*, *time\_limit=None*, *soft\_time\_limit=None*, *scheduler=None*, *pool\_cls=None*, *state\_db=None*, *task\_time\_limit=None*, *task\_soft\_time\_limit=None*, *scheduler\_cls=None*, *schedule\_filename=None*, *max\_tasks\_per\_child=None*, *prefetch\_multiplier=None*, *disable\_rate\_limits=None*, *worker\_lost\_wait=None*, *max\_memory\_per\_child=None*, *\*\*\_kw*)[[source]](../_modules/celery/worker/worker.html#WorkController.setup_defaults)

    setup\_includes(*includes*)[[source]](../_modules/celery/worker/worker.html#WorkController.setup_includes)

    setup\_instance(*queues=None*, *ready\_callback=None*, *pidfile=None*, *include=None*, *use\_eventloop=None*, *exclude\_queues=None*, *\*\*kwargs*)[[source]](../_modules/celery/worker/worker.html#WorkController.setup_instance)

    setup\_queues(*include*, *exclude=None*)[[source]](../_modules/celery/worker/worker.html#WorkController.setup_queues)

    should\_use\_eventloop()[[source]](../_modules/celery/worker/worker.html#WorkController.should_use_eventloop)

    signal\_consumer\_close()[[source]](../_modules/celery/worker/worker.html#WorkController.signal_consumer_close)

    start()[[source]](../_modules/celery/worker/worker.html#WorkController.start)

    property state

    stats()[[source]](../_modules/celery/worker/worker.html#WorkController.stats)

    stop(*in\_sighandler=False*, *exitcode=None*)[[source]](../_modules/celery/worker/worker.html#WorkController.stop)
    :   Graceful shutdown of the worker server (Warm shutdown).

    terminate(*in\_sighandler=False*)[[source]](../_modules/celery/worker/worker.html#WorkController.terminate)
    :   Not so graceful shutdown of the worker server (Cold shutdown).

    wait\_for\_soft\_shutdown()[[source]](../_modules/celery/worker/worker.html#WorkController.wait_for_soft_shutdown)
    :   Wait [`worker_soft_shutdown_timeout`](../userguide/configuration.html#std-setting-worker_soft_shutdown_timeout) if soft shutdown is enabled.

        To enable soft shutdown, set the [`worker_soft_shutdown_timeout`](../userguide/configuration.html#std-setting-worker_soft_shutdown_timeout) in the
        configuration. Soft shutdown can be used to allow the worker to finish processing
        few more tasks before initiating a cold shutdown. This mechanism allows the worker
        to finish short tasks that are already in progress and requeue long-running tasks
        to be picked up by another worker.

        Warning

        If there are no tasks in the worker, the worker will not wait for the
        soft shutdown timeout even if it is set as it makes no sense to wait for
        the timeout when there are no tasks to process.