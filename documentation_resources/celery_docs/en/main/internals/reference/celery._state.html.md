<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery._state.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery._state.html).

# `celery._state`

Internal state.

This is an internal module containing thread state
like the `current_app`, and `current_task`.

This module shouldn’t be used directly.

celery.\_state.connect\_on\_app\_finalize(*callback*)[[source]](../../_modules/celery/_state.html#connect_on_app_finalize)
:   Connect callback to be called when any app is finalized.

celery.\_state.current\_app = <Celery default>
:   Proxy to current app.

celery.\_state.current\_task = None
:   Proxy to current task.

celery.\_state.get\_current\_app()[[source]](../../_modules/celery/_state.html#get_current_app)

celery.\_state.get\_current\_task()[[source]](../../_modules/celery/_state.html#get_current_task)
:   Currently executing task.

celery.\_state.get\_current\_worker\_task()[[source]](../../_modules/celery/_state.html#get_current_worker_task)
:   Currently executing task, that was applied by the worker.

    This is used to differentiate between the actual task
    executed by the worker and any task that was called within
    a task (using `task.__call__` or `task.apply`)

celery.\_state.set\_default\_app(*app*)[[source]](../../_modules/celery/_state.html#set_default_app)
:   Set default app.