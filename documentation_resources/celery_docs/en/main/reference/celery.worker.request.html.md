<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.request.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.request.html).

# `celery.worker.request`

Task request.

This module defines the [`Request`](#celery.worker.request.Request "celery.worker.request.Request") class, that specifies
how tasks are executed.

class celery.worker.request.Request(*message*, *on\_ack=<function noop>*, *hostname=None*, *eventer=None*, *app=None*, *connection\_errors=None*, *request\_dict=None*, *task=None*, *on\_reject=<function noop>*, *body=None*, *headers=None*, *decoded=False*, *utc=True*, *maybe\_make\_aware=<function maybe\_make\_aware>*, *maybe\_iso8601=<function maybe\_iso8601>*, *\*\*opts*)[[source]](../_modules/celery/worker/request.html#Request)
:   A request for task execution.

    acknowledge()[[source]](../_modules/celery/worker/request.html#Request.acknowledge)
    :   Acknowledge task.

    acknowledged = False

    property app

    property args

    property argsrepr

    property body

    cancel(*pool*, *signal=None*, *emit\_retry=True*)[[source]](../_modules/celery/worker/request.html#Request.cancel)

    property chord

    property connection\_errors

    property content\_encoding

    property content\_type

    property correlation\_id

    property delivery\_info

    property errbacks

    property eta

    property eventer

    execute(*loglevel=None*, *logfile=None*)[[source]](../_modules/celery/worker/request.html#Request.execute)
    :   Execute the task in a [`trace_task()`](../internals/reference/celery.app.trace.html#celery.app.trace.trace_task "celery.app.trace.trace_task").

        Parameters:
        :   - **loglevel** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – The loglevel used by the task.
            - **logfile** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – The logfile used by the task.

    execute\_using\_pool(*pool: [BasePool](../internals/reference/celery.concurrency.base.html#celery.concurrency.base.BasePool "celery.concurrency.base.BasePool")*, *\*\*kwargs*)[[source]](../_modules/celery/worker/request.html#Request.execute_using_pool)
    :   Used by the worker to send this task to the pool.

        Parameters:
        :   **pool** (*TaskPool*) – The execution pool
            used to execute this request.

        Raises:
        :   [**celery.exceptions.TaskRevokedError**](celery.exceptions.html#celery.exceptions.TaskRevokedError "celery.exceptions.TaskRevokedError") – if the task was revoked.

    property expires

    property group

    property group\_index

    property groups

    property hostname

    humaninfo()[[source]](../_modules/celery/worker/request.html#Request.humaninfo)

    id

    property ignore\_result

    info(*safe=False*)[[source]](../_modules/celery/worker/request.html#Request.info)

    property kwargs

    property kwargsrepr

    maybe\_expire()[[source]](../_modules/celery/worker/request.html#Request.maybe_expire)
    :   If expired, mark the task as revoked.

    property message

    name

    on\_accepted(*pid*, *time\_accepted*)[[source]](../_modules/celery/worker/request.html#Request.on_accepted)
    :   Handler called when task is accepted by worker pool.

    property on\_ack

    on\_failure(*exc\_info*, *send\_failed\_event=True*, *return\_ok=False*)[[source]](../_modules/celery/worker/request.html#Request.on_failure)
    :   Handler called if the task raised an exception.

    property on\_reject

    on\_retry(*exc\_info*)[[source]](../_modules/celery/worker/request.html#Request.on_retry)
    :   Handler called if the task should be retried.

    on\_success(*failed\_\_retval\_\_runtime*, *\*\*kwargs*)[[source]](../_modules/celery/worker/request.html#Request.on_success)
    :   Handler called if the task was successfully processed.

    on\_timeout(*soft*, *timeout*)[[source]](../_modules/celery/worker/request.html#Request.on_timeout)
    :   Handler called if the task times out.

    property parent\_id

    reject(*requeue=False*)[[source]](../_modules/celery/worker/request.html#Request.reject)

    property replaced\_task\_nesting

    property reply\_to

    property request\_dict

    revoked()[[source]](../_modules/celery/worker/request.html#Request.revoked)
    :   If revoked, skip task and mark state.

    property root\_id

    send\_event(*type*, *\*\*fields*)[[source]](../_modules/celery/worker/request.html#Request.send_event)

    property stamped\_headers: [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")

    property stamps: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

    property store\_errors

    property task

    property task\_id

    property task\_name

    terminate(*pool*, *signal=None*)[[source]](../_modules/celery/worker/request.html#Request.terminate)

    time\_limits = (None, None)

    time\_start = None

    property type

    property tzlocal

    property utc

    worker\_pid = None