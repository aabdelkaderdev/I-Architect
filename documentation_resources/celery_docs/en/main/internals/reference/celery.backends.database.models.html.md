<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.database.models.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.database.models.html).

# `celery.backends.database.models`

Database models used by the SQLAlchemy result store backend.

class celery.backends.database.models.Task(*task\_id*)[[source]](../../_modules/celery/backends/database/models.html#Task)
:   Task result/status.

    classmethod configure(*schema=None*, *name=None*)[[source]](../../_modules/celery/backends/database/models.html#Task.configure)

    date\_done

    id

    result

    status

    task\_id

    to\_dict()[[source]](../../_modules/celery/backends/database/models.html#Task.to_dict)

    traceback

class celery.backends.database.models.TaskExtended(*task\_id*)[[source]](../../_modules/celery/backends/database/models.html#TaskExtended)
:   For the extend result.

    args

    date\_done

    id

    kwargs

    name

    queue

    result

    retries

    status

    task\_id

    to\_dict()[[source]](../../_modules/celery/backends/database/models.html#TaskExtended.to_dict)

    traceback

    worker

class celery.backends.database.models.TaskSet(*taskset\_id*, *result*)[[source]](../../_modules/celery/backends/database/models.html#TaskSet)
:   TaskSet result.

    classmethod configure(*schema=None*, *name=None*)[[source]](../../_modules/celery/backends/database/models.html#TaskSet.configure)

    date\_done

    id

    result

    taskset\_id

    to\_dict()[[source]](../../_modules/celery/backends/database/models.html#TaskSet.to_dict)