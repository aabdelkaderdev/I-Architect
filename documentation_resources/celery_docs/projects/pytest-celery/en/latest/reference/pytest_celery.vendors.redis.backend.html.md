<!-- Source: https://docs.celeryq.dev/projects/pytest-celery/en/latest/reference/pytest_celery.vendors.redis.backend.html -->

This document describes the current stable version of pytest\_celery (1.3).
For development docs,
[go here](https://pytest-celery.readthedocs.io/en/main/reference/pytest_celery.vendors.redis.backend.html).

# pytest\_celery.vendors.redis.backend package

## Submodules

## pytest\_celery.vendors.redis.backend.api module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Redis Backend vendor.

*class* pytest\_celery.vendors.redis.backend.api.RedisTestBackend(*container: [CeleryTestContainer](pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")*, *app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)") = None*)[[source]](../_modules/pytest_celery/vendors/redis/backend/api.html#RedisTestBackend)
:   Bases: [`CeleryTestBackend`](pytest_celery.api.html#pytest_celery.api.backend.CeleryTestBackend "pytest_celery.api.backend.CeleryTestBackend")

    teardown() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/redis/backend/api.html#RedisTestBackend.teardown)
    :   When a test that has a AsyncResult object is finished there’s a race
        condition between the AsyncResult object and the Redis container.

        The AsyncResult object tries to release the connection but the
        Redis container has already exited.

## pytest\_celery.vendors.redis.backend.defaults module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Redis Backend vendor.

## pytest\_celery.vendors.redis.backend.fixtures module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Redis Backend vendor.

pytest\_celery.vendors.redis.backend.fixtures.celery\_redis\_backend(*default\_redis\_backend: [RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")*) → [RedisTestBackend](#pytest_celery.vendors.redis.backend.api.RedisTestBackend "pytest_celery.vendors.redis.backend.api.RedisTestBackend")[[source]](../_modules/pytest_celery/vendors/redis/backend/fixtures.html#celery_redis_backend)
:   Creates a RedisTestBackend instance. Responsible for tearing down the
    node.

    Parameters:
    :   **default\_redis\_backend** ([*RedisContainer*](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")) – Instantiated RedisContainer.

pytest\_celery.vendors.redis.backend.fixtures.default\_redis\_backend\_cls() → [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")][[source]](../_modules/pytest_celery/vendors/redis/backend/fixtures.html#default_redis_backend_cls)
:   Default Redis backend container class. Override to apply custom
    configuration globally.

    See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   API for managing the vendor’s container.

    Return type:
    :   [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")]

pytest\_celery.vendors.redis.backend.fixtures.default\_redis\_backend\_command(*default\_redis\_backend\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")]*) → [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")][[source]](../_modules/pytest_celery/vendors/redis/backend/fixtures.html#default_redis_backend_command)
:   Command to run the container.

    Parameters:
    :   **default\_redis\_backend\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*RedisContainer*](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Docker CMD instruction.

    Return type:
    :   [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")]

pytest\_celery.vendors.redis.backend.fixtures.default\_redis\_backend\_env(*default\_redis\_backend\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")]*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/redis/backend/fixtures.html#default_redis_backend_env)
:   Environment variables for this vendor.

    Parameters:
    :   **default\_rabbitmq\_broker\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*RedisContainer*](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Items to pass to the container’s environment.

    Return type:
    :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

pytest\_celery.vendors.redis.backend.fixtures.default\_redis\_backend\_image(*default\_redis\_backend\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")]*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/redis/backend/fixtures.html#default_redis_backend_image)
:   Sets the image name for this vendor.

    Parameters:
    :   **default\_rabbitmq\_broker\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*RedisContainer*](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Docker image name.

    Return type:
    :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

pytest\_celery.vendors.redis.backend.fixtures.default\_redis\_backend\_ports(*default\_redis\_backend\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")]*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/redis/backend/fixtures.html#default_redis_backend_ports)
:   Port bindings for this vendor.

    Parameters:
    :   **default\_redis\_backend\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*RedisContainer*](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Port bindings.

    Return type:
    :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

## Module contents

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Redis Backend vendor.