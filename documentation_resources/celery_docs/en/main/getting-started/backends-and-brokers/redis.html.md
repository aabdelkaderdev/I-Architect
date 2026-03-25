<!-- Source: https://docs.celeryq.dev/en/main/getting-started/backends-and-brokers/redis.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/getting-started/backends-and-brokers/redis.html).

# Using Redis

## Installation

For the Redis support you have to install additional dependencies.
You can install both Celery and these dependencies in one go using
the `celery[redis]` [bundle](../introduction.html#bundles):

```
$ pip install -U "celery[redis]"
```

## Configuration

Configuration is easy, just configure the location of
your Redis database:

```
app.conf.broker_url = 'redis://localhost:6379/0'
```

Where the URL is in the format of:

```
redis://:password@hostname:port/db_number
```

all fields after the scheme are optional, and will default to `localhost`
on port 6379, using database 0.

If redis credential provider should be used, the URL needs to be in the following format:

```
redis://@hostname:port/db_number?credential_provider=mymodule.myfile.myclass
```

If a Unix socket connection should be used, the URL needs to be in the format:

```
redis+socket:///path/to/redis.sock
```

Specifying a different database number when using a Unix socket is possible
by adding the `virtual_host` parameter to the URL:

```
redis+socket:///path/to/redis.sock?virtual_host=db_number
```

It is also easy to connect directly to a list of Redis Sentinel:

```
app.conf.broker_url = 'sentinel://localhost:26379;sentinel://localhost:26380;sentinel://localhost:26381'
app.conf.broker_transport_options = { 'master_name': "cluster1" }
```

Additional options can be passed to the Sentinel client using `sentinel_kwargs`:

```
app.conf.broker_transport_options = { 'sentinel_kwargs': { 'password': "password" } }
```

### Visibility Timeout

The visibility timeout defines the number of seconds to wait
for the worker to acknowledge the task before the message is redelivered
to another worker. Be sure to see [Caveats](#redis-caveats) below.

This option is set via the [`broker_transport_options`](../../userguide/configuration.html#std-setting-broker_transport_options) setting:

```
app.conf.broker_transport_options = {'visibility_timeout': 3600}  # 1 hour.
```

The default visibility timeout for Redis is 1 hour.

### Results

If you also want to store the state and return values of tasks in Redis,
you should configure these settings:

```
app.conf.result_backend = 'redis://localhost:6379/0'
```

For a complete list of options supported by the Redis result backend, see
[Redis backend settings](../../userguide/configuration.html#conf-redis-result-backend).

If you are using Sentinel, you should specify the master\_name using the [`result_backend_transport_options`](../../userguide/configuration.html#std-setting-result_backend_transport_options) setting:

```
app.conf.result_backend_transport_options = {'master_name': "mymaster"}
```

#### Global keyprefix

The global key prefix will be prepended to all keys used for the result backend,
which can be useful when a redis database is shared by different users.
By default, no prefix is prepended.

To configure the global keyprefix for the Redis result backend, use the `global_keyprefix` key under [`result_backend_transport_options`](../../userguide/configuration.html#std-setting-result_backend_transport_options):

```
app.conf.result_backend_transport_options = {
    'global_keyprefix': 'my_prefix_'
}
```

#### Connection timeouts

To configure the connection timeouts for the Redis result backend, use the `retry_policy` key under [`result_backend_transport_options`](../../userguide/configuration.html#std-setting-result_backend_transport_options):

```
app.conf.result_backend_transport_options = {
    'retry_policy': {
       'timeout': 5.0
    }
}
```

See [`retry_over_time()`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.utils.functional.html#kombu.utils.functional.retry_over_time "(in Kombu v5.6)") for the possible retry policy options.

## Serverless

Celery supports utilizing a remote serverless Redis, which can significantly
reduce the operational overhead and cost, making it a favorable choice in
microservice architectures or environments where minimizing operational
expenses is crucial. Serverless Redis provides the necessary functionalities
without the need for manual setup, configuration, and management, thus
aligning well with the principles of automation and scalability that Celery promotes.

### Upstash

[Upstash](http://upstash.com/?code=celery) offers a serverless Redis database service,
providing a seamless solution for Celery users looking to leverage
serverless architectures. Upstash’s serverless Redis service is designed
with an eventual consistency model and durable storage, facilitated
through a multi-tier storage architecture.

Integration with Celery is straightforward as demonstrated
in an [example provided by Upstash](https://github.com/upstash/examples/tree/main/examples/using-celery).

### Dragonfly

[Dragonfly](https://www.dragonflydb.io/) is a drop-in Redis replacement that cuts costs and boosts performance.
Designed to fully utilize the power of modern cloud hardware and deliver on the data demands of modern applications,
Dragonfly frees developers from the limits of traditional in-memory data stores.

## Caveats

### Visibility timeout

If a task isn’t acknowledged within the [Visibility Timeout](#redis-visibility-timeout)
the task will be redelivered to another worker and executed.

This causes problems with ETA/countdown/retry tasks where the
time to execute exceeds the visibility timeout; in fact if that
happens it will be executed again, and again in a loop.

To remediate that, you can increase the visibility timeout to match
the time of the longest ETA you’re planning to use. However, this is not
recommended as it may have negative impact on the reliability.
Celery will redeliver messages at worker shutdown,
so having a long visibility timeout will only delay the redelivery
of ‘lost’ tasks in the event of a power failure or forcefully terminated
workers.

Broker is not a database, so if you are in need of scheduling tasks for
a more distant future, database-backed periodic task might be a better choice.
Periodic tasks won’t be affected by the visibility timeout,
as this is a concept separate from ETA/countdown.

You can increase this timeout by configuring all of the following options
with the same name (required to set all of them):

```
app.conf.broker_transport_options = {'visibility_timeout': 43200}
app.conf.result_backend_transport_options = {'visibility_timeout': 43200}
app.conf.visibility_timeout = 43200
```

The value must be an int describing the number of seconds.

Note: If multiple applications are sharing the same Broker, with different settings, the \_shortest\_ value will be used.
This include if the value is not set, and the default is sent

### Soft Shutdown

During [shutdown](../../userguide/workers.html#worker-stopping), the worker will attempt to re-queue any unacknowledged messages
with [`task_acks_late`](../../userguide/configuration.html#std-setting-task_acks_late) enabled. However, if the worker is terminated forcefully
([cold shutdown](../../userguide/workers.html#worker-cold-shutdown)), the worker might not be able to re-queue the tasks on time,
and they will not be consumed again until the [Visibility Timeout](#redis-visibility-timeout) has passed. This creates a
problem when the [Visibility Timeout](#redis-visibility-timeout) is very high and a worker needs to shut down just after it has
received a task. If the task is not re-queued in such case, it will need to wait for the long visibility timeout
to pass before it can be consumed again, leading to potentially very long delays in tasks execution.

The [soft shutdown](../../userguide/workers.html#worker-soft-shutdown) introduces a time-limited warm shutdown phase just before
the [cold shutdown](../../userguide/workers.html#worker-cold-shutdown). This time window significantly increases the chances of
re-queuing the tasks during shutdown which mitigates the problem of long visibility timeouts.

To enable the [soft shutdown](../../userguide/workers.html#worker-soft-shutdown), set the [`worker_soft_shutdown_timeout`](../../userguide/configuration.html#std-setting-worker_soft_shutdown_timeout) to a value
greater than 0. The value must be an float describing the number of seconds. During this time, the worker will
continue to process the running tasks until the timeout expires, after which the [cold shutdown](../../userguide/workers.html#worker-cold-shutdown)
will be initiated automatically to terminate the worker gracefully.

If the [REMAP\_SIGTERM](../../userguide/workers.html#worker-remap-sigterm) is configured to SIGQUIT in the environment variables, and
the [`worker_soft_shutdown_timeout`](../../userguide/configuration.html#std-setting-worker_soft_shutdown_timeout) is set, the worker will initiate the [soft shutdown](../../userguide/workers.html#worker-soft-shutdown)
when it receives the `TERM` signal (*and* the `QUIT` signal).

### Key eviction

Redis may evict keys from the database in some situations

If you experience an error like:

```
InconsistencyError: Probably the key ('_kombu.binding.celery') has been
removed from the Redis database.
```

then you may want to configure the **redis-server** to not evict keys
by setting in the redis configuration file:

- the `maxmemory` option
- the `maxmemory-policy` option to `noeviction` or `allkeys-lru`

See Redis server documentation about Eviction Policies for details:

> <https://redis.io/topics/lru-cache>

### Group result ordering

Versions of Celery up to and including 4.4.6 used an unsorted list to store
result objects for groups in the Redis backend. This can cause those results to
be returned in a different order to their associated tasks in the original
group instantiation. Celery 4.4.7 introduced an opt-in behaviour which fixes
this issue and ensures that group results are returned in the same order the
tasks were defined, matching the behaviour of other backends. In Celery 5.0
this behaviour was changed to be opt-out. The behaviour is controlled by the
result\_chord\_ordered configuration option which may be set like so:

```
# Specifying this for workers running Celery 4.4.6 or earlier has no effect
app.conf.result_backend_transport_options = {
    'result_chord_ordered': True    # or False
}
```

This is an incompatible change in the runtime behaviour of workers sharing the
same Redis backend for result storage, so all workers must follow either the
new or old behaviour to avoid breakage. For clusters with some workers running
Celery 4.4.6 or earlier, this means that workers running 4.4.7 need no special
configuration and workers running 5.0 or later must have result\_chord\_ordered
set to False. For clusters with no workers running 4.4.6 or earlier but some
workers running 4.4.7, it is recommended that result\_chord\_ordered be set to
True for all workers to ease future migration. Migration between behaviours
will disrupt results currently held in the Redis backend and cause breakage if
downstream tasks are run by migrated workers - plan accordingly.