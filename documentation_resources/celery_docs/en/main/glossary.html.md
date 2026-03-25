<!-- Source: https://docs.celeryq.dev/en/main/glossary.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/glossary.html).

# Glossary

ack
:   Short for [acknowledged](#term-acknowledged).

acknowledged
:   Workers acknowledge messages to signify that a message has been
    handled. Failing to acknowledge a message
    will cause the message to be redelivered. Exactly when a
    transaction is considered a failure varies by transport. In AMQP the
    transaction fails when the connection/channel is closed (or lost),
    but in Redis/SQS the transaction times out after a configurable amount
    of time (the `visibility_timeout`).

apply
:   Originally a synonym to [call](#term-calling) but used to signify
    that a function is executed by the current process.

billiard
:   Fork of the Python multiprocessing library containing improvements
    required by Celery.

calling
:   Sends a task message so that the task function is
    [executed](#term-executing) by a worker.

cipater
:   Celery release 3.1 named after song by Autechre
    (<http://www.youtube.com/watch?v=OHsaqUr_33Y>)

context
:   The context of a task contains information like the id of the task,
    it’s arguments and what queue it was delivered to.
    It can be accessed as the tasks `request` attribute.
    See [Task Request](userguide/tasks.html#task-request-info)

early ack
:   Short for [early acknowledgment](#term-early-acknowledgment)

early acknowledgment
:   Task is [acknowledged](#term-acknowledged) just-in-time before being executed,
    meaning the task won’t be redelivered to another worker if the
    machine loses power, or the worker instance is abruptly killed,
    mid-execution.

    Configured using [`task_acks_late`](userguide/configuration.html#std-setting-task_acks_late).

ETA
:   “Estimated Time of Arrival”, in Celery and Google Task Queue, etc.,
    used as the term for a delayed message that should not be processed
    until the specified ETA time. See [ETA and Countdown](userguide/calling.html#calling-eta).

executing
:   Workers *execute* task [requests](#term-request).

idempotent
:   Idempotence is a mathematical property that describes a function that
    can be called multiple times without changing the result.
    Practically it means that a function can be repeated many times without
    unintended effects, but not necessarily side-effect free in the pure
    sense (compare to [nullipotent](#term-nullipotent)).

    Further reading: <https://en.wikipedia.org/wiki/Idempotent>

kombu
:   Python messaging library used by Celery to send and receive messages.

late ack
:   Short for [late acknowledgment](#term-late-acknowledgment)

late acknowledgment
:   Task is [acknowledged](#term-acknowledged) after execution (both if successful, or
    if the task is raising an error), which means the task will be
    redelivered to another worker in the event of the machine losing
    power, or the worker instance being killed mid-execution.

    Configured using [`task_acks_late`](userguide/configuration.html#std-setting-task_acks_late).

nullipotent
:   describes a function that’ll have the same effect, and give the same
    result, even if called zero or multiple times (side-effect free).
    A stronger version of [idempotent](#term-idempotent).

pidbox
:   A process mailbox, used to implement remote control commands.

prefetch count
:   Maximum number of unacknowledged messages a consumer can hold and if
    exceeded the transport shouldn’t deliver any more messages to that
    consumer. See [Prefetch Limits](userguide/optimizing.html#optimizing-prefetch-limit).

prefetch multiplier
:   The [prefetch count](#term-prefetch-count) is configured by using the
    [`worker_prefetch_multiplier`](userguide/configuration.html#std-setting-worker_prefetch_multiplier) setting, which is multiplied
    by the number of pool slots (threads/processes/greenthreads).

    Note

    If you are using eta or countdown tasks, the [`worker_prefetch_multiplier`](userguide/configuration.html#std-setting-worker_prefetch_multiplier)
    still determines the base prefetch count. The [`worker_eta_task_limit`](userguide/configuration.html#std-setting-worker_eta_task_limit)
    setting, when enabled, instead caps the total number of unacknowledged
    messages the worker will hold (including eta/countdown tasks). See
    [`worker_eta_task_limit`](userguide/configuration.html#std-setting-worker_eta_task_limit).

reentrant
:   describes a function that can be interrupted in the middle of
    execution (e.g., by hardware interrupt or signal), and then safely
    called again later. Reentrancy isn’t the same as
    [idempotence](#term-idempotent) as the return value doesn’t have to
    be the same given the same inputs, and a reentrant function may have
    side effects as long as it can be interrupted; An idempotent function
    is always reentrant, but the reverse may not be true.

request
:   Task messages are converted to *requests* within the worker.
    The request information is also available as the task’s
    [context](#term-context) (the `task.request` attribute).