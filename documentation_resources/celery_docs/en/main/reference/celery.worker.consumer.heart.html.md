<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.heart.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.heart.html).

# `celery.worker.consumer.heart`

Worker Event Heartbeat Bootstep.

class celery.worker.consumer.heart.Heart(*c*, *without\_heartbeat=False*, *heartbeat\_interval=None*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/heart.html#Heart)
:   Bootstep sending event heartbeats.

    This service sends a `worker-heartbeat` message every n seconds.

    Note

    Not to be confused with AMQP protocol level heartbeats.

    name = 'celery.worker.consumer.heart.Heart'

    requires = (step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)

    shutdown(*c*)

    start(*c*)[[source]](../_modules/celery/worker/consumer/heart.html#Heart.start)

    stop(*c*)[[source]](../_modules/celery/worker/consumer/heart.html#Heart.stop)