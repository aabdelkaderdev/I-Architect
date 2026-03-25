<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.events.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.events.html).

# `celery.events`

Monitoring Event Receiver+Dispatcher.

Events is a stream of messages sent for certain actions occurring
in the worker (and clients if [`task_send_sent_event`](../userguide/configuration.html#std-setting-task_send_sent_event)
is enabled), used for monitoring purposes.

celery.events.Event(*type*, *\_fields=None*, *\_\_dict\_\_=<class 'dict'>*, *\_\_now\_\_=<built-in function time>*, *\*\*fields*)[[source]](../_modules/celery/events/event.html#Event)
:   Create an event.

    Notes

    An event is simply a dictionary: the only required field is `type`.
    A `timestamp` field will be set to the current time if not provided.

class celery.events.EventDispatcher(*connection=None*, *hostname=None*, *enabled=True*, *channel=None*, *buffer\_while\_offline=True*, *app=None*, *serializer=None*, *groups=None*, *delivery\_mode=1*, *buffer\_group=None*, *buffer\_limit=24*, *on\_send\_buffered=None*)[[source]](../_modules/celery/events/dispatcher.html#EventDispatcher)
:   Dispatches event messages.

    Parameters:
    :   - **connection** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Connection to the broker.
        - **hostname** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Hostname to identify ourselves as,
          by default uses the hostname returned by
          `anon_nodename()`.
        - **groups** (*Sequence**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – List of groups to send events for.
          [`send()`](#celery.events.EventDispatcher.send "celery.events.EventDispatcher.send") will ignore send requests to groups not in this list.
          If this is `None`, all events will be sent.
          Example groups include `"task"` and `"worker"`.
        - **enabled** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Set to `False` to not actually publish any
          events, making [`send()`](#celery.events.EventDispatcher.send "celery.events.EventDispatcher.send") a no-op.
        - **channel** (*kombu.Channel*) – Can be used instead of connection to specify
          an exact channel to use when sending events.
        - **buffer\_while\_offline** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If enabled events will be buffered
          while the connection is down. [`flush()`](#celery.events.EventDispatcher.flush "celery.events.EventDispatcher.flush") must be called
          as soon as the connection is re-established.

    Note

    You need to [`close()`](#celery.events.EventDispatcher.close "celery.events.EventDispatcher.close") this after use.

    DISABLED\_TRANSPORTS = {'sql'}

    app = None

    close()[[source]](../_modules/celery/events/dispatcher.html#EventDispatcher.close)
    :   Close the event dispatcher.

    disable()[[source]](../_modules/celery/events/dispatcher.html#EventDispatcher.disable)

    enable()[[source]](../_modules/celery/events/dispatcher.html#EventDispatcher.enable)

    extend\_buffer(*other*)[[source]](../_modules/celery/events/dispatcher.html#EventDispatcher.extend_buffer)
    :   Copy the outbound buffer of another instance.

    flush(*errors=True*, *groups=True*)[[source]](../_modules/celery/events/dispatcher.html#EventDispatcher.flush)
    :   Flush the outbound buffer.

    on\_disabled = None

    on\_enabled = None

    publish(*type*, *fields*, *producer*, *blind=False*, *Event=<function Event>*, *\*\*kwargs*)[[source]](../_modules/celery/events/dispatcher.html#EventDispatcher.publish)
    :   Publish event using custom [`Producer`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Producer "(in Kombu v5.6)").

        Parameters:
        :   - **type** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Event type name, with group separated by dash (-).
              fields: Dictionary of event fields, must be json serializable.
            - **producer** ([*kombu.Producer*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Producer "(in Kombu v5.6)")) – Producer instance to use:
              only the `publish` method will be called.
            - **retry** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Retry in the event of connection failure.
            - **retry\_policy** (*Mapping*) – Map of custom retry policy options.
              See [`ensure()`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection.ensure "(in Kombu v5.6)").
            - **blind** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Don’t set logical clock value (also don’t forward
              the internal logical clock).
            - **Event** (*Callable*) – Event type used to create event.
              Defaults to [`Event()`](#celery.events.Event "celery.events.Event").
            - **utcoffset** (*Callable*) – Function returning the current
              utc offset in hours.

    property publisher

    send(*type*, *blind=False*, *utcoffset=<function utcoffset>*, *retry=False*, *retry\_policy=None*, *Event=<function Event>*, *\*\*fields*)[[source]](../_modules/celery/events/dispatcher.html#EventDispatcher.send)
    :   Send event.

        Parameters:
        :   - **type** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Event type name, with group separated by dash (-).
            - **retry** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Retry in the event of connection failure.
            - **retry\_policy** (*Mapping*) – Map of custom retry policy options.
              See [`ensure()`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection.ensure "(in Kombu v5.6)").
            - **blind** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Don’t set logical clock value (also don’t forward
              the internal logical clock).
            - **Event** (*Callable*) – Event type used to create event,
              defaults to [`Event()`](#celery.events.Event "celery.events.Event").
            - **utcoffset** (*Callable*) – unction returning the current utc offset
              in hours.
            - **\*\*fields** (*Any*) – Event fields – must be json serializable.

class celery.events.EventReceiver(*channel*, *handlers=None*, *routing\_key='#'*, *node\_id=None*, *app=None*, *queue\_prefix=None*, *accept=None*, *queue\_ttl=None*, *queue\_expires=None*, *queue\_exclusive=None*, *queue\_durable=None*)[[source]](../_modules/celery/events/receiver.html#EventReceiver)
:   Capture events.

    Parameters:
    :   - **connection** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Connection to the broker.
        - **handlers** (*Mapping**[**Callable**]*) – Event handlers.
          This is a map of event type names and their handlers.
          The special handler “\*” captures all events that don’t have a
          handler.

    app = None

    capture(*limit=None*, *timeout=None*, *wakeup=True*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.capture)
    :   Open up a consumer capturing events.

        This has to run in the main process, and it will never stop
        unless `EventDispatcher.should_stop` is set to True, or
        forced via [`KeyboardInterrupt`](https://docs.python.org/dev/library/exceptions.html#KeyboardInterrupt "(in Python v3.15)") or [`SystemExit`](https://docs.python.org/dev/library/exceptions.html#SystemExit "(in Python v3.15)").

    property connection

    event\_from\_message(*body*, *localize=True*, *now=<built-in function time>*, *tzfields=operator.itemgetter('utcoffset'*, *'timestamp')*, *adjust\_timestamp=<function adjust\_timestamp>*, *CLIENT\_CLOCK\_SKEW=-1*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.event_from_message)

    get\_consumers(*Consumer*, *channel*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.get_consumers)

    itercapture(*limit=None*, *timeout=None*, *wakeup=True*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.itercapture)

    on\_consume\_ready(*connection*, *channel*, *consumers*, *wakeup=True*, *\*\*kwargs*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.on_consume_ready)

    process(*type*, *event*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.process)
    :   Process event by dispatching to configured handler.

    wakeup\_workers(*channel=None*)[[source]](../_modules/celery/events/receiver.html#EventReceiver.wakeup_workers)

celery.events.get\_exchange(*conn*, *name='celeryev'*)[[source]](../_modules/celery/events/event.html#get_exchange)
:   Get exchange used for sending events.

    Parameters:
    :   - **conn** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Connection used for sending/receiving events.
        - **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of the exchange. Default is `celeryev`.

    Note

    The event type changes if Redis is used as the transport
    (from topic -> fanout).

celery.events.group\_from(*type*)[[source]](../_modules/celery/events/event.html#group_from)
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