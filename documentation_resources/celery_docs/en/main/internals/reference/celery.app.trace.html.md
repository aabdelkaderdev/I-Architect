<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.app.trace.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.app.trace.html).

# `celery.app.trace`

Trace task execution.

This module defines how the task execution is traced:
errors are recorded, handlers are applied and so on.

class celery.app.trace.TraceInfo(*state*, *retval=None*)[[source]](../../_modules/celery/app/trace.html#TraceInfo)
:   Information about task execution.

    handle\_error\_state(*task*, *req*, *eager=False*, *call\_errbacks=True*)[[source]](../../_modules/celery/app/trace.html#TraceInfo.handle_error_state)

    handle\_failure(*task*, *req*, *store\_errors=True*, *call\_errbacks=True*)[[source]](../../_modules/celery/app/trace.html#TraceInfo.handle_failure)
    :   Handle exception.

    handle\_ignore(*task*, *req*, *\*\*kwargs*)[[source]](../../_modules/celery/app/trace.html#TraceInfo.handle_ignore)

    handle\_reject(*task*, *req*, *\*\*kwargs*)[[source]](../../_modules/celery/app/trace.html#TraceInfo.handle_reject)

    handle\_retry(*task*, *req*, *store\_errors=True*, *\*\*kwargs*)[[source]](../../_modules/celery/app/trace.html#TraceInfo.handle_retry)
    :   Handle retry exception.

    retval

    state

celery.app.trace.build\_tracer(*name*, *task*, *loader=None*, *hostname=None*, *store\_errors=True*, *Info=<class 'celery.app.trace.TraceInfo'>*, *eager=False*, *propagate=False*, *app=None*, *monotonic=<built-in function monotonic>*, *trace\_ok\_t=<class 'celery.app.trace.trace\_ok\_t'>*, *IGNORE\_STATES=frozenset({'IGNORED'*, *'REJECTED'*, *'RETRY'})*)[[source]](../../_modules/celery/app/trace.html#build_tracer)
:   Return a function that traces task execution.

    Catches all exceptions and updates result backend with the
    state and result.

    If the call was successful, it saves the result to the task result
    backend, and sets the task status to “SUCCESS”.

    If the call raises [`Retry`](../../reference/celery.exceptions.html#celery.exceptions.Retry "celery.exceptions.Retry"), it extracts
    the original exception, uses that as the result and sets the task state
    to “RETRY”.

    If the call results in an exception, it saves the exception as the task
    result, and sets the task state to “FAILURE”.

    Return a function that takes the following arguments:

    > param uuid:
    > :   The id of the task.
    >
    > param args:
    > :   List of positional args to pass on to the function.
    >
    > param kwargs:
    > :   Keyword arguments mapping to pass on to the function.
    >
    > keyword request:
    > :   Request dict.

celery.app.trace.reset\_worker\_optimizations(*app=<Celery default>*)[[source]](../../_modules/celery/app/trace.html#reset_worker_optimizations)
:   Reset previously configured optimizations.

celery.app.trace.setup\_worker\_optimizations(*app*, *hostname=None*)[[source]](../../_modules/celery/app/trace.html#setup_worker_optimizations)
:   Setup worker related optimizations.

celery.app.trace.trace\_task(*task*, *uuid*, *args*, *kwargs*, *request=None*, *\*\*opts*)[[source]](../../_modules/celery/app/trace.html#trace_task)
:   Trace task execution.