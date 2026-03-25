<!-- Source: https://docs.celeryq.dev/en/main/_modules/celery/worker/consumer/heart.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/celery/worker/consumer/heart.html).

# Source code for celery.worker.consumer.heart

```
"""Worker Event Heartbeat Bootstep."""
from celery import bootsteps
from celery.worker import heartbeat

from .events import Events

__all__ = ('Heart',)

[docs]
class Heart(bootsteps.StartStopStep):
    """Bootstep sending event heartbeats.

    This service sends a ``worker-heartbeat`` message every n seconds.

    Note:
        Not to be confused with AMQP protocol level heartbeats.
    """

    requires = (Events,)

    def __init__(self, c,
                 without_heartbeat=False, heartbeat_interval=None, **kwargs):
        self.enabled = not without_heartbeat
        self.heartbeat_interval = heartbeat_interval
        c.heart = None
        super().__init__(c, **kwargs)

[docs]
    def start(self, c):
        c.heart = heartbeat.Heart(
            c.timer, c.event_dispatcher, self.heartbeat_interval,
        )
        c.heart.start()

[docs]
    def stop(self, c):
        c.heart = c.heart and c.heart.stop()

shutdown = stop
```