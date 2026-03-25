<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.worker.autoscale.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.worker.autoscale.html).

# `celery.worker.autoscale`

Pool Autoscaling.

This module implements the internal thread responsible
for growing and shrinking the pool according to the
current autoscale settings.

The autoscale thread is only enabled if
the [`celery worker --autoscale`](../../reference/cli.html#cmdoption-celery-worker-autoscale) option is used.

class celery.worker.autoscale.Autoscaler(*pool*, *max\_concurrency*, *min\_concurrency=0*, *worker=None*, *keepalive=30.0*, *mutex=None*)[[source]](../../_modules/celery/worker/autoscale.html#Autoscaler)
:   Background thread to autoscale pool workers.

    body()[[source]](../../_modules/celery/worker/autoscale.html#Autoscaler.body)

    info()[[source]](../../_modules/celery/worker/autoscale.html#Autoscaler.info)

    maybe\_scale(*req=None*)[[source]](../../_modules/celery/worker/autoscale.html#Autoscaler.maybe_scale)

    property processes

    property qty

    scale\_down(*n*)[[source]](../../_modules/celery/worker/autoscale.html#Autoscaler.scale_down)

    scale\_up(*n*)[[source]](../../_modules/celery/worker/autoscale.html#Autoscaler.scale_up)

    update(*max=None*, *min=None*)[[source]](../../_modules/celery/worker/autoscale.html#Autoscaler.update)

class celery.worker.autoscale.WorkerComponent(*w*, *\*\*kwargs*)[[source]](../../_modules/celery/worker/autoscale.html#WorkerComponent)
:   Bootstep that starts the autoscaler thread/timer in the worker.

    conditional = True

    create(*w*)[[source]](../../_modules/celery/worker/autoscale.html#WorkerComponent.create)
    :   Create the step.

    info(*w*)[[source]](../../_modules/celery/worker/autoscale.html#WorkerComponent.info)
    :   Return Autoscaler info.

    label = 'Autoscaler'

    name = 'celery.worker.autoscale.WorkerComponent'

    register\_with\_event\_loop(*w*, *hub*)[[source]](../../_modules/celery/worker/autoscale.html#WorkerComponent.register_with_event_loop)

    requires = (step:celery.worker.components.Pool{(step:celery.worker.components.Hub{(step:celery.worker.components.Timer{()},)},)},)