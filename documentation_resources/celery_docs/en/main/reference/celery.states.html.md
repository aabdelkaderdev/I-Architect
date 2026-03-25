<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.states.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.states.html).

Built-in task states.

# 

See [States](../userguide/tasks.html#task-states).

# 

## 

Set of states meaning the task result is ready (has been executed).

## 

Set of states meaning the task result is not ready (hasn’t been executed).

## 

Set of states meaning the task returned an exception.

## 

Set of exception states that should propagate exceptions to the user.

## 

Set of all possible states.

#

celery.states.FAILURE = 'FAILURE'
:   Task failed

celery.states.PENDING = 'PENDING'
:   Task state is unknown (assumed pending since you know the id).

celery.states.RECEIVED = 'RECEIVED'
:   Task was received by a worker (only used in events).

celery.states.RETRY = 'RETRY'
:   Task is waiting for retry.

celery.states.REVOKED = 'REVOKED'
:   Task was revoked.

celery.states.STARTED = 'STARTED'
:   Task was started by a worker ([`task_track_started`](../userguide/configuration.html#std-setting-task_track_started)).

celery.states.SUCCESS = 'SUCCESS'
:   Task succeeded

celery.states.precedence(*state: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")[[source]](../_modules/celery/states.html#precedence)
:   Get the precedence index for state.

    Lower index means higher precedence.

class celery.states.state[[source]](../_modules/celery/states.html#state)
:   Task state.

    State is a subclass of [`str`](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), implementing comparison
    methods adhering to state precedence rules:

    ```
    >>> from celery.states import state, PENDING, SUCCESS

    >>> state(PENDING) < state(SUCCESS)
    True
    ```

    Any custom state is considered to be lower than [`FAILURE`](../userguide/tasks.html#std-state-FAILURE) and
    [`SUCCESS`](../userguide/tasks.html#std-state-SUCCESS), but higher than any of the other built-in states:

    ```
    >>> state('PROGRESS') > state(STARTED)
    True

    >>> state('PROGRESS') > state('SUCCESS')
    False
    ```