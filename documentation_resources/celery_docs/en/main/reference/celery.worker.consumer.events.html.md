<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.events.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.events.html).

# `celery.worker.consumer.events`

Worker Event Dispatcher Bootstep.

`Events` -> [`celery.events.EventDispatcher`](celery.events.html#celery.events.EventDispatcher "celery.events.EventDispatcher").

class celery.worker.consumer.events.Events(*c*, *task\_events=True*, *without\_heartbeat=False*, *without\_gossip=False*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/events.html#Events)
:   Service used for sending monitoring events.

    name = 'celery.worker.consumer.events.Events'

    requires = (step:celery.worker.consumer.connection.Connection{()},)

    shutdown(*c*)[[source]](../_modules/celery/worker/consumer/events.html#Events.shutdown)

    start(*c*)[[source]](../_modules/celery/worker/consumer/events.html#Events.start)

    stop(*c*)[[source]](../_modules/celery/worker/consumer/events.html#Events.stop)