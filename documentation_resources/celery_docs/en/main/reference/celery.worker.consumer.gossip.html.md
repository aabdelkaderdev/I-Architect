<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.gossip.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.gossip.html).

# `celery.worker.consumer.gossip`

Worker <-> Worker communication Bootstep.

class celery.worker.consumer.gossip.Gossip(*c*, *without\_gossip=False*, *interval=5.0*, *heartbeat\_interval=2.0*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip)
:   Bootstep consuming events from other workers.

    This keeps the logical clock value up to date.

    call\_task(*task*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.call_task)

    compatible\_transport(*app*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.compatible_transport)

    compatible\_transports = {'amqp', 'redis'}

    election(*id*, *topic*, *action=None*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.election)

    get\_consumers(*channel*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.get_consumers)

    label = 'Gossip'

    name = 'celery.worker.consumer.gossip.Gossip'

    on\_elect(*event*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_elect)

    on\_elect\_ack(*event*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_elect_ack)

    on\_message(*prepare*, *message*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_message)

    on\_node\_join(*worker*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_node_join)

    on\_node\_leave(*worker*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_node_leave)

    on\_node\_lost(*worker*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_node_lost)

    periodic()[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.periodic)

    register\_timer()[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.register_timer)

    requires = (step:celery.worker.consumer.mingle.Mingle{(step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)},)

    start(*c*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.start)