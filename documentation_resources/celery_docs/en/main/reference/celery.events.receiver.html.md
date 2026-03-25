<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.events.receiver.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.events.receiver.html).

# `celery.events.receiver`

Event receiver implementation.

class celery.events.receiver.EventReceiver(*channel*, *handlers=None*, *routing\_key='#'*, *node\_id=None*, *app=None*, *queue\_prefix=None*, *accept=None*, *queue\_ttl=None*, *queue\_expires=None*, *queue\_exclusive=None*, *queue\_durable=None*)[[source]](../_modules/celery/events/receiver.html#EventReceiver)
:   Capture events.

    Parameters:
    :   - **connection** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Connection to the broker.
        - **handlers** (*Mapping**[**Callable**]*) – Event handlers.
          This is a map of event type names and their handlers.
          The special handler “\*” captures all events that don’t have a
          handler.

    app = None

    capture(*limit=None*, *timeout=None*, *wakeup=True*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.capture)
    :   Open up a consumer capturing events.

        This has to run in the main process, and it will never stop
        unless `EventDispatcher.should_stop` is set to True, or
        forced via [`KeyboardInterrupt`](https://docs.python.org/dev/library/exceptions.html#KeyboardInterrupt "(in Python v3.15)") or [`SystemExit`](https://docs.python.org/dev/library/exceptions.html#SystemExit "(in Python v3.15)").

    property connection

    event\_from\_message(*body*, *localize=True*, *now=<built-in function time>*, *tzfields=operator.itemgetter('utcoffset'*, *'timestamp')*, *adjust\_timestamp=<function adjust\_timestamp>*, *CLIENT\_CLOCK\_SKEW=-1*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.event_from_message)

    get\_consumers(*Consumer*, *channel*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.get_consumers)

    itercapture(*limit=None*, *timeout=None*, *wakeup=True*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.itercapture)

    on\_consume\_ready(*connection*, *channel*, *consumers*, *wakeup=True*, *\*\*kwargs*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.on_consume_ready)

    process(*type*, *event*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.process)
    :   Process event by dispatching to configured handler.

    wakeup\_workers(*channel=None*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.wakeup_workers)