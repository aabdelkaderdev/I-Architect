<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.events.dispatcher.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.events.dispatcher.html).

# `celery.events.state`

Event dispatcher sends events.

class celery.events.dispatcher.EventDispatcher(*connection=None*, *hostname=None*, *enabled=True*, *channel=None*, *buffer\_while\_offline=True*, *app=None*, *serializer=None*, *groups=None*, *delivery\_mode=1*, *buffer\_group=None*, *buffer\_limit=24*, *on\_send\_buffered=None*)[[source]](../_modules/celery/events/dispatcher.html#EventDispatcher)
:   Dispatches event messages.

    Parameters:
    :   - **connection** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Connection to the broker.
        - **hostname** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Hostname to identify ourselves as,
          by default uses the hostname returned by
          `anon_nodename()`.
        - **groups** (*Sequence**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – List of groups to send events for.
          [`send()`](#celery.events.dispatcher.EventDispatcher.send "celery.events.dispatcher.EventDispatcher.send") will ignore send requests to groups not in this list.
          If this is `None`, all events will be sent.
          Example groups include `"task"` and `"worker"`.
        - **enabled** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Set to `False` to not actually publish any
          events, making [`send()`](#celery.events.dispatcher.EventDispatcher.send "celery.events.dispatcher.EventDispatcher.send") a no-op.
        - **channel** (*kombu.Channel*) – Can be used instead of connection to specify
          an exact channel to use when sending events.
        - **buffer\_while\_offline** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If enabled events will be buffered
          while the connection is down. [`flush()`](#celery.events.dispatcher.EventDispatcher.flush "celery.events.dispatcher.EventDispatcher.flush") must be called
          as soon as the connection is re-established.

    Note

    You need to [`close()`](#celery.events.dispatcher.EventDispatcher.close "celery.events.dispatcher.EventDispatcher.close") this after use.

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
              Defaults to `Event()`.
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
              defaults to `Event()`.
            - **utcoffset** (*Callable*) – unction returning the current utc offset
              in hours.
            - **\*\*fields** (*Any*) – Event fields – must be json serializable.