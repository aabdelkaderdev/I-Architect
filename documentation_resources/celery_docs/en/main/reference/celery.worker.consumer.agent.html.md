<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.agent.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.agent.html).

# `celery.worker.consumer.agent`

Celery + <https://pypi.org/project/cell/> integration.

class celery.worker.consumer.agent.Agent(*c*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/agent.html#Agent)
:   Agent starts <https://pypi.org/project/cell/> actors.

    conditional = True

    create(*c*)[[source]](../_modules/celery/worker/consumer/agent.html#Agent.create)
    :   Create the step.

    name = 'celery.worker.consumer.agent.Agent'

    requires = (step:celery.worker.consumer.connection.Connection{()},)