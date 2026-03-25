<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.app.events.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.events.html).

# `celery.app.events`

Implementation for the app.events shortcuts.

class celery.app.events.Events(*app=None*)[[source]](../_modules/celery/app/events.html#Events)
:   Implements app.events.

    property Dispatcher

    property Receiver

    property State

    default\_dispatcher(*hostname=None*, *enabled=True*, *buffer\_while\_offline=False*)[[source]](../_modules/celery/app/events.html#Events.default_dispatcher)

    dispatcher\_cls = 'celery.events.dispatcher:EventDispatcher'

    receiver\_cls = 'celery.events.receiver:EventReceiver'

    state\_cls = 'celery.events.state:State'