<!-- Source: https://docs.celeryq.dev/en/main/internals/worker.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/worker.html).

# Internals: The worker

## 

The worker consists of 4 main components: the consumer, the scheduler,
the mediator and the task pool. All these components runs in parallel working
with two data structures: the ready queue and the ETA schedule.

## 

### 

The timer uses [`heapq`](https://docs.python.org/dev/library/heapq.html#module-heapq "(in Python v3.15)") to schedule internal functions.
It’s very efficient and can handle hundred of thousands of entries.

## 

### 

Receives messages from the broker using <https://pypi.org/project/Kombu/>.

When a message is received it’s converted into a
[`celery.worker.request.Request`](../reference/celery.worker.request.html#celery.worker.request.Request "celery.worker.request.Request") object.

Tasks with an ETA, or rate-limit are entered into the timer,
messages that can be immediately processed are sent to the execution pool.

ETA and rate-limit when used together will result in the rate limit being
observed with the task being scheduled after the ETA.

### 

The timer schedules internal functions, like cleanup and internal monitoring,
but also it schedules ETA tasks and rate limited tasks.
If the scheduled tasks ETA has passed it is moved to the execution pool.

### 

This is a slightly modified `multiprocessing.Pool`.
It mostly works the same way, except it makes sure all of the workers
are running at all times. If a worker is missing, it replaces
it with a new one.