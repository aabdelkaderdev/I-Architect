<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.html).

# `celery.worker.consumer`

Worker consumer.

class celery.worker.consumer.Agent(*c*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/agent.html#Agent)
:   Agent starts <https://pypi.org/project/cell/> actors.

    conditional = True

    create(*c*)[[source]](../_modules/celery/worker/consumer/agent.html#Agent.create)
    :   Create the step.

    name = 'celery.worker.consumer.agent.Agent'

    requires = (step:celery.worker.consumer.connection.Connection{()},)

class celery.worker.consumer.Connection(*c*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/connection.html#Connection)
:   Service managing the consumer broker connection.

    info(*c*)[[source]](../_modules/celery/worker/consumer/connection.html#Connection.info)

    name = 'celery.worker.consumer.connection.Connection'

    shutdown(*c*)[[source]](../_modules/celery/worker/consumer/connection.html#Connection.shutdown)

    start(*c*)[[source]](../_modules/celery/worker/consumer/connection.html#Connection.start)

class celery.worker.consumer.Consumer(*on\_task\_request*, *init\_callback=<function noop>*, *hostname=None*, *pool=None*, *app=None*, *timer=None*, *controller=None*, *hub=None*, *amqheartbeat=None*, *worker\_options=None*, *disable\_rate\_limits=False*, *initial\_prefetch\_count=2*, *prefetch\_multiplier=1*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/consumer.html#Consumer)
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

class celery.worker.consumer.Control(*c*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/control.html#Control)
:   Remote control command service.

    include\_if(*c*)[[source]](../_modules/celery/worker/consumer/control.html#Control.include_if)
    :   Return true if bootstep should be included.

        You can define this as an optional predicate that decides whether
        this step should be created.

    name = 'celery.worker.consumer.control.Control'

    requires = (step:celery.worker.consumer.tasks.Tasks{(step:celery.worker.consumer.mingle.Mingle{(step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)},)},)

class celery.worker.consumer.Events(*c*, *task\_events=True*, *without\_heartbeat=False*, *without\_gossip=False*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/events.html#Events)
:   Service used for sending monitoring events.

    name = 'celery.worker.consumer.events.Events'

    requires = (step:celery.worker.consumer.connection.Connection{()},)

    shutdown(*c*)[[source]](../_modules/celery/worker/consumer/events.html#Events.shutdown)

    start(*c*)[[source]](../_modules/celery/worker/consumer/events.html#Events.start)

    stop(*c*)[[source]](../_modules/celery/worker/consumer/events.html#Events.stop)

class celery.worker.consumer.Gossip(*c*, *without\_gossip=False*, *interval=5.0*, *heartbeat\_interval=2.0*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip)
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

class celery.worker.consumer.Heart(*c*, *without\_heartbeat=False*, *heartbeat\_interval=None*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/heart.html#Heart)
:   Bootstep sending event heartbeats.

    This service sends a `worker-heartbeat` message every n seconds.

    Note

    Not to be confused with AMQP protocol level heartbeats.

    name = 'celery.worker.consumer.heart.Heart'

    requires = (step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)

    shutdown(*c*)

    start(*c*)[[source]](../_modules/celery/worker/consumer/heart.html#Heart.start)

    stop(*c*)[[source]](../_modules/celery/worker/consumer/heart.html#Heart.stop)

class celery.worker.consumer.Mingle(*c*, *without\_mingle=False*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle)
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

class celery.worker.consumer.Tasks(*c*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks)
:   Bootstep starting the task message consumer.

    info(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.info)
    :   Return task consumer info.

    name = 'celery.worker.consumer.tasks.Tasks'

    qos\_global(*c*) → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.qos_global)
    :   Determine if global QoS should be applied.

        Additional information:
        :   <https://www.rabbitmq.com/docs/consumer-prefetch>
            <https://www.rabbitmq.com/docs/quorum-queues#global-qos>

    requires = (step:celery.worker.consumer.mingle.Mingle{(step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)},)

    shutdown(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.shutdown)
    :   Shutdown task consumer.

    start(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.start)
    :   Start task consumer.

    stop(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.stop)
    :   Stop task consumer.