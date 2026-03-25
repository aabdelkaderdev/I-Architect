<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.contrib.django.task.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.django.task.html).

# `celery.contrib.django.task`

Added in version 5.4.

## 

class celery.contrib.django.task.DjangoTask[[source]](../_modules/celery/contrib/django/task.html#DjangoTask)
:   Extend the base [`Task`](celery.app.task.html#celery.app.task.Task "celery.app.task.Task") for Django.

    Provide a nicer API to trigger tasks at the end of the DB transaction.

    apply\_async\_on\_commit(*\*args*, *\*\*kwargs*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/contrib/django/task.html#DjangoTask.apply_async_on_commit)
    :   Call [`apply_async()`](celery.app.task.html#celery.app.task.Task.apply_async "celery.app.task.Task.apply_async") with Django’s `on_commit()`.

    delay\_on\_commit(*\*args*, *\*\*kwargs*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/contrib/django/task.html#DjangoTask.delay_on_commit)
    :   Call [`delay()`](celery.app.task.html#celery.app.task.Task.delay "celery.app.task.Task.delay") with Django’s `on_commit()`.