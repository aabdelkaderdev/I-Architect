<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.events.snapshot.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.events.snapshot.html).

# `celery.events.snapshot`

Periodically store events in a database.

Consuming the events as a stream isn’t always suitable
so this module implements a system to take snapshots of the
state of a cluster at regular intervals. There’s a full
implementation of this writing the snapshots to a database
in `djcelery.snapshots` in the django-celery distribution.

class celery.events.snapshot.Polaroid(*state*, *freq=1.0*, *maxrate=None*, *cleanup\_freq=3600.0*, *timer=None*, *app=None*)[[source]](../../_modules/celery/events/snapshot.html#Polaroid)
:   Record event snapshots.

    cancel()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.cancel)

    capture()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.capture)

    cleanup()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.cleanup)

    cleanup\_signal = <Signal: cleanup\_signal providing\_args=set()>

    clear\_after = False

    install()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.install)

    on\_cleanup()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.on_cleanup)

    on\_shutter(*state*)[[source]](../../_modules/celery/events/snapshot.html#Polaroid.on_shutter)

    shutter()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.shutter)

    shutter\_signal = <Signal: shutter\_signal providing\_args={'state'}>

    timer = None

celery.events.snapshot.evcam(*camera*, *freq=1.0*, *maxrate=None*, *loglevel=0*, *logfile=None*, *pidfile=None*, *timer=None*, *app=None*, *\*\*kwargs*)[[source]](../../_modules/celery/events/snapshot.html#evcam)
:   Start snapshot recorder.