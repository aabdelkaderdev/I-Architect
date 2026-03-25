<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.solo.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.solo.html).

# `celery.concurrency.solo`

Single-threaded execution pool.

class celery.concurrency.solo.TaskPool(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/concurrency/solo.html#TaskPool)
:   Solo task pool (blocking, inline, fast).

    body\_can\_be\_buffer = True