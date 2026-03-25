<!-- Source: https://docs.celeryq.dev/en/main/_modules/celery/concurrency/solo.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/celery/concurrency/solo.html).

# Source code for celery.concurrency.solo

```
"""Single-threaded execution pool."""
import os

from celery import signals

from .base import BasePool, apply_target

__all__ = ('TaskPool',)

[docs]
class TaskPool(BasePool):
    """Solo task pool (blocking, inline, fast)."""

    body_can_be_buffer = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_apply = apply_target
        self.limit = 1
        signals.worker_process_init.send(sender=None)

    def _get_info(self):
        info = super()._get_info()
        info.update({
            'max-concurrency': 1,
            'processes': [os.getpid()],
            'max-tasks-per-child': None,
            'put-guarded-by-semaphore': True,
            'timeouts': (),
        })
        return info
```