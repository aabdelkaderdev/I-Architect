<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.events.event.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.events.event.html).

# `celery.events.event`

Creating events, and event exchange definition.

celery.events.event.Event(*type*, *\_fields=None*, *\_\_dict\_\_=<class 'dict'>*, *\_\_now\_\_=<built-in function time>*, *\*\*fields*)[[source]](../_modules/celery/events/event.html#Event)
:   Create an event.

    Notes

    An event is simply a dictionary: the only required field is `type`.
    A `timestamp` field will be set to the current time if not provided.

celery.events.event.event\_exchange = <unbound Exchange celeryev(topic)>
:   Exchange used to send events on.
    Note: Use [`get_exchange()`](#celery.events.event.get_exchange "celery.events.event.get_exchange") instead, as the type of
    exchange will vary depending on the broker connection.

celery.events.event.get\_exchange(*conn*, *name='celeryev'*)[[source]](../_modules/celery/events/event.html#get_exchange)
:   Get exchange used for sending events.

    Parameters:
    :   - **conn** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Connection used for sending/receiving events.
        - **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of the exchange. Default is `celeryev`.

    Note

    The event type changes if Redis is used as the transport
    (from topic -> fanout).

celery.events.event.group\_from(*type*)[[source]](../_modules/celery/events/event.html#group_from)
:   Get the group part of an event type name.

    Example

    ```
    >>> group_from('task-sent')
    'task'
    ```

    ```
    >>> group_from('custom-my-event')
    'custom'
    ```