<!-- Source: https://docs.celeryq.dev/en/main/history/whatsnew-5.5.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/history/whatsnew-5.5.html).

# What’s new in Celery 5.5 (Immunity)

Author:
:   Tomer Nosrati (`tomer.nosrati at gmail.com`).

Celery is a simple, flexible, and reliable distributed programming framework
to process vast amounts of messages, while providing operations with
the tools required to maintain a distributed system with python.

It’s a task queue with focus on real-time processing, while also
supporting task scheduling.

Celery has a large and diverse community of users and contributors,
you should come join us on IRC
or our mailing-list.

Note

Following the problems with Freenode, we migrated our IRC channel to Libera Chat
as most projects did.
You can also join us using [Gitter](https://gitter.im/celery/celery).

We’re sometimes there to answer questions. We welcome you to join.

To read more about Celery you should go read the [introduction](../getting-started/introduction.html#intro).

While this version is **mostly** backward compatible with previous versions
it’s important that you read the following section as this release
is a new major version.

This version is officially supported on CPython 3.8, 3.9, 3.10, 3.11, 3.12 and 3.13.
and is also supported on PyPy3.10+.

## 

Note

**This release contains fixes for many long standing bugs & stability issues.
We encourage our users to upgrade to this release as soon as possible.**

The 5.5.0 release is a new feature release for Celery.

Releases in the 5.x series are codenamed after songs of [Jon Hopkins](https://en.wikipedia.org/wiki/Jon_Hopkins).
This release has been codenamed [Immunity](https://www.youtube.com/watch?v=Y8eQR5DMous).

From now on we only support Python 3.8 and above.
We will maintain compatibility with Python 3.8 until it’s
EOL in 2024.

*— Tomer Nosrati*

### 

We no longer support Celery 4.x as we don’t have the resources to do so.
If you’d like to help us, all contributions are welcome.

Celery 5.x **is not** an LTS release. We will support it until the release
of Celery 6.x.

We’re in the process of defining our Long Term Support policy.
Watch the next “What’s New” document for updates.

## 

### 

Celery 5.0 introduces a new CLI implementation which isn’t completely backwards compatible.

The global options can no longer be positioned after the sub-command.
Instead, they must be positioned as an option for the celery command like so:

```
celery --app path.to.app worker
```

If you were using our [Daemonization](../userguide/daemonizing.html#daemonizing) guide to deploy Celery in production,
you should revisit it for updates.

### 

If you haven’t already updated your configuration when you migrated to Celery 4.0,
please do so now.

We elected to extend the deprecation period until 6.0 since
we did not loudly warn about using these deprecated settings.

Please refer to the [migration guide](../userguide/configuration.html#conf-old-settings-map) for instructions.

### 

Make sure you are not affected by any of the important upgrade notes
mentioned in the [following section](#v550-important).

You should verify that none of the breaking changes in the CLI
do not affect you. Please refer to [New Command Line Interface](whatsnew-5.0.html#new-command-line-interface) for details.

### 

Celery 5.x only supports Python 3. Therefore, you must ensure your code is
compatible with Python 3.

If you haven’t ported your code to Python 3, you must do so before upgrading.

You can use tools like [2to3](https://docs.python.org/3.8/library/2to3.html)
and [pyupgrade](https://github.com/asottile/pyupgrade) to assist you with
this effort.

After the migration is done, run your test suite with Celery 5 to ensure
nothing has been broken.

### 

At this point you can upgrade your workers and clients with the new version.

## 

### 

The supported Python versions are:

- CPython 3.8
- CPython 3.9
- CPython 3.10
- CPython 3.11
- CPython 3.12
- CPython 3.13
- PyPy3.10 (`pypy3`)

### 

Python 3.8 will reach EOL in October, 2024.

### 

#### 

Starting from Celery v5.5, the minimum required version is Kombu 5.5.

#### 

redis-py 4.5.2 is the new minimum required version.

#### 

SQLAlchemy 1.4.x & 2.0.x is now supported in Celery v5.5.

#### 

Minimum required version is now 4.2.1.

#### 

Minimum django version is bumped to v2.2.28.
Also added –skip-checks flag to bypass django core checks.

## 

### 

Long-standing disconnection issues with the Redis broker have been identified and
resolved in Kombu 5.5.0. These improvements significantly enhance stability when
using Redis as a broker, particularly in high-throughput environments.

Additionally, the Redis backend now has better exception handling with the new
`exception_safe_to_retry` feature, which improves resilience during temporary
Redis connection issues. See [Redis backend settings](../userguide/configuration.html#conf-redis-result-backend) for complete
documentation.

### 

Replaced the <https://pypi.org/project/pycurl/> dependency with <https://pypi.org/project/urllib3/>.

We’re monitoring the performance impact of this change and welcome feedback from users
who notice any significant differences in their environments.

### 

Added support for RabbitMQ’s new [Quorum Queues](https://www.rabbitmq.com/docs/quorum-queues)
feature, including compatibility with ETA tasks. This implementation has some limitations compared
to classic queues, so please refer to the documentation for details.

[Native Delayed Delivery](https://docs.particular.net/transports/rabbitmq/delayed-delivery)
is automatically enabled when quorum queues are detected to implement the ETA mechanism.

See [Using Quorum Queues](../getting-started/backends-and-brokers/rabbitmq.html#using-quorum-queues) for complete documentation.

Configuration options:

- [`broker_native_delayed_delivery_queue_type`](../userguide/configuration.html#std-setting-broker_native_delayed_delivery_queue_type): Specifies the queue type for
  delayed delivery (default: `quorum`)
- [`task_default_queue_type`](../userguide/configuration.html#std-setting-task_default_queue_type): Sets the default queue type for tasks
  (default: `classic`)
- [`worker_detect_quorum_queues`](../userguide/configuration.html#std-setting-worker_detect_quorum_queues): Controls automatic detection of quorum
  queues (default: `True`)

### 

Soft shutdown is a time limited warm shutdown, initiated just before the cold shutdown.
The worker will allow [`worker_soft_shutdown_timeout`](../userguide/configuration.html#std-setting-worker_soft_shutdown_timeout) seconds for all currently
executing tasks to finish before it terminates. If the time limit is reached, the worker
will initiate a cold shutdown and cancel all currently executing tasks.

This feature is particularly valuable when using brokers with visibility timeout
mechanisms, such as Redis or SQS. It allows the worker enough time to re-queue
tasks that were not completed before exiting, preventing task loss during worker
shutdown.

See [Stopping the worker](../userguide/workers.html#worker-stopping) for complete documentation on worker shutdown types.

Configuration options:

- [`worker_soft_shutdown_timeout`](../userguide/configuration.html#std-setting-worker_soft_shutdown_timeout): Sets the duration in seconds for the soft
  shutdown period (default: `0.0`, disabled)
- [`worker_enable_soft_shutdown_on_idle`](../userguide/configuration.html#std-setting-worker_enable_soft_shutdown_on_idle): Controls whether soft shutdown
  should be enabled even when the worker is idle (default: `False`)

### 

New native support for Pydantic models in tasks. This integration allows you to
leverage Pydantic’s powerful data validation and serialization capabilities directly
in your Celery tasks.

Example usage:

```
from pydantic import BaseModel
from celery import Celery

app = Celery('tasks')

class ArgModel(BaseModel):
    value: int

class ReturnModel(BaseModel):
    value: str

@app.task(pydantic=True)
def x(arg: ArgModel) -> ReturnModel:
    # args/kwargs type hinted as Pydantic model will be converted
    assert isinstance(arg, ArgModel)

    # The returned model will be converted to a dict automatically
    return ReturnModel(value=f"example: {arg.value}")
```

See [Argument validation with Pydantic](../userguide/tasks.html#task-pydantic) for complete documentation.

Configuration options:

- `pydantic=True`: Enables Pydantic integration for the task
- `pydantic_strict=True/False`: Controls whether strict validation is enabled
  (default: `False`)
- `pydantic_context={...}`: Provides additional context for validation
- `pydantic_dump_kwargs={...}`: Customizes serialization behavior

### 

New support for Google Cloud Pub/Sub as a message transport, expanding Celery’s
cloud integration options.

See [Using Google Pub/Sub](../getting-started/backends-and-brokers/gcpubsub.html#broker-gcpubsub) for complete documentation.

For the Google Pub/Sub support you have to install additional dependencies:

```
$ pip install "celery[gcpubsub]"
```

Then configure your Celery application to use the Google Pub/Sub transport:

```
broker_url = 'gcpubsub://projects/project-id'
```

### 

Official support for Python 3.13. All core dependencies have been updated to
ensure compatibility, including Kombu and py-amqp.

This release maintains compatibility with Python 3.8 through 3.13, as well as
PyPy 3.10+.

### 

The “REMAP\_SIGTERM” feature, previously undocumented, has been tested, documented,
and is now officially supported. This feature allows you to remap the SIGTERM
signal to SIGQUIT, enabling you to initiate a soft or cold shutdown using TERM
instead of QUIT.

This is particularly useful in containerized environments where SIGTERM is the
standard signal for graceful termination.

See [Cold Shutdown documentation](../userguide/workers.html#worker-remap-sigterm) for more info.

To enable this feature, set the environment variable:

```
export REMAP_SIGTERM="SIGQUIT"
```

### 

New `create_tables_at_setup` option for the database backend. This option
controls when database tables are created, allowing for non-lazy table creation.

By default (`create_tables_at_setup=True`), tables are created during backend
initialization. Setting this to `False` defers table creation until they are
actually needed, which can be useful in certain deployment scenarios where you want
more control over database schema management.

See [Database backend settings](../userguide/configuration.html#conf-database-result-backend) for complete documentation.