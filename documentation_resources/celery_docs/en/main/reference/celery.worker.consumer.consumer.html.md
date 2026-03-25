<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.consumer.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.consumer.html).

# `celery.worker.consumer.consumer`

Worker Consumer Blueprint.

This module contains the components responsible for consuming messages
from the broker, processing the messages and keeping the broker connections
up and running.

class celery.worker.consumer.consumer.Consumer(*on\_task\_request*, *init\_callback=<function noop>*, *hostname=None*, *pool=None*, *app=None*, *timer=None*, *controller=None*, *hub=None*, *amqheartbeat=None*, *worker\_options=None*, *disable\_rate\_limits=False*, *initial\_prefetch\_count=2*, *prefetch\_multiplier=1*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer)
:   Consumer blueprint.

    class Blueprint(*steps=None*, *name=None*, *on\_start=None*, *on\_close=None*, *on\_stopped=None*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.Blueprint)
    :   Consumer blueprint.

        default\_steps = ['celery.worker.consumer.connection:Connection', 'celery.worker.consumer.mingle:Mingle', 'celery.worker.consumer.events:Events', 'celery.worker.consumer.gossip:Gossip', 'celery.worker.consumer.heart:Heart', 'celery.worker.consumer.control:Control', 'celery.worker.consumer.tasks:Tasks', 'celery.worker.consumer.delayed\_delivery:DelayedDelivery', 'celery.worker.consumer.consumer:Evloop', 'celery.worker.consumer.agent:Agent']

        name = 'Consumer'

        shutdown(*parent*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.Blueprint.shutdown)

    Strategies
    :   alias of [`dict`](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

    add\_task\_queue(*queue*, *exchange=None*, *exchange\_type=None*, *routing\_key=None*, *\*\*options*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.add_task_queue)

    apply\_eta\_task(*task*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.apply_eta_task)
    :   Method called by the timer to apply a task with an ETA/countdown.

    broker\_connection\_retry\_attempt = 0
    :   Counter to track number of conn retry attempts
        to broker. Will be reset to 0 once successful

    bucket\_for\_task(*type*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.bucket_for_task)

    call\_soon(*p*, *\*args*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.call_soon)

    cancel\_active\_requests()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.cancel_active_requests)
    :   Cancel active requests during shutdown.

        Cancels all active requests that either do not require late acknowledgments or,
        if they do, have not been acknowledged yet.

        Does not cancel successful tasks, even if they have not been acknowledged yet.

    cancel\_task\_queue(*queue*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.cancel_task_queue)

    connect()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.connect)
    :   Establish the broker connection used for consuming tasks.

        Retries establishing the connection if the
        [`broker_connection_retry`](../userguide/configuration.html#std-setting-broker_connection_retry) setting is enabled

    connection\_for\_read(*heartbeat=None*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.connection_for_read)

    connection\_for\_write(*url=None*, *heartbeat=None*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.connection_for_write)

    create\_task\_handler(*promise=<class 'vine.promises.promise'>*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.create_task_handler)

    ensure\_connected(*conn*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.ensure_connected)

    first\_connection\_attempt = True
    :   This flag will be turned off after the first failed
        connection attempt.

    init\_callback = None
    :   Optional callback called the first time the worker
        is ready to receive tasks.

    loop\_args()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.loop_args)

    property max\_prefetch\_count

    on\_close()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.on_close)

    on\_connection\_error\_after\_connected(*exc*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.on_connection_error_after_connected)

    on\_connection\_error\_before\_connected(*exc*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.on_connection_error_before_connected)

    on\_decode\_error(*message*, *exc*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.on_decode_error)
    :   Callback called if an error occurs while decoding a message.

        Simply logs the error and acknowledges the message so it
        doesn’t enter a loop.

        Parameters:
        :   - **message** (*kombu.Message*) – The message received.
            - **exc** ([*Exception*](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)")) – The exception being handled.

    on\_invalid\_task(*body*, *message*, *exc*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.on_invalid_task)

    on\_ready()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.on_ready)

    on\_send\_event\_buffered()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.on_send_event_buffered)

    on\_unknown\_message(*body*, *message*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.on_unknown_message)

    on\_unknown\_task(*body*, *message*, *exc*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.on_unknown_task)

    perform\_pending\_operations()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.perform_pending_operations)

    pool = None
    :   The current worker pool instance.

    register\_with\_event\_loop(*hub*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.register_with_event_loop)

    reset\_rate\_limits()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.reset_rate_limits)

    restart\_count = -1

    shutdown()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.shutdown)

    start()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.start)

    stop()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.stop)

    timer = None
    :   A timer used for high-priority internal tasks, such
        as sending heartbeats.

    update\_strategies()[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer.update_strategies)

class celery.worker.consumer.consumer.Evloop(*parent*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/consumer.html#Evloop)
:   Event loop service.

    Note

    This is always started last.

    label = 'event loop'

    last = True

    name = 'celery.worker.consumer.consumer.Evloop'

    patch\_all(*c*)[[source]](../_modules/celery/worker/consumer/consumer.html#Evloop.patch_all)

    start(*c*)[[source]](../_modules/celery/worker/consumer/consumer.html#Evloop.start)

celery.worker.consumer.consumer.dump\_body(*m*, *body*)[[source]](../_modules/celery/worker/consumer/consumer.html#dump_body)
:   Format message body for debugging purposes.