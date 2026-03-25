<!-- Source: https://docs.celeryq.dev/projects/pytest-celery/en/latest/getting-started/vendors.html -->

This document describes the current stable version of pytest\_celery (1.3).
For development docs,
[go here](https://pytest-celery.readthedocs.io/en/main/getting-started/vendors.html).

# Vendors

Release:
:   1.3

Date:
:   Mar 24, 2026

## 

The plugin comes with support for several brokers and backends out of
the box. This page lists the supported vendors and their status.

### 

|  |  |  |
| --- | --- | --- |
| **Name** | **Status** | **Enabled** |
| *RabbitMQ* | Stable | Yes |
| *Redis* | Stable | Yes |
| *Localstack (SQS)* | Beta | No |

### 

|  |  |  |
| --- | --- | --- |
| **Name** | **Status** | **Enabled** |
| *Redis* | Stable | Yes |
| *Memcache* | Experimental | No |

Experimental or Beta status means it may be functional but are not confirmed to be production ready.

Enabled means that it is automatically added to the test [Test Setup Matrix](../userguide/setup-matrix.html#setup-matrix)
when running the test suite [if the vendor dependencies are installed](introduction.html#installation).

Warning

Enabling a new vendor will automatically add it globally to every test suite that relies
on the default vendors detection. Be careful when enabling new vendors and make sure they are
stable and production ready.

## 

The plugin provides a built-in Celery worker that can be used to run
tests against. It uses the latest stable version of Celery and can be used, replaced or extended
by the user.

The Dockerfile is published with the source code and can be found using
`WORKER_DOCKERFILE_ROOTDIR`.

pytest\_celery.vendors.worker.Dockerfile

```
FROM python:3.10-slim-bookworm

# Create a user to run the worker
RUN adduser --disabled-password --gecos "" test_user

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential \
    git \
    wget \
    make \
    curl \
    apt-utils \
    debconf \
    lsb-release \
    libcurl4-openssl-dev \
    libmemcached-dev \
    libffi-dev \
    libssl-dev \
    ca-certificates \
    pypy3 \
    pypy3-lib \
    sudo

# Set arguments
ARG CELERY_VERSION=""
ARG CELERY_LOG_LEVEL=INFO
ARG CELERY_WORKER_NAME=celery_test_worker
ARG CELERY_WORKER_QUEUE=celery
ARG PYTEST_CELERY_PKG="pytest-celery"
ENV WORKER_VERSION=$CELERY_VERSION
ENV LOG_LEVEL=$CELERY_LOG_LEVEL
ENV WORKER_NAME=$CELERY_WORKER_NAME
ENV WORKER_QUEUE=$CELERY_WORKER_QUEUE

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 5678

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade \
    pip \
    celery[redis,pymemcache,gevent,sqs]${WORKER_VERSION:+==$WORKER_VERSION} \
    "${PYTEST_CELERY_PKG}"

# The workdir must be /app
WORKDIR /app

COPY content/ .

# Switch to the test_user
USER test_user

# Start the celery worker
CMD celery -A app worker --loglevel=$LOG_LEVEL -n $WORKER_NAME@%h -Q $WORKER_QUEUE
```

## 

To use the [Localstack broker](first-steps.html#localstack-broker), you will need add additional configuration to the test setup.

You may add this to `conftest.py` to configure the Localstack broker.

```
import os

import pytest
from celery import Celery

from pytest_celery import LOCALSTACK_CREDS

@pytest.fixture
def default_worker_env(default_worker_env: dict) -> dict:
    default_worker_env.update(LOCALSTACK_CREDS)
    return default_worker_env

@pytest.fixture(scope="session", autouse=True)
def set_aws_credentials():
    os.environ.update(LOCALSTACK_CREDS)

@pytest.fixture
def default_worker_app(default_worker_app: Celery) -> Celery:
    app = default_worker_app
    if app.conf.broker_url and app.conf.broker_url.startswith("sqs"):
        app.conf.broker_transport_options["region"] = LOCALSTACK_CREDS["AWS_DEFAULT_REGION"]
    return app
```

And to enable the Localstack broker in the default [Test Setup Matrix](../userguide/setup-matrix.html#setup-matrix), add the following configuration to `conftest.py`.

```
from pytest_celery import ALL_CELERY_BROKERS
from pytest_celery import CELERY_LOCALSTACK_BROKER
from pytest_celery import CeleryTestBroker
from pytest_celery import _is_vendor_installed

if _is_vendor_installed("localstack"):
    ALL_CELERY_BROKERS.add(CELERY_LOCALSTACK_BROKER)

@pytest.fixture(params=ALL_CELERY_BROKERS)
def celery_broker(request: pytest.FixtureRequest) -> CeleryTestBroker:  # type: ignore
    broker: CeleryTestBroker = request.getfixturevalue(request.param)
    yield broker
    broker.teardown()
```

## 

Injected brokers, backends and workers can extend the built-in ones or
provide completely new ones. The plugin provides a set of base classes
that can be used to implement custom vendors.

### 

*class* pytest\_celery.api.broker.CeleryTestBroker(*container: [CeleryTestContainer](../reference/pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")*, *app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)") = None*)[[source]](../_modules/pytest_celery/api/broker.html#CeleryTestBroker)
:   Bases: [`CeleryTestNode`](../reference/pytest_celery.api.html#pytest_celery.api.base.CeleryTestNode "pytest_celery.api.base.CeleryTestNode")

    This is specialized node type for handling celery brokers nodes. It is
    used to encapsulate a broker instance.

    Responsibility Scope:
    :   Handling broker specific requirements and configuration.

    *property* app*: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)")*
    :   Celery app for the node if available.

    assert\_log\_does\_not\_exist(*log: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *message: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*, *timeout: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 1*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Assert that a log does not exist in the container.

        Parameters:
        :   - **log** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Log to assert.
            - **message** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *optional*) – Message to display while waiting. Defaults to “”.
            - **timeout** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Timeout in seconds. Defaults to 1.

    assert\_log\_exists(*log: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *message: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*, *timeout: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 60*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Assert that a log exists in the container.

        Parameters:
        :   - **log** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Log to assert.
            - **message** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *optional*) – Message to display while waiting. Defaults to “”.
            - **timeout** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Timeout in seconds. Defaults to RESULT\_TIMEOUT.

    config(*\*args: [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")*, *\*\*kwargs: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")
    :   Compile the configurations required for Celery from this node.

    *property* container*: [CeleryTestContainer](../reference/pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")*
    :   Underlying container for the node.

    *classmethod* default\_config() → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/api/broker.html#CeleryTestBroker.default_config)
    :   Default node configurations if not overridden by the user.

    hostname() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")
    :   Get the hostname of this node.

    kill(*signal: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 'SIGKILL'*, *reload\_container: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Kill the underlying container.

        Parameters:
        :   - **signal** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") *|* [*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Signal to send to the container. Defaults to “SIGKILL”.
            - **reload\_container** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")*,* *optional*) – Reload the container object after killing it. Defaults to True.

    logs() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")
    :   Get the logs of the underlying container.

    name() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")
    :   Get the name of this node.

    ready() → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")
    :   Waits until the node is ready or raise an exception if it fails to
        boot up.

    restart(*reload\_container: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*, *force: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/pytest_celery/api/broker.html#CeleryTestBroker.restart)
    :   Override restart method to update the app broker url with new
        container values.

    teardown() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Teardown the node.

    wait\_for\_log(*log: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *message: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*, *timeout: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 60*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Wait for a log to appear in the container.

        Parameters:
        :   - **log** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Log to wait for.
            - **message** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *optional*) – Message to display while waiting. Defaults to “”.
            - **timeout** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Timeout in seconds. Defaults to RESULT\_TIMEOUT.

### 

*class* pytest\_celery.api.backend.CeleryTestBackend(*container: [CeleryTestContainer](../reference/pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")*, *app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)") = None*)[[source]](../_modules/pytest_celery/api/backend.html#CeleryTestBackend)
:   Bases: [`CeleryTestNode`](../reference/pytest_celery.api.html#pytest_celery.api.base.CeleryTestNode "pytest_celery.api.base.CeleryTestNode")

    This is specialized node type for handling celery backends nodes. It is
    used to encapsulate a backend instance.

    Responsibility Scope:
    :   Handling backend specific requirements and configuration.

    *property* app*: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)")*
    :   Celery app for the node if available.

    assert\_log\_does\_not\_exist(*log: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *message: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*, *timeout: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 1*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Assert that a log does not exist in the container.

        Parameters:
        :   - **log** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Log to assert.
            - **message** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *optional*) – Message to display while waiting. Defaults to “”.
            - **timeout** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Timeout in seconds. Defaults to 1.

    assert\_log\_exists(*log: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *message: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*, *timeout: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 60*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Assert that a log exists in the container.

        Parameters:
        :   - **log** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Log to assert.
            - **message** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *optional*) – Message to display while waiting. Defaults to “”.
            - **timeout** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Timeout in seconds. Defaults to RESULT\_TIMEOUT.

    config(*\*args: [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")*, *\*\*kwargs: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")
    :   Compile the configurations required for Celery from this node.

    *property* container*: [CeleryTestContainer](../reference/pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")*
    :   Underlying container for the node.

    *classmethod* default\_config() → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/api/backend.html#CeleryTestBackend.default_config)
    :   Default node configurations if not overridden by the user.

    hostname() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")
    :   Get the hostname of this node.

    kill(*signal: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 'SIGKILL'*, *reload\_container: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Kill the underlying container.

        Parameters:
        :   - **signal** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") *|* [*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Signal to send to the container. Defaults to “SIGKILL”.
            - **reload\_container** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")*,* *optional*) – Reload the container object after killing it. Defaults to True.

    logs() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")
    :   Get the logs of the underlying container.

    name() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")
    :   Get the name of this node.

    ready() → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")
    :   Waits until the node is ready or raise an exception if it fails to
        boot up.

    restart(*reload\_container: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*, *force: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/pytest_celery/api/backend.html#CeleryTestBackend.restart)
    :   Override restart method to update the app result backend with new
        container values.

    teardown() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Teardown the node.

    wait\_for\_log(*log: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *message: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*, *timeout: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 60*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Wait for a log to appear in the container.

        Parameters:
        :   - **log** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Log to wait for.
            - **message** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *optional*) – Message to display while waiting. Defaults to “”.
            - **timeout** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Timeout in seconds. Defaults to RESULT\_TIMEOUT.

### 

*class* pytest\_celery.api.worker.CeleryTestWorker(*container: [CeleryTestContainer](../reference/pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")*, *app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)")*)[[source]](../_modules/pytest_celery/api/worker.html#CeleryTestWorker)
:   Bases: [`CeleryTestNode`](../reference/pytest_celery.api.html#pytest_celery.api.base.CeleryTestNode "pytest_celery.api.base.CeleryTestNode")

    This is specialized node type for handling celery worker nodes. It is
    used to encapsulate a worker instance.

    Responsibility Scope:
    :   Managing a celery worker.

    *property* app*: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)")*
    :   Celery app for the node if available.

    assert\_log\_does\_not\_exist(*log: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *message: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*, *timeout: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 1*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Assert that a log does not exist in the container.

        Parameters:
        :   - **log** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Log to assert.
            - **message** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *optional*) – Message to display while waiting. Defaults to “”.
            - **timeout** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Timeout in seconds. Defaults to 1.

    assert\_log\_exists(*log: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *message: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*, *timeout: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 60*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Assert that a log exists in the container.

        Parameters:
        :   - **log** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Log to assert.
            - **message** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *optional*) – Message to display while waiting. Defaults to “”.
            - **timeout** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Timeout in seconds. Defaults to RESULT\_TIMEOUT.

    config(*\*args: [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")*, *\*\*kwargs: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")
    :   Compile the configurations required for Celery from this node.

    *property* container*: [CeleryTestContainer](../reference/pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")*
    :   Underlying container for the node.

    *classmethod* default\_config() → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")
    :   Default node configurations if not overridden by the user.

    get\_running\_processes\_info(*columns: [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *filters: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")][[source]](../_modules/pytest_celery/api/worker.html#CeleryTestWorker.get_running_processes_info)
    :   Get running processes info on the container of this node.

        Possible columns:
        :   - pid
            - name
            - username
            - cmdline
            - cpu\_percent
            - memory\_percent
            - create\_time

        Parameters:
        :   - **columns** ([*list*](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")*[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]* *|* *None**,* *optional*) – Columns to query. Defaults to None (all).
            - **filters** ([*dict*](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]* *|* *None**,* *optional*) – Filters to apply. Defaults to None.

        Raises:
        :   [**RuntimeError**](https://docs.python.org/dev/library/exceptions.html#RuntimeError "(in Python v3.15)") – If the command fails.

        Returns:
        :   List of processes info per requested columns.

        Return type:
        :   [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")]

    hostname() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/api/worker.html#CeleryTestWorker.hostname)
    :   Hostname of the worker node.

    kill(*signal: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 'SIGKILL'*, *reload\_container: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Kill the underlying container.

        Parameters:
        :   - **signal** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") *|* [*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Signal to send to the container. Defaults to “SIGKILL”.
            - **reload\_container** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")*,* *optional*) – Reload the container object after killing it. Defaults to True.

    *property* log\_level*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*
    :   Celery log level of this worker node.

    logs() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")
    :   Get the logs of the underlying container.

    name() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")
    :   Get the name of this node.

    ready() → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")
    :   Waits until the node is ready or raise an exception if it fails to
        boot up.

    restart(*reload\_container: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*, *force: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Restart the underlying container.

        Parameters:
        :   - **reload\_container** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")*,* *optional*) – Reload the container object after restarting it. Defaults to True.
            - **force** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")*,* *optional*) – Kill the container before restarting it. Defaults to False.

    teardown() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Teardown the node.

    *property* version*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*
    :   Celery version of this worker node.

    wait\_for\_log(*log: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *message: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*, *timeout: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 60*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")
    :   Wait for a log to appear in the container.

        Parameters:
        :   - **log** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Log to wait for.
            - **message** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *optional*) – Message to display while waiting. Defaults to “”.
            - **timeout** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* *optional*) – Timeout in seconds. Defaults to RESULT\_TIMEOUT.

    *property* worker\_name*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*
    :   Celery test worker node name.

    *property* worker\_queue*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*
    :   Celery queue for this worker node.

## 

The **Vendor Class** is an optional mechanism for OOP style configuration of the plugin’s vendors.
It allows registering a class that defines how does the vendor behave and configured.

The vendor class represents the vendor’s container class that is used automatically by the plugin.

The following diagram shows the relationship between the vendor class and the vendor’s infrastructure.

```
        graph TD;
    Vendor[Vendor] --> BrokerComponent[Broker Component]
    Vendor --> BackendComponent[Backend Component]
    Vendor --> WorkerComponent[Worker Component]

    BrokerComponent --> Comp
    BackendComponent --> Comp
    WorkerComponent --> Comp

    subgraph Comp["Component"]
        Node[Node] --> Container[Container]
    end

    Comp --> DefaultFixtures[Default Fixtures]
    Comp --> VendorClass[Vendor Class]
    VendorClass -. "You are here" .-> VendorClass
    DefaultFixtures <.-> VendorClass

    style Vendor fill:#f9f,stroke:#333,stroke-width:4px
    style Comp fill:#ddf,stroke:#333,stroke-width:2px
    style Node fill:#eeffdd,stroke:#333
    style Container fill:#ffffee,stroke:#333
    style VendorClass fill:#ffeedd,stroke:#333
```

### 

Warning

It is used only to override the built-in vendors **containers**.

#### Registering a Vendor Class

The plugin uses the vendor class to implement the default fixtures of the vendor.
To override it, create your own vendor class and subclass the matching built-in vendor class
to include the built-in fixtures implementation.

##### Worker Example

```
class MyWorkerContainer(CeleryWorkerContainer):
    @property
    def client(self) -> Any:
        return self

    @classmethod
    def version(cls) -> str:
        return celery.__version__

    @classmethod
    def log_level(cls) -> str:
        return "INFO"

    @classmethod
    def worker_name(cls) -> str:
        return "my_tests_worker"

    @classmethod
    def worker_queue(cls) -> str:
        return "my_tests_queue"

    def post_initialization_logic(self) -> None:
        pass
```

And then, register it using the matching default fixture.

```
@pytest.fixture
def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return MyWorkerContainer
```

Warning

The worker vendor requires another fixture to be registered to allow configuring the worker
before it gets built.

```
@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
    return MyWorkerContainer
```

There’s no `session` vendor class for other vendors.

- For RabbitMQ Broker use [`default_rabbitmq_broker_cls`](../reference/pytest_celery.vendors.rabbitmq.html#pytest_celery.vendors.rabbitmq.fixtures.default_rabbitmq_broker_cls "pytest_celery.vendors.rabbitmq.fixtures.default_rabbitmq_broker_cls").
- For Redis Broker use [`default_redis_broker_cls`](../reference/pytest_celery.vendors.redis.broker.html#pytest_celery.vendors.redis.broker.fixtures.default_redis_broker_cls "pytest_celery.vendors.redis.broker.fixtures.default_redis_broker_cls").
- For SQS Broker use [`default_localstack_broker_cls`](../reference/pytest_celery.vendors.localstack.html#pytest_celery.vendors.localstack.fixtures.default_localstack_broker_cls "pytest_celery.vendors.localstack.fixtures.default_localstack_broker_cls").
- For Redis Backend use [`default_redis_backend_cls`](../reference/pytest_celery.vendors.redis.backend.html#pytest_celery.vendors.redis.backend.fixtures.default_redis_backend_cls "pytest_celery.vendors.redis.backend.fixtures.default_redis_backend_cls").
- For Memcache Backend use [`default_memcached_backend_cls`](../reference/pytest_celery.vendors.memcached.html#pytest_celery.vendors.memcached.fixtures.default_memcached_backend_cls "pytest_celery.vendors.memcached.fixtures.default_memcached_backend_cls").

#### Accessing the Vendor Class

Once a vendor class has been registered, it can be accessed using the [Test Setup](first-steps.html#test-setup).
Any additional API added to the class can be accessed as well.

For example,

```
def test_accessing_post_initialization_logic(celery_setup: CeleryTestSetup):
    worker: MyWorkerContainer = celery_setup.worker
    worker.post_initialization_logic()
```