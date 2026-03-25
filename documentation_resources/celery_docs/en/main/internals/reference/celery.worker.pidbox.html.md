<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.worker.pidbox.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.worker.pidbox.html).

# `celery.worker.pidbox`

Worker Pidbox (remote control).

class celery.worker.pidbox.Pidbox(*c*)[[source]](../../_modules/celery/worker/pidbox.html#Pidbox)
:   Worker mailbox.

    consumer = None

    on\_message(*body*, *message*)[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.on_message)

    on\_stop()[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.on_stop)

    reset()[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.reset)

    shutdown(*c*)[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.shutdown)

    start(*c*)[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.start)

    stop(*c*)[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.stop)

class celery.worker.pidbox.gPidbox(*c*)[[source]](../../_modules/celery/worker/pidbox.html#gPidbox)
:   Worker pidbox (greenlet).

    loop(*c*)[[source]](../../_modules/celery/worker/pidbox.html#gPidbox.loop)

    on\_stop()[[source]](../../_modules/celery/worker/pidbox.html#gPidbox.on_stop)

    reset()[[source]](../../_modules/celery/worker/pidbox.html#gPidbox.reset)

    start(*c*)[[source]](../../_modules/celery/worker/pidbox.html#gPidbox.start)