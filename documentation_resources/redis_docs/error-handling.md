<!-- Source: https://redis.io/docs/latest/develop/clients/redis-py/error-handling -->

# Error handling

Learn how to handle errors when using redis-py

redis-py uses **exceptions** to signal errors. The redis-py documentation mainly
shows the "happy path" in code examples and omits error handling for brevity.
This page explains how
redis-py's error handling works and how to apply common error handling patterns.
For an overview of error types and handling strategies, see
[Error handling](/docs/latest/develop/clients/error-handling/).
See also [Production usage](/docs/latest/develop/clients/redis-py/produsage/)
for more information on connection management, timeouts, and other aspects of
app reliability.

## Exception hierarchy

redis-py organizes exceptions in a hierarchy. The base exception is `redis.RedisError`, with specific subclasses for different error types, as shown below:

```
"RedisError":
    _meta:
        description: "Base class for all redis-py exceptions"
    "ConnectionError":
        "TimeoutError":
        "BusyLoadingError":
    "ResponseError":
    "InvalidResponse":
    "DataError":
    "PubSubError":
    "...":
        _meta:
            ellipsis: true
            description: "Other exception types"
```

### Key exceptions

The following exceptions are the most commonly encountered in redis-py applications.
See
[Categories of errors](/docs/latest/develop/clients/error-handling/#categories-of-errors)
for a more detailed discussion of these errors and their causes.

| Exception | When it occurs | Recoverable | Recommended action |
| --- | --- | --- | --- |
| `redis.ConnectionError` | Network or connection issues | â | Retry with backoff or fall back to alternative |
| `redis.TimeoutError` | Operation exceeded timeout | â | Retry with backoff |
| `redis.ResponseError` | Invalid command or Redis error response | â | Fix the command or arguments |
| `redis.DataError` | Data serialization/deserialization issues | â ï¸ | Log, invalidate cache, fetch fresh data |

## Applying error handling patterns

The [Error handling](/docs/latest/develop/clients/error-handling/) overview
describes four main patterns. The sections below show how to implement them in
redis-py:

### Pattern 1: Fail fast

Catch specific exceptions that represent unrecoverable errors and re-raise them (see
[Pattern 1: Fail fast](/docs/latest/develop/clients/error-handling/#pattern-1-fail-fast)
for a full description):

```
import redis

r = redis.Redis()

try:
    result = r.get(key)
except redis.ResponseError:
    # This indicates a bug in the code
    raise
```

### Pattern 2: Graceful degradation

Catch connection errors and fall back to an alternative (see
[Pattern 2: Graceful degradation](/docs/latest/develop/clients/error-handling/#pattern-2-graceful-degradation)
for a full description):

```
try:
    cached_value = r.get(key)
    if cached_value:
        return cached_value
except redis.ConnectionError:
    logger.warning("Cache unavailable, using database")

# Fallback to database
return database.get(key)
```

### Pattern 3: Retry with backoff

Retry on temporary errors like timeouts (see
[Pattern 3: Retry with backoff](/docs/latest/develop/clients/error-handling/#pattern-3-retry-with-backoff)
for a full description). redis-py has built-in retry logic
which is highly configurable. You can customize the retry strategy
(or supply your own custom strategy) and you can also specify which errors
should be retried. See
[Production usage](/docs/latest/develop/clients/redis-py/produsage/#retries)
for more information.

### Pattern 4: Log and continue

Log non-critical errors and continue (see
[Pattern 4: Log and continue](/docs/latest/develop/clients/error-handling/#pattern-4-log-and-continue)
for a full description):

```
try:
    r.setex(key, 3600, value)
except redis.ConnectionError:
    logger.warning(f"Failed to cache {key}, continuing without cache")
    # Application continues normally
```

## Async error handling

Error handling works the usual way when you use `async`/`await`,
as shown in the example below:

```
import redis.asyncio as redis

async def get_with_fallback(key):
    r = await redis.from_url("redis://localhost")
    try:
        return await r.get(key)
    except redis.ConnectionError:
        logger.warning("Cache unavailable")
        return await database.get(key)
    finally:
        await r.close()
```

## See also

- [Error handling](/docs/latest/develop/clients/error-handling/)
- [Production usage](/docs/latest/develop/clients/redis-py/produsage/)

RATE THIS PAGE

★

★

★

★

★

[Back to top â](#)

Submit

## On this page