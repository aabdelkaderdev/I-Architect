<!-- Source: https://docs.celeryq.dev/projects/pytest-celery/en/latest/reference/pytest_celery.vendors.redis.broker.html -->

This document describes the current stable version of pytest\_celery (1.3).
For development docs,
[go here](https://pytest-celery.readthedocs.io/en/main/reference/pytest_celery.vendors.redis.broker.html).

# pytest\_celery.vendors.redis.broker package

## Submodules

## pytest\_celery.vendors.redis.broker.api module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Redis Broker vendor.

*class* pytest\_celery.vendors.redis.broker.api.RedisTestBroker(*container: [CeleryTestContainer](pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")*, *app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)") = None*)[[source]](../_modules/pytest_celery/vendors/redis/broker/api.html#RedisTestBroker)
:   Bases: [`CeleryTestBroker`](pytest_celery.api.html#pytest_celery.api.broker.CeleryTestBroker "pytest_celery.api.broker.CeleryTestBroker")

## pytest\_celery.vendors.redis.broker.defaults module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Redis Broker vendor.

## pytest\_celery.vendors.redis.broker.fixtures module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Redis Broker vendor.

pytest\_celery.vendors.redis.broker.fixtures.celery\_redis\_broker(*default\_redis\_broker: [RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")*) → [RedisTestBroker](#pytest_celery.vendors.redis.broker.api.RedisTestBroker "pytest_celery.vendors.redis.broker.api.RedisTestBroker")[[source]](../_modules/pytest_celery/vendors/redis/broker/fixtures.html#celery_redis_broker)
:   Creates a RedisTestBroker instance. Responsible for tearing down the
    node.

    Parameters:
    :   **default\_redis\_broker** ([*RedisContainer*](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")) – Instantiated RedisContainer.

pytest\_celery.vendors.redis.broker.fixtures.default\_redis\_broker\_cls() → [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")][[source]](../_modules/pytest_celery/vendors/redis/broker/fixtures.html#default_redis_broker_cls)
:   Default Redis broker container class. Override to apply custom
    configuration globally.

    See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   API for managing the vendor’s container.

    Return type:
    :   [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")]

pytest\_celery.vendors.redis.broker.fixtures.default\_redis\_broker\_command(*default\_redis\_broker\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")]*) → [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")][[source]](../_modules/pytest_celery/vendors/redis/broker/fixtures.html#default_redis_broker_command)
:   Command to run the container.

    Parameters:
    :   **default\_redis\_broker\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*RedisContainer*](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Docker CMD instruction.

    Return type:
    :   [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")]

pytest\_celery.vendors.redis.broker.fixtures.default\_redis\_broker\_env(*default\_redis\_broker\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")]*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/redis/broker/fixtures.html#default_redis_broker_env)
:   Environment variables for this vendor.

    Parameters:
    :   **default\_rabbitmq\_broker\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*RedisContainer*](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Items to pass to the container’s environment.

    Return type:
    :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

pytest\_celery.vendors.redis.broker.fixtures.default\_redis\_broker\_image(*default\_redis\_broker\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")]*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/redis/broker/fixtures.html#default_redis_broker_image)
:   Sets the image name for this vendor.

    Parameters:
    :   **default\_rabbitmq\_broker\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*RedisContainer*](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Docker image name.

    Return type:
    :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

pytest\_celery.vendors.redis.broker.fixtures.default\_redis\_broker\_ports(*default\_redis\_broker\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RedisContainer](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")]*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/redis/broker/fixtures.html#default_redis_broker_ports)
:   Port bindings for this vendor.

    Parameters:
    :   **default\_redis\_broker\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*RedisContainer*](pytest_celery.vendors.redis.html#pytest_celery.vendors.redis.container.RedisContainer "pytest_celery.vendors.redis.container.RedisContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Port bindings.

    Return type:
    :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

## Module contents

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Redis Broker vendor.