<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.worker.loops.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.worker.loops.html).

# `celery.worker.loops`

The consumers highly-optimized inner loop.

celery.worker.loops.asynloop(*obj*, *connection*, *consumer*, *blueprint*, *hub*, *qos*, *heartbeat*, *clock*, *hbrate=2.0*)[[source]](../../_modules/celery/worker/loops.html#asynloop)
:   Non-blocking event loop.

celery.worker.loops.synloop(*obj*, *connection*, *consumer*, *blueprint*, *hub*, *qos*, *heartbeat*, *clock*, *hbrate=2.0*, *\*\*kwargs*)[[source]](../../_modules/celery/worker/loops.html#synloop)
:   Fallback blocking event loop for transports that doesn’t support AIO.