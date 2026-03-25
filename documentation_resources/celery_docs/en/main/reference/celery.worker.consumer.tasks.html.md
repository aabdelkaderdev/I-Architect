<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.tasks.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.tasks.html).

# `celery.worker.consumer.tasks`

Worker Task Consumer Bootstep.

class celery.worker.consumer.tasks.Tasks(*c*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks)
:   Bootstep starting the task message consumer.

    info(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.info)
    :   Return task consumer info.

    name = 'celery.worker.consumer.tasks.Tasks'

    qos\_global(*c*) → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.qos_global)
    :   Determine if global QoS should be applied.

        Additional information:
        :   <https://www.rabbitmq.com/docs/consumer-prefetch>
            <https://www.rabbitmq.com/docs/quorum-queues#global-qos>

    requires = (step:celery.worker.consumer.mingle.Mingle{(step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)},)

    shutdown(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.shutdown)
    :   Shutdown task consumer.

    start(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.start)
    :   Start task consumer.

    stop(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.stop)
    :   Stop task consumer.