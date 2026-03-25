<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.app.registry.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.registry.html).

# `celery.app.registry`

Registry of available tasks.

class celery.app.registry.TaskRegistry[[source]](../_modules/celery/app/registry.html#TaskRegistry)
:   Map of registered tasks.

    exception NotRegistered
    :   The task is not registered.

    filter\_types(*type*)[[source]](../_modules/celery/app/registry.html#TaskRegistry.filter_types)

    periodic()[[source]](../_modules/celery/app/registry.html#TaskRegistry.periodic)

    register(*task*)[[source]](../_modules/celery/app/registry.html#TaskRegistry.register)
    :   Register a task in the task registry.

        The task will be automatically instantiated if not already an
        instance. Name must be configured prior to registration.

    regular()[[source]](../_modules/celery/app/registry.html#TaskRegistry.regular)

    unregister(*name*)[[source]](../_modules/celery/app/registry.html#TaskRegistry.unregister)
    :   Unregister task by name.

        Parameters:
        :   **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – name of the task to unregister, or a
            [`celery.app.task.Task`](celery.app.task.html#celery.app.task.Task "celery.app.task.Task") with a valid name attribute.

        Raises:
        :   [**celery.exceptions.NotRegistered**](celery.exceptions.html#celery.exceptions.NotRegistered "celery.exceptions.NotRegistered") – if the task is not registered.