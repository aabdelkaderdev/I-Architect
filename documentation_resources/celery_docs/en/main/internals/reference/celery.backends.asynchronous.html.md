<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.asynchronous.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.asynchronous.html).

# `celery.backends.asynchronous`

Async I/O backend support utilities.

class celery.backends.asynchronous.AsyncBackendMixin[[source]](../../_modules/celery/backends/asynchronous.html#AsyncBackendMixin)
:   Mixin for backends that enables the async API.

    add\_pending\_result(*result*, *weak=False*, *start\_drainer=True*)[[source]](../../_modules/celery/backends/asynchronous.html#AsyncBackendMixin.add_pending_result)

    add\_pending\_results(*results*, *weak=False*)[[source]](../../_modules/celery/backends/asynchronous.html#AsyncBackendMixin.add_pending_results)

    property is\_async

    iter\_native(*result*, *no\_ack=True*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/asynchronous.html#AsyncBackendMixin.iter_native)

    on\_result\_fulfilled(*result*)[[source]](../../_modules/celery/backends/asynchronous.html#AsyncBackendMixin.on_result_fulfilled)

    remove\_pending\_result(*result*)[[source]](../../_modules/celery/backends/asynchronous.html#AsyncBackendMixin.remove_pending_result)

    wait\_for\_pending(*result*, *callback=None*, *propagate=True*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/asynchronous.html#AsyncBackendMixin.wait_for_pending)

class celery.backends.asynchronous.BaseResultConsumer(*backend*, *app*, *accept*, *pending\_results*, *pending\_messages*)[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer)
:   Manager responsible for consuming result messages.

    cancel\_for(*task\_id*)[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer.cancel_for)

    consume\_from(*task\_id*)[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer.consume_from)

    drain\_events(*timeout=None*)[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer.drain_events)

    drain\_events\_until(*p*, *timeout=None*, *on\_interval=None*)[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer.drain_events_until)

    on\_after\_fork()[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer.on_after_fork)

    on\_out\_of\_band\_result(*message*)[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer.on_out_of_band_result)

    on\_state\_change(*meta*, *message*)[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer.on_state_change)

    on\_wait\_for\_pending(*result*, *timeout=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer.on_wait_for_pending)

    reconnect\_on\_error()[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer.reconnect_on_error)
    :   Context manager that catches connection errors and reconnects.

        Wraps a block of code so that any `_connection_errors` raised
        inside it trigger a call to `_reconnect()`. If reconnection
        itself raises a connection error the consumer is considered
        unrecoverable and a [`RuntimeError`](https://docs.python.org/dev/library/exceptions.html#RuntimeError "(in Python v3.15)") is raised to signal that
        the Celery application must be restarted.

    start(*initial\_task\_id*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer.start)

    stop()[[source]](../../_modules/celery/backends/asynchronous.html#BaseResultConsumer.stop)

class celery.backends.asynchronous.Drainer(*result\_consumer*)[[source]](../../_modules/celery/backends/asynchronous.html#Drainer)
:   Result draining service.

    drain\_events\_until(*p*, *timeout=None*, *interval=1*, *on\_interval=None*, *wait=None*)[[source]](../../_modules/celery/backends/asynchronous.html#Drainer.drain_events_until)

    start()[[source]](../../_modules/celery/backends/asynchronous.html#Drainer.start)

    stop()[[source]](../../_modules/celery/backends/asynchronous.html#Drainer.stop)

    wait\_for(*p*, *wait*, *timeout=None*)[[source]](../../_modules/celery/backends/asynchronous.html#Drainer.wait_for)

celery.backends.asynchronous.register\_drainer(*name*)[[source]](../../_modules/celery/backends/asynchronous.html#register_drainer)
:   Decorator used to register a new result drainer type.