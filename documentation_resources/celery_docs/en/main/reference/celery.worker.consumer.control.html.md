<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.control.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.control.html).

# `celery.worker.consumer.control`

Worker Remote Control Bootstep.

`Control` -> [`celery.worker.pidbox`](../internals/reference/celery.worker.pidbox.html#module-celery.worker.pidbox "celery.worker.pidbox") -> [`kombu.pidbox`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.pidbox.html#module-kombu.pidbox "(in Kombu v5.6)").

The actual commands are implemented in [`celery.worker.control`](../internals/reference/celery.worker.control.html#module-celery.worker.control "celery.worker.control").

class celery.worker.consumer.control.Control(*c*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/control.html#Control)
:   Remote control command service.

    include\_if(*c*)[[source]](../_modules/celery/worker/consumer/control.html#Control.include_if)
    :   Return true if bootstep should be included.

        You can define this as an optional predicate that decides whether
        this step should be created.

    name = 'celery.worker.consumer.control.Control'

    requires = (step:celery.worker.consumer.tasks.Tasks{(step:celery.worker.consumer.mingle.Mingle{(step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)},)},)