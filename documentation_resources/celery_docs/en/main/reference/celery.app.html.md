<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.app.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.html).

Celery Application.

# 

celery.app.default\_app = <Celery default>
:   Proxy always returning the app set as default.

# 

celery.app.app\_or\_default(*app=None*)
:   Function returning the app provided or the default app if none.

    The environment variable `CELERY_TRACE_APP` is used to
    trace app leaks. When enabled an exception is raised if there
    is no active app.

celery.app.enable\_trace()[[source]](../_modules/celery/_state.html#enable_trace)
:   Enable tracing of app instances.

celery.app.disable\_trace()[[source]](../_modules/celery/_state.html#disable_trace)
:   Disable tracing of app instances.