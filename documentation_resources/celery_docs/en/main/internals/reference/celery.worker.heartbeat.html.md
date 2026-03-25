<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.worker.heartbeat.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.worker.heartbeat.html).

# `celery.worker.heartbeat`

Heartbeat service.

This is the internal thread responsible for sending heartbeat events
at regular intervals (may not be an actual thread).

class celery.worker.heartbeat.Heart(*timer*, *eventer*, *interval=None*)[[source]](../../_modules/celery/worker/heartbeat.html#Heart)
:   Timer sending heartbeats at regular intervals.

    Parameters:
    :   - **timer** ([*kombu.asynchronous.timer.Timer*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.asynchronous.timer.html#kombu.asynchronous.timer.Timer "(in Kombu v5.6)")) – Timer to use.
        - **eventer** ([*celery.events.EventDispatcher*](../../reference/celery.events.html#celery.events.EventDispatcher "celery.events.EventDispatcher")) – Event dispatcher
          to use.
        - **interval** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time in seconds between sending
          heartbeats. Default is 2 seconds.

    start()[[source]](../../_modules/celery/worker/heartbeat.html#Heart.start)

    stop()[[source]](../../_modules/celery/worker/heartbeat.html#Heart.stop)