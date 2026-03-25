<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.events.state.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.events.state.html).

# `celery.events.state`

In-memory representation of cluster state.

This module implements a data-structure used to keep
track of the state of a cluster of workers and the tasks
it is working on (by consuming events).

For every event consumed the state is updated,
so the state represents the state of the cluster
at the time of the last event.

Snapshots ([`celery.events.snapshot`](../internals/reference/celery.events.snapshot.html#module-celery.events.snapshot "celery.events.snapshot")) can be used to
take “pictures” of this state at regular intervals
to for example, store that in a database.

class celery.events.state.State(*callback=None*, *workers=None*, *tasks=None*, *taskheap=None*, *max\_workers\_in\_memory=5000*, *max\_tasks\_in\_memory=10000*, *on\_node\_join=None*, *on\_node\_leave=None*, *tasks\_by\_type=None*, *tasks\_by\_worker=None*)[[source]](../_modules/celery/events/state.html#State)
:   Records clusters state.

    class Task(*uuid=None*, *cluster\_state=None*, *children=None*, *\*\*kwargs*)
    :   Task State.

        args = None

        as\_dict()

        client = None

        clock = 0

        eta = None

        event(*type\_*, *timestamp=None*, *local\_received=None*, *fields=None*, *precedence=<function precedence>*, *setattr=<built-in function setattr>*, *task\_event\_to\_state=<built-in method get of dict object>*, *RETRY='RETRY'*)

        exception = None

        exchange = None

        expires = None

        failed = None

        property id

        info(*fields=None*, *extra=None*)
        :   Information about this task suitable for on-screen display.

        kwargs = None

        merge\_rules = {'RECEIVED': ('name', 'args', 'kwargs', 'parent\_id', 'root\_id', 'retries', 'eta', 'expires')}
        :   How to merge out of order events.
            Disorder is detected by logical ordering (e.g., [`task-received`](../userguide/monitoring.html#std-event-task-received)
            must’ve happened before a [`task-failed`](../userguide/monitoring.html#std-event-task-failed) event).

            A merge rule consists of a state and a list of fields to keep from
            that state. `(RECEIVED, ('name', 'args')`, means the name and args
            fields are always taken from the RECEIVED state, and any values for
            these fields received before or after is simply ignored.

        name = None

        property origin

        property parent

        parent\_id = None

        property ready

        received = None

        rejected = None

        result = None

        retried = None

        retries = None

        revoked = None

        property root

        root\_id = None

        routing\_key = None

        runtime = None

        sent = None

        started = None

        state = 'PENDING'

        succeeded = None

        timestamp = None

        traceback = None

        worker = None

    class Worker(*hostname=None*, *pid=None*, *freq=60*, *heartbeats=None*, *clock=0*, *active=None*, *processed=None*, *loadavg=None*, *sw\_ident=None*, *sw\_ver=None*, *sw\_sys=None*)
    :   Worker State.

        active

        property alive

        clock

        event

        expire\_window = 200

        freq

        property heartbeat\_expires

        heartbeat\_max = 4

        heartbeats

        hostname

        property id

        loadavg

        pid

        processed

        property status\_string

        sw\_ident

        sw\_sys

        sw\_ver

        update(*f*, *\*\*kw*)

    alive\_workers()[[source]](../_modules/celery/events/state.html#State.alive_workers)
    :   Return a list of (seemingly) alive workers.

    clear(*ready: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*)[[source]](../_modules/celery/events/state.html#State.clear)

    clear\_tasks(*ready=True*)[[source]](../_modules/celery/events/state.html#State.clear_tasks)

    event(*event*)[[source]](../_modules/celery/events/state.html#State.event)

    event\_count = 0

    freeze\_while(*fun*, *\*args*, *\*\*kwargs*)[[source]](../_modules/celery/events/state.html#State.freeze_while)

    get\_or\_create\_task(*uuid*)[[source]](../_modules/celery/events/state.html#State.get_or_create_task)
    :   Get or create task by uuid.

    get\_or\_create\_worker(*hostname*, *\*\*kwargs*)[[source]](../_modules/celery/events/state.html#State.get_or_create_worker)
    :   Get or create worker by hostname.

        Returns:
        :   of `(worker, was_created)` pairs.

        Return type:
        :   Tuple

    heap\_multiplier = 4

    itertasks(*limit: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*)[[source]](../_modules/celery/events/state.html#State.itertasks)

    rebuild\_taskheap(*timetuple=<class 'kombu.clocks.timetuple'>*)[[source]](../_modules/celery/events/state.html#State.rebuild_taskheap)

    task\_count = 0

    task\_event(*type\_*, *fields*)[[source]](../_modules/celery/events/state.html#State.task_event)
    :   Deprecated, use [`event()`](#celery.events.state.State.event "celery.events.state.State.event").

    task\_types()[[source]](../_modules/celery/events/state.html#State.task_types)
    :   Return a list of all seen task types.

    tasks\_by\_time(*limit=None*, *reverse: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*)[[source]](../_modules/celery/events/state.html#State.tasks_by_time)
    :   Generator yielding tasks ordered by time.

        Yields:
        :   Tuples of `(uuid, Task)`.

    tasks\_by\_timestamp(*limit=None*, *reverse: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*)
    :   Generator yielding tasks ordered by time.

        Yields:
        :   Tuples of `(uuid, Task)`.

    worker\_event(*type\_*, *fields*)[[source]](../_modules/celery/events/state.html#State.worker_event)
    :   Deprecated, use [`event()`](#celery.events.state.State.event "celery.events.state.State.event").

class celery.events.state.Task(*uuid=None*, *cluster\_state=None*, *children=None*, *\*\*kwargs*)[[source]](../_modules/celery/events/state.html#Task)
:   Task State.

    args = None

    as\_dict()[[source]](../_modules/celery/events/state.html#Task.as_dict)

    client = None

    clock = 0

    eta = None

    event(*type\_*, *timestamp=None*, *local\_received=None*, *fields=None*, *precedence=<function precedence>*, *setattr=<built-in function setattr>*, *task\_event\_to\_state=<built-in method get of dict object>*, *RETRY='RETRY'*)[[source]](../_modules/celery/events/state.html#Task.event)

    exception = None

    exchange = None

    expires = None

    failed = None

    property id

    info(*fields=None*, *extra=None*)[[source]](../_modules/celery/events/state.html#Task.info)
    :   Information about this task suitable for on-screen display.

    kwargs = None

    merge\_rules = {'RECEIVED': ('name', 'args', 'kwargs', 'parent\_id', 'root\_id', 'retries', 'eta', 'expires')}
    :   How to merge out of order events.
        Disorder is detected by logical ordering (e.g., [`task-received`](../userguide/monitoring.html#std-event-task-received)
        must’ve happened before a [`task-failed`](../userguide/monitoring.html#std-event-task-failed) event).

        A merge rule consists of a state and a list of fields to keep from
        that state. `(RECEIVED, ('name', 'args')`, means the name and args
        fields are always taken from the RECEIVED state, and any values for
        these fields received before or after is simply ignored.

    name = None

    property origin

    property parent

    parent\_id = None

    property ready

    received = None

    rejected = None

    result = None

    retried = None

    retries = None

    revoked = None

    property root

    root\_id = None

    routing\_key = None

    runtime = None

    sent = None

    started = None

    state = 'PENDING'

    succeeded = None

    timestamp = None

    traceback = None

    worker = None

class celery.events.state.Worker(*hostname=None*, *pid=None*, *freq=60*, *heartbeats=None*, *clock=0*, *active=None*, *processed=None*, *loadavg=None*, *sw\_ident=None*, *sw\_ver=None*, *sw\_sys=None*)[[source]](../_modules/celery/events/state.html#Worker)
:   Worker State.

    active

    property alive

    clock

    event

    expire\_window = 200

    freq

    property heartbeat\_expires

    heartbeat\_max = 4

    heartbeats

    hostname

    property id

    loadavg

    pid

    processed

    property status\_string

    sw\_ident

    sw\_sys

    sw\_ver

    update(*f*, *\*\*kw*)[[source]](../_modules/celery/events/state.html#Worker.update)

celery.events.state.heartbeat\_expires(*timestamp*, *freq=60*, *expire\_window=200*, *Decimal=<class 'decimal.Decimal'>*, *float=<class 'float'>*, *isinstance=<built-in function isinstance>*)[[source]](../_modules/celery/events/state.html#heartbeat_expires)
:   Return time when heartbeat expires.