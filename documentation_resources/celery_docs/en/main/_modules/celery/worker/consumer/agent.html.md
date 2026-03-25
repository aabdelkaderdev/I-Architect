<!-- Source: https://docs.celeryq.dev/en/main/_modules/celery/worker/consumer/agent.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/celery/worker/consumer/agent.html).

# Source code for celery.worker.consumer.agent

```
"""Celery + :pypi:`cell` integration."""
from celery import bootsteps

from .connection import Connection

__all__ = ('Agent',)

[docs]
class Agent(bootsteps.StartStopStep):
    """Agent starts :pypi:`cell` actors."""

    conditional = True
    requires = (Connection,)

    def __init__(self, c, **kwargs):
        self.agent_cls = self.enabled = c.app.conf.worker_agent
        super().__init__(c, **kwargs)

[docs]
    def create(self, c):
        agent = c.agent = self.instantiate(self.agent_cls, c.connection)
        return agent
```