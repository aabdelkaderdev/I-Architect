<!-- Source: https://docs.celeryq.dev/en/main/_modules/celery/worker/consumer/mingle.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/celery/worker/consumer/mingle.html).

# Source code for celery.worker.consumer.mingle

```
"""Worker <-> Worker Sync at startup (Bootstep)."""
from celery import bootsteps
from celery.utils.log import get_logger

from .events import Events

__all__ = ('Mingle',)

logger = get_logger(__name__)
debug, info, exception = logger.debug, logger.info, logger.exception

[docs]
class Mingle(bootsteps.StartStopStep):
    """Bootstep syncing state with neighbor workers.

    At startup, or upon consumer restart, this will:

    - Sync logical clocks.
    - Sync revoked tasks.

    """

    label = 'Mingle'
    requires = (Events,)
    compatible_transports = {'amqp', 'redis', 'gcpubsub'}

    def __init__(self, c, without_mingle=False, **kwargs):
        self.enabled = not without_mingle and self.compatible_transport(c.app)
        super().__init__(
            c, without_mingle=without_mingle, **kwargs)

[docs]
    def compatible_transport(self, app):
        with app.connection_for_read() as conn:
            return conn.transport.driver_type in self.compatible_transports

[docs]
    def start(self, c):
        self.sync(c)

[docs]
    def sync(self, c):
        info('mingle: searching for neighbors')
        replies = self.send_hello(c)
        if replies:
            info('mingle: sync with %s nodes',
                 len([reply for reply, value in replies.items() if value]))
            [self.on_node_reply(c, nodename, reply)
             for nodename, reply in replies.items() if reply]
            info('mingle: sync complete')
        else:
            info('mingle: all alone')

[docs]
    def send_hello(self, c):
        inspect = c.app.control.inspect(timeout=1.0, connection=c.connection)
        our_revoked = c.controller.state.revoked
        replies = inspect.hello(c.hostname, our_revoked._data) or {}
        replies.pop(c.hostname, None)  # delete my own response
        return replies

[docs]
    def on_node_reply(self, c, nodename, reply):
        debug('mingle: processing reply from %s', nodename)
        try:
            self.sync_with_node(c, **reply)
        except MemoryError:
            raise
        except Exception as exc:  # pylint: disable=broad-except
            exception('mingle: sync with %s failed: %r', nodename, exc)

[docs]
    def sync_with_node(self, c, clock=None, revoked=None, **kwargs):
        self.on_clock_event(c, clock)
        self.on_revoked_received(c, revoked)

[docs]
    def on_clock_event(self, c, clock):
        c.app.clock.adjust(clock) if clock else c.app.clock.forward()

[docs]
    def on_revoked_received(self, c, revoked):
        if revoked:
            c.controller.state.revoked.update(revoked)
```