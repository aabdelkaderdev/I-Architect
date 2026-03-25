<!-- Source: https://docs.celeryq.dev/en/main/_modules/celery/worker/consumer/control.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/celery/worker/consumer/control.html).

# Source code for celery.worker.consumer.control

```
"""Worker Remote Control Bootstep.

``Control`` -> :mod:`celery.worker.pidbox` -> :mod:`kombu.pidbox`.

The actual commands are implemented in :mod:`celery.worker.control`.
"""
from celery import bootsteps
from celery.utils.log import get_logger
from celery.worker import pidbox

from .tasks import Tasks

__all__ = ('Control',)

logger = get_logger(__name__)

[docs]
class Control(bootsteps.StartStopStep):
    """Remote control command service."""

    requires = (Tasks,)

    def __init__(self, c, **kwargs):
        self.is_green = c.pool is not None and c.pool.is_green
        self.box = (pidbox.gPidbox if self.is_green else pidbox.Pidbox)(c)
        self.start = self.box.start
        self.stop = self.box.stop
        self.shutdown = self.box.shutdown
        super().__init__(c, **kwargs)

[docs]
    def include_if(self, c):
        return (c.app.conf.worker_enable_remote_control and
                c.conninfo.supports_exchange_type('fanout'))
```