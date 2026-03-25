<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.app.control.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.control.html).

# `celery.app.control`

Worker Remote Control Client.

Client for worker remote control commands.
Server implementation is in [`celery.worker.control`](../internals/reference/celery.worker.control.html#module-celery.worker.control "celery.worker.control").
There are two types of remote control commands:

- Inspect commands: Does not have side effects, will usually just return some value
  found in the worker, like the list of currently registered tasks, the list of active tasks, etc.
  Commands are accessible via [`Inspect`](#celery.app.control.Inspect "celery.app.control.Inspect") class.
- Control commands: Performs side effects, like adding a new queue to consume from.
  Commands are accessible via [`Control`](#celery.app.control.Control "celery.app.control.Control") class.

class celery.app.control.Control(*app=None*)[[source]](../_modules/celery/app/control.html#Control)
:   Worker remote control client.

    class Mailbox(*namespace*, *type='direct'*, *connection=None*, *clock=None*, *accept=None*, *serializer=None*, *producer\_pool=None*, *queue\_ttl=None*, *queue\_expires=None*, *queue\_durable=False*, *queue\_exclusive=False*, *reply\_queue\_ttl=None*, *reply\_queue\_expires=10.0*)
    :   Process Mailbox.

        Node(*hostname=None*, *state=None*, *channel=None*, *handlers=None*)

        abcast(*command*, *kwargs=None*)

        accept = ['json']
        :   Only accepts json messages by default.

        call(*destination*, *command*, *kwargs=None*, *timeout=None*, *callback=None*, *channel=None*)

        cast(*destination*, *command*, *kwargs=None*)

        connection = None
        :   Connection (if bound).

        exchange = None
        :   mailbox exchange (init by constructor).

        exchange\_fmt = '%s.pidbox'

        get\_queue(*hostname*)

        get\_reply\_queue()

        multi\_call(*command*, *kwargs=None*, *timeout=1*, *limit=None*, *callback=None*, *channel=None*)

        namespace = None
        :   Name of application.

        node\_cls
        :   alias of [`Node`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.pidbox.html#kombu.pidbox.Node "(in Kombu v5.6)")

        property oid

        producer\_or\_acquire(*producer=None*, *channel=None*)

        property producer\_pool

        reply\_exchange = None
        :   exchange to send replies to.

        reply\_exchange\_fmt = 'reply.%s.pidbox'

        property reply\_queue

        serializer = None
        :   Message serializer

        type = 'direct'
        :   Exchange type (usually direct, or fanout for broadcast).

    add\_consumer(*queue*, *exchange=None*, *exchange\_type='direct'*, *routing\_key=None*, *options=None*, *destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.add_consumer)
    :   Tell all (or specific) workers to start consuming from a new queue.

        Only the queue name is required as if only the queue is specified
        then the exchange/routing key will be set to the same name (
        like automatic queues do).

        Note

        This command does not respect the default queue/exchange
        options in the configuration.

        Parameters:
        :   - **queue** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of queue to start consuming from.
            - **exchange** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Optional name of exchange.
            - **exchange\_type** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Type of exchange (defaults to ‘direct’)
              command to, when empty broadcast to all workers.
            - **routing\_key** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Optional routing key.
            - **options** (*Dict*) – Additional options as supported
              by `kombu.entity.Queue.from_dict()`.

        See also

        [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast") for supported keyword arguments.

    autoscale(*max*, *min*, *destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.autoscale)
    :   Change worker(s) autoscale setting.

        See also

        Supports the same arguments as [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast").

    broadcast(*command*, *arguments=None*, *destination=None*, *connection=None*, *reply=False*, *timeout=1.0*, *limit=None*, *callback=None*, *channel=None*, *pattern=None*, *matcher=None*, *\*\*extra\_kwargs*)[[source]](../_modules/celery/app/control.html#Control.broadcast)
    :   Broadcast a control command to the celery workers.

        Parameters:
        :   - **command** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of command to send.
            - **arguments** (*Dict*) – Keyword arguments for the command.
            - **destination** (*List*) – If set, a list of the hosts to send the
              command to, when empty broadcast to all workers.
            - **connection** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Custom broker connection to use,
              if not set, a connection will be acquired from the pool.
            - **reply** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Wait for and return the reply.
            - **timeout** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Timeout in seconds to wait for the reply.
            - **limit** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – Limit number of replies.
            - **callback** (*Callable*) – Callback called immediately for
              each reply received.
            - **pattern** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Custom pattern string to match
            - **matcher** (*Callable*) – Custom matcher to run the pattern to match

    cancel\_consumer(*queue*, *destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.cancel_consumer)
    :   Tell all (or specific) workers to stop consuming from `queue`.

        See also

        Supports the same arguments as [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast").

    disable\_events(*destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.disable_events)
    :   Tell all (or specific) workers to disable events.

        See also

        Supports the same arguments as [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast").

    discard\_all(*connection=None*)
    :   Discard all waiting tasks.

        This will ignore all tasks waiting for execution, and they will
        be deleted from the messaging server.

        Parameters:
        :   **connection** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Optional specific connection
            instance to use. If not provided a connection will
            be acquired from the connection pool.

        Returns:
        :   the number of tasks discarded.

        Return type:
        :   [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")

    election(*id*, *topic*, *action=None*, *connection=None*)[[source]](../_modules/celery/app/control.html#Control.election)

    enable\_events(*destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.enable_events)
    :   Tell all (or specific) workers to enable events.

        See also

        Supports the same arguments as [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast").

    heartbeat(*destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.heartbeat)
    :   Tell worker(s) to send a heartbeat immediately.

        See also

        Supports the same arguments as [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast")

    property inspect
    :   Create new [`Inspect`](#celery.app.control.Inspect "celery.app.control.Inspect") instance.

    ping(*destination=None*, *timeout=1.0*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.ping)
    :   Ping all (or specific) workers.

        ```
        >>> app.control.ping()
        [{'celery@node1': {'ok': 'pong'}}, {'celery@node2': {'ok': 'pong'}}]
        >>> app.control.ping(destination=['celery@node2'])
        [{'celery@node2': {'ok': 'pong'}}]
        ```

        Returns:
        :   List of `{HOSTNAME: {'ok': 'pong'}}` dictionaries.

        Return type:
        :   List[Dict]

        See also

        [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast") for supported keyword arguments.

    pool\_grow(*n=1*, *destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.pool_grow)
    :   Tell all (or specific) workers to grow the pool by `n`.

        See also

        Supports the same arguments as [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast").

    pool\_restart(*modules=None*, *reload=False*, *reloader=None*, *destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.pool_restart)
    :   Restart the execution pools of all or specific workers.

        Keyword Arguments:
        :   - **modules** (*Sequence**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – List of modules to reload.
            - **reload** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Flag to enable module reloading. Default is False.
            - **reloader** (*Any*) – Function to reload a module.
            - **destination** (*Sequence**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – List of worker names to send this
              command to.

        See also

        Supports the same arguments as [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast")

    pool\_shrink(*n=1*, *destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.pool_shrink)
    :   Tell all (or specific) workers to shrink the pool by `n`.

        See also

        Supports the same arguments as [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast").

    purge(*connection=None*)[[source]](../_modules/celery/app/control.html#Control.purge)
    :   Discard all waiting tasks.

        This will ignore all tasks waiting for execution, and they will
        be deleted from the messaging server.

        Parameters:
        :   **connection** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Optional specific connection
            instance to use. If not provided a connection will
            be acquired from the connection pool.

        Returns:
        :   the number of tasks discarded.

        Return type:
        :   [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")

    rate\_limit(*task\_name*, *rate\_limit*, *destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.rate_limit)
    :   Tell workers to set a new rate limit for task by type.

        Parameters:
        :   - **task\_name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of task to change rate limit for.
            - **rate\_limit** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – The rate limit as tasks per second,
              or a rate limit string (‘100/m’, etc.
              see [`celery.app.task.Task.rate_limit`](celery.app.task.html#celery.app.task.Task.rate_limit "celery.app.task.Task.rate_limit") for
              more information).

        See also

        [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast") for supported keyword arguments.

    revoke(*task\_id*, *destination=None*, *terminate=False*, *signal='SIGTERM'*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.revoke)
    :   Tell all (or specific) workers to revoke a task by id (or list of ids).

        If a task is revoked, the workers will ignore the task and
        not execute it after all.

        Parameters:
        :   - **task\_id** (*Union**(*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*list*](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")*)*) – Id of the task to revoke
              (or list of ids).
            - **terminate** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Also terminate the process currently working
              on the task (if any).
            - **signal** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of signal to send to process if terminate.
              Default is TERM.

        See also

        [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast") for supported keyword arguments.

    revoke\_by\_stamped\_headers(*headers*, *destination=None*, *terminate=False*, *signal='SIGTERM'*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.revoke_by_stamped_headers)
    :   Tell all (or specific) workers to revoke a task by headers.

        If a task is revoked, the workers will ignore the task and
        not execute it after all.

        Parameters:
        :   - **headers** ([*dict*](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *Union**(*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*list*](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")*)**]*) – Headers to match when revoking tasks.
            - **terminate** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Also terminate the process currently working
              on the task (if any).
            - **signal** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of signal to send to process if terminate.
              Default is TERM.

        See also

        [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast") for supported keyword arguments.

    shutdown(*destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.shutdown)
    :   Shutdown worker(s).

        See also

        Supports the same arguments as [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast")

    terminate(*task\_id*, *destination=None*, *signal='SIGTERM'*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.terminate)
    :   Tell all (or specific) workers to terminate a task by id (or list of ids).

        See also

        This is just a shortcut to [`revoke()`](#celery.app.control.Control.revoke "celery.app.control.Control.revoke") with the terminate
        argument enabled.

    time\_limit(*task\_name*, *soft=None*, *hard=None*, *destination=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/control.html#Control.time_limit)
    :   Tell workers to set time limits for a task by type.

        Parameters:
        :   - **task\_name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of task to change time limits for.
            - **soft** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – New soft time limit (in seconds).
            - **hard** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – New hard time limit (in seconds).
            - **\*\*kwargs** (*Any*) – arguments passed on to [`broadcast()`](#celery.app.control.Control.broadcast "celery.app.control.Control.broadcast").

class celery.app.control.Inspect(*destination=None*, *timeout=1.0*, *callback=None*, *connection=None*, *app=None*, *limit=None*, *pattern=None*, *matcher=None*)[[source]](../_modules/celery/app/control.html#Inspect)
:   API for inspecting workers.

    This class provides proxy for accessing Inspect API of workers. The API is
    defined in [`celery.worker.control`](../internals/reference/celery.worker.control.html#module-celery.worker.control "celery.worker.control")

    active(*safe=None*)[[source]](../_modules/celery/app/control.html#Inspect.active)
    :   Return list of tasks currently executed by workers.

        Parameters:
        :   **safe** (*Boolean*) – Set to True to disable deserialization.

        Returns:
        :   Dictionary `{HOSTNAME: [TASK_INFO,...]}`.

        Return type:
        :   Dict

        See also

        For `TASK_INFO` details see [`query_task()`](#celery.app.control.Inspect.query_task "celery.app.control.Inspect.query_task") return value.

    active\_queues()[[source]](../_modules/celery/app/control.html#Inspect.active_queues)
    :   Return information about queues from which worker consumes tasks.

        Returns:
        :   Dictionary `{HOSTNAME: [QUEUE_INFO, QUEUE_INFO,...]}`.

        Return type:
        :   Dict

        Here is the list of `QUEUE_INFO` fields:

        - `name`
        - `exchange`
          :   - `name`
              - `type`
              - `arguments`
              - `durable`
              - `passive`
              - `auto_delete`
              - `delivery_mode`
              - `no_declare`
        - `routing_key`
        - `queue_arguments`
        - `binding_arguments`
        - `consumer_arguments`
        - `durable`
        - `exclusive`
        - `auto_delete`
        - `no_ack`
        - `alias`
        - `bindings`
        - `no_declare`
        - `expires`
        - `message_ttl`
        - `max_length`
        - `max_length_bytes`
        - `max_priority`

        See also

        See the RabbitMQ/AMQP documentation for more details about
        `queue_info` fields.

        Note

        The `queue_info` fields are RabbitMQ/AMQP oriented.
        Not all fields applies for other transports.

    app = None

    clock()[[source]](../_modules/celery/app/control.html#Inspect.clock)
    :   Get the Clock value on workers.

        ```
        >>> app.control.inspect().clock()
        {'celery@node1': {'clock': 12}}
        ```

        Returns:
        :   Dictionary `{HOSTNAME: CLOCK_VALUE}`.

        Return type:
        :   Dict

    conf(*with\_defaults=False*)[[source]](../_modules/celery/app/control.html#Inspect.conf)
    :   Return configuration of each worker.

        Parameters:
        :   **with\_defaults** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – if set to True, method returns also
            configuration options with default values.

        Returns:
        :   Dictionary `{HOSTNAME: WORKER_CONFIGURATION}`.

        Return type:
        :   Dict

        See also

        `WORKER_CONFIGURATION` is a dictionary containing current configuration options.
        See [Configuration and defaults](../userguide/configuration.html#configuration) for possible values.

    hello(*from\_node*, *revoked=None*)[[source]](../_modules/celery/app/control.html#Inspect.hello)

    memdump(*samples=10*)[[source]](../_modules/celery/app/control.html#Inspect.memdump)
    :   Dump statistics of previous memsample requests.

        Note

        Requires the psutils library.

    memsample()[[source]](../_modules/celery/app/control.html#Inspect.memsample)
    :   Return sample current RSS memory usage.

        Note

        Requires the psutils library.

    objgraph(*type='Request'*, *n=200*, *max\_depth=10*)[[source]](../_modules/celery/app/control.html#Inspect.objgraph)
    :   Create graph of uncollected objects (memory-leak debugging).

        Parameters:
        :   - **n** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – Max number of objects to graph.
            - **max\_depth** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – Traverse at most n levels deep.
            - **type** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of object to graph. Default is `"Request"`.

        Returns:
        :   Dictionary `{'filename': FILENAME}`

        Return type:
        :   Dict

        Note

        Requires the objgraph library.

    ping(*destination=None*)[[source]](../_modules/celery/app/control.html#Inspect.ping)
    :   Ping all (or specific) workers.

        ```
        >>> app.control.inspect().ping()
        {'celery@node1': {'ok': 'pong'}, 'celery@node2': {'ok': 'pong'}}
        >>> app.control.inspect().ping(destination=['celery@node1'])
        {'celery@node1': {'ok': 'pong'}}
        ```

        Parameters:
        :   **destination** (*List*) – If set, a list of the hosts to send the
            command to, when empty broadcast to all workers.

        Returns:
        :   Dictionary `{HOSTNAME: {'ok': 'pong'}}`.

        Return type:
        :   Dict

        See also

        `broadcast()` for supported keyword arguments.

    query\_task(*\*ids*)[[source]](../_modules/celery/app/control.html#Inspect.query_task)
    :   Return detail of tasks currently executed by workers.

        Parameters:
        :   **\*ids** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – IDs of tasks to be queried.

        Returns:
        :   Dictionary `{HOSTNAME: {TASK_ID: [STATE, TASK_INFO]}}`.

        Return type:
        :   Dict

        Here is the list of `TASK_INFO` fields:
        :   - `id` - ID of the task
            - `name` - Name of the task
            - `args` - Positinal arguments passed to the task
            - `kwargs` - Keyword arguments passed to the task
            - `type` - Type of the task
            - `hostname` - Hostname of the worker processing the task
            - `time_start` - Time of processing start
            - `acknowledged` - True when task was acknowledged to broker
            - `delivery_info` - Dictionary containing delivery information
              :   - `exchange` - Name of exchange where task was published
                  - `routing_key` - Routing key used when task was published
                  - `priority` - Priority used when task was published
                  - `redelivered` - True if the task was redelivered
            - `worker_pid` - PID of worker processing the task

    registered(*\*taskinfoitems*)[[source]](../_modules/celery/app/control.html#Inspect.registered)
    :   Return all registered tasks per worker.

        ```
        >>> app.control.inspect().registered()
        {'celery@node1': ['task1', 'task1']}
        >>> app.control.inspect().registered('serializer', 'max_retries')
        {'celery@node1': ['task_foo [serializer=json max_retries=3]', 'tasb_bar [serializer=json max_retries=3]']}
        ```

        Parameters:
        :   **taskinfoitems** (*Sequence**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – List of [`Task`](celery.app.task.html#celery.app.task.Task "celery.app.task.Task")
            attributes to include.

        Returns:
        :   Dictionary `{HOSTNAME: [TASK1_INFO, ...]}`.

        Return type:
        :   Dict

    registered\_tasks(*\*taskinfoitems*)
    :   Return all registered tasks per worker.

        ```
        >>> app.control.inspect().registered()
        {'celery@node1': ['task1', 'task1']}
        >>> app.control.inspect().registered('serializer', 'max_retries')
        {'celery@node1': ['task_foo [serializer=json max_retries=3]', 'tasb_bar [serializer=json max_retries=3]']}
        ```

        Parameters:
        :   **taskinfoitems** (*Sequence**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – List of [`Task`](celery.app.task.html#celery.app.task.Task "celery.app.task.Task")
            attributes to include.

        Returns:
        :   Dictionary `{HOSTNAME: [TASK1_INFO, ...]}`.

        Return type:
        :   Dict

    report()[[source]](../_modules/celery/app/control.html#Inspect.report)
    :   Return human readable report for each worker.

        Returns:
        :   Dictionary `{HOSTNAME: {'ok': REPORT_STRING}}`.

        Return type:
        :   Dict

    reserved(*safe=None*)[[source]](../_modules/celery/app/control.html#Inspect.reserved)
    :   Return list of currently reserved tasks, not including scheduled/active.

        Returns:
        :   Dictionary `{HOSTNAME: [TASK_INFO,...]}`.

        Return type:
        :   Dict

        See also

        For `TASK_INFO` details see [`query_task()`](#celery.app.control.Inspect.query_task "celery.app.control.Inspect.query_task") return value.

    revoked()[[source]](../_modules/celery/app/control.html#Inspect.revoked)
    :   Return list of revoked tasks.

        ```
        >>> app.control.inspect().revoked()
        {'celery@node1': ['16f527de-1c72-47a6-b477-c472b92fef7a']}
        ```

        Returns:
        :   Dictionary `{HOSTNAME: [TASK_ID, ...]}`.

        Return type:
        :   Dict

    scheduled(*safe=None*)[[source]](../_modules/celery/app/control.html#Inspect.scheduled)
    :   Return list of scheduled tasks with details.

        Returns:
        :   Dictionary `{HOSTNAME: [TASK_SCHEDULED_INFO,...]}`.

        Return type:
        :   Dict

        Here is the list of `TASK_SCHEDULED_INFO` fields:

        - `eta` - scheduled time for task execution as string in ISO 8601 format
        - `priority` - priority of the task
        - `request` - field containing `TASK_INFO` value.

        See also

        For more details about `TASK_INFO` see [`query_task()`](#celery.app.control.Inspect.query_task "celery.app.control.Inspect.query_task") return value.

    stats()[[source]](../_modules/celery/app/control.html#Inspect.stats)
    :   Return statistics of worker.

        Returns:
        :   Dictionary `{HOSTNAME: STAT_INFO}`.

        Return type:
        :   Dict

        Here is the list of `STAT_INFO` fields:

        - `broker` - Section for broker information.
          :   - `connect_timeout` - Timeout in seconds (int/float) for establishing a new connection.
              - `heartbeat` - Current heartbeat value (set by client).
              - `hostname` - Node name of the remote broker.
              - `insist` - No longer used.
              - `login_method` - Login method used to connect to the broker.
              - `port` - Port of the remote broker.
              - `ssl` - SSL enabled/disabled.
              - `transport` - Name of transport used (e.g., amqp or redis)
              - `transport_options` - Options passed to transport.
              - `uri_prefix` - Some transports expects the host name to be a URL.
                E.g. `redis+socket:///tmp/redis.sock`.
                In this example the URI-prefix will be redis.
              - `userid` - User id used to connect to the broker with.
              - `virtual_host` - Virtual host used.
        - `clock` - Value of the workers logical clock. This is a positive integer
          and should be increasing every time you receive statistics.
        - `uptime` - Numbers of seconds since the worker controller was started
        - `pid` - Process id of the worker instance (Main process).
        - `pool` - Pool-specific section.
          :   - `max-concurrency` - Max number of processes/threads/green threads.
              - `max-tasks-per-child` - Max number of tasks a thread may execute before being recycled.
              - `processes` - List of PIDs (or thread-id’s).
              - `put-guarded-by-semaphore` - Internal
              - `timeouts` - Default values for time limits.
              - `writes` - Specific to the prefork pool, this shows the distribution
                of writes to each process in the pool when using async I/O.
        - `prefetch_count` - Current prefetch count value for the task consumer.
        - `rusage` - System usage statistics. The fields available may be different on your platform.
          From *getrusage(2)*:

          > - `stime` - Time spent in operating system code on behalf of this process.
          > - `utime` - Time spent executing user instructions.
          > - `maxrss` - The maximum resident size used by this process (in kilobytes).
          > - `idrss` - Amount of non-shared memory used for data (in kilobytes times
          >   ticks of execution)
          > - `isrss` - Amount of non-shared memory used for stack space
          >   (in kilobytes times ticks of execution)
          > - `ixrss` - Amount of memory shared with other processes
          >   (in kilobytes times ticks of execution).
          > - `inblock` - Number of times the file system had to read from the disk
          >   on behalf of this process.
          > - `oublock` - Number of times the file system has to write to disk
          >   on behalf of this process.
          > - `majflt` - Number of page faults that were serviced by doing I/O.
          > - `minflt` - Number of page faults that were serviced without doing I/O.
          > - `msgrcv` - Number of IPC messages received.
          > - `msgsnd` - Number of IPC messages sent.
          > - `nvcsw` - Number of times this process voluntarily invoked a context switch.
          > - `nivcsw` - Number of times an involuntary context switch took place.
          > - `nsignals` - Number of signals received.
          > - `nswap` - The number of times this process was swapped entirely
          >   out of memory.
        - `total` - Map of task names and the total number of tasks with that type
          the worker has accepted since start-up.

celery.app.control.flatten\_reply(*reply*)[[source]](../_modules/celery/app/control.html#flatten_reply)
:   Flatten node replies.

    Convert from a list of replies in this format:

    ```
    [{'a@example.com': reply},
     {'b@example.com': reply}]
    ```

    into this format:

    ```
    {'a@example.com': reply,
     'b@example.com': reply}
    ```