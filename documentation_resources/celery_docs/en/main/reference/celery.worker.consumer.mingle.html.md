<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.mingle.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.mingle.html).

# `celery.worker.consumer.mingle`

Worker <-> Worker Sync at startup (Bootstep).

class celery.worker.consumer.mingle.Mingle(*c*, *without\_mingle=False*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle)
:   Bootstep syncing state with neighbor workers.

    At startup, or upon consumer restart, this will:

    - Sync logical clocks.
    - Sync revoked tasks.

    compatible\_transport(*app*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.compatible_transport)

    compatible\_transports = {'amqp', 'gcpubsub', 'redis'}

    label = 'Mingle'

    name = 'celery.worker.consumer.mingle.Mingle'

    on\_clock\_event(*c*, *clock*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.on_clock_event)

    on\_node\_reply(*c*, *nodename*, *reply*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.on_node_reply)

    on\_revoked\_received(*c*, *revoked*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.on_revoked_received)

    requires = (step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)

    send\_hello(*c*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.send_hello)

    start(*c*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.start)

    sync(*c*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.sync)

    sync\_with\_node(*c*, *clock=None*, *revoked=None*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.sync_with_node)