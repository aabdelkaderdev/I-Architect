<!-- Source: https://docs.celeryq.dev/en/main/_modules/celery/contrib/django/task.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/celery/contrib/django/task.html).

# Source code for celery.contrib.django.task

```
import functools

from django.db import transaction

from celery.app.task import Task

[docs]
class DjangoTask(Task):
    """
    Extend the base :class:`~celery.app.task.Task` for Django.

    Provide a nicer API to trigger tasks at the end of the DB transaction.
    """

[docs]
    def delay_on_commit(self, *args, **kwargs) -> None:
        """Call :meth:`~celery.app.task.Task.delay` with Django's ``on_commit()``."""
        transaction.on_commit(functools.partial(self.delay, *args, **kwargs))

[docs]
    def apply_async_on_commit(self, *args, **kwargs) -> None:
        """Call :meth:`~celery.app.task.Task.apply_async` with Django's ``on_commit()``."""
        transaction.on_commit(functools.partial(self.apply_async, *args, **kwargs))
```