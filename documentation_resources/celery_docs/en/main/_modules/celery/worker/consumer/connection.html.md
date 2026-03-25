<!-- Source: https://docs.celeryq.dev/en/main/_modules/celery/worker/consumer/connection.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/celery/worker/consumer/connection.html).

# Source code for celery.worker.consumer.connection

```
"""Consumer Broker Connection Bootstep."""
from kombu.common import ignore_errors

from celery import bootsteps
from celery.utils.log import get_logger

__all__ = ('Connection',)

logger = get_logger(__name__)
info = logger.info

[docs]
class Connection(bootsteps.StartStopStep):
    """Service managing the consumer broker connection."""

    def __init__(self, c, **kwargs):
        c.connection = None
        super().__init__(c, **kwargs)

[docs]
    def start(self, c):
        c.connection = c.connect()
        info('Connected to %s', c.connection.as_uri())

[docs]
    def shutdown(self, c):
        # We must set self.connection to None here, so
        # that the green pidbox thread exits.
        connection, c.connection = c.connection, None
        if connection:
            ignore_errors(connection, connection.close)

[docs]
    def info(self, c):
        params = 'N/A'
        if c.connection:
            params = c.connection.info()
            params.pop('password', None)  # don't send password.
        return {'broker': params}
```