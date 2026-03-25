<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.app.amqp.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.amqp.html).

Sending/Receiving Messages (Kombu integration).

# 

class celery.app.amqp.AMQP(*app*)[[source]](../_modules/celery/app/amqp.html#AMQP)
:   App AMQP API: app.amqp.

    Connection
    :   Broker connection class used. Default is [`kombu.Connection`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)").

    Consumer
    :   Base Consumer class used. Default is [`kombu.Consumer`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Consumer "(in Kombu v5.6)").

    Producer
    :   Base Producer class used. Default is [`kombu.Producer`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Producer "(in Kombu v5.6)").

    queues
    :   All currently defined task queues (a [`Queues`](#celery.app.amqp.Queues "celery.app.amqp.Queues") instance).

    argsrepr\_maxsize
    :   Max size of positional argument representation used for logging
        purposes. Default is 1024.

    kwargsrepr\_maxsize
    :   Max size of keyword argument representation used for logging
        purposes. Default is 1024.

    Queues(*queues*, *create\_missing=None*, *create\_missing\_queue\_type=None*, *create\_missing\_queue\_exchange\_type=None*, *autoexchange=None*, *max\_priority=None*)[[source]](../_modules/celery/app/amqp.html#AMQP.Queues)

    Router(*queues=None*, *create\_missing=None*)[[source]](../_modules/celery/app/amqp.html#AMQP.Router)
    :   Return the current task router.

    flush\_routes()[[source]](../_modules/celery/app/amqp.html#AMQP.flush_routes)

    create\_task\_message

    send\_task\_message

    default\_queue

    default\_exchange

    producer\_pool

    router

    routes

# 

class celery.app.amqp.Queues(*queues=None*, *default\_exchange=None*, *create\_missing=True*, *create\_missing\_queue\_type=None*, *create\_missing\_queue\_exchange\_type=None*, *autoexchange=None*, *max\_priority=None*, *default\_routing\_key=None*)[[source]](../_modules/celery/app/amqp.html#Queues)
:   Queue name⇒ declaration mapping.

    Parameters:
    :   - **queues** (*Iterable*) – Initial list/tuple or dict of queues.
        - **create\_missing** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – By default any unknown queues will be
          added automatically, but if this flag is disabled the occurrence
          of unknown queues in wanted will raise [`KeyError`](https://docs.python.org/dev/library/exceptions.html#KeyError "(in Python v3.15)").
        - **create\_missing\_queue\_type** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Type of queue to create for missing queues.
          Must be either ‘classic’ (default) or ‘quorum’. If set to ‘quorum’,
          the broker will declare new queues using the quorum type.
        - **create\_missing\_queue\_exchange\_type** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Type of exchange to use
          when creating missing queues. If not set, the default exchange type
          will be used. If set, the exchange type will be set to this value
          when creating missing queues.
        - **max\_priority** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – Default x-max-priority for queues with none set.

    add(*queue*, *\*\*kwargs*)[[source]](../_modules/celery/app/amqp.html#Queues.add)
    :   Add new queue.

        The first argument can either be a [`kombu.Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") instance,
        or the name of a queue. If the former the rest of the keyword
        arguments are ignored, and options are simply taken from the queue
        instance.

        Parameters:
        :   - **queue** ([*kombu.Queue*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)")*,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Queue to add.
            - **exchange** ([*kombu.Exchange*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Exchange "(in Kombu v5.6)")*,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – if queue is str, specifies exchange name.
            - **routing\_key** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – if queue is str, specifies binding key.
            - **exchange\_type** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – if queue is str, specifies type of exchange.
            - **\*\*options** (*Any*) – Additional declaration options used when
              queue is a str.

    add\_compat(*name*, *\*\*options*)[[source]](../_modules/celery/app/amqp.html#Queues.add_compat)

    property consume\_from

    deselect(*exclude*)[[source]](../_modules/celery/app/amqp.html#Queues.deselect)
    :   Deselect queues so that they won’t be consumed from.

        Parameters:
        :   **exclude** (*Sequence**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]**,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Names of queues to avoid
            consuming from.

    format(*indent=0*, *indent\_first=True*)[[source]](../_modules/celery/app/amqp.html#Queues.format)
    :   Format routing table into string for log dumps.

    new\_missing(*name*)[[source]](../_modules/celery/app/amqp.html#Queues.new_missing)

    select(*include*)[[source]](../_modules/celery/app/amqp.html#Queues.select)
    :   Select a subset of currently defined queues to consume from.

        Parameters:
        :   **include** (*Sequence**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]**,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Names of queues to consume from.

    select\_add(*queue*, *\*\*kwargs*)[[source]](../_modules/celery/app/amqp.html#Queues.select_add)
    :   Add new task queue that’ll be consumed from.

        The queue will be active even when a subset has been selected
        using the [`celery worker -Q`](cli.html#cmdoption-celery-worker-Q) option.