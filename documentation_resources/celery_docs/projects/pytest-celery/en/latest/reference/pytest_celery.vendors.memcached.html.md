<!-- Source: https://docs.celeryq.dev/projects/pytest-celery/en/latest/reference/pytest_celery.vendors.memcached.html -->

This document describes the current stable version of pytest\_celery (1.3).
For development docs,
[go here](https://pytest-celery.readthedocs.io/en/main/reference/pytest_celery.vendors.memcached.html).

# pytest\_celery.vendors.memcached package

## Submodules

## pytest\_celery.vendors.memcached.api module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Memcached Backend vendor.

*class* pytest\_celery.vendors.memcached.api.MemcachedTestBackend(*container: [CeleryTestContainer](pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")*, *app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)") = None*)[[source]](../_modules/pytest_celery/vendors/memcached/api.html#MemcachedTestBackend)
:   Bases: [`CeleryTestBackend`](pytest_celery.api.html#pytest_celery.api.backend.CeleryTestBackend "pytest_celery.api.backend.CeleryTestBackend")

## pytest\_celery.vendors.memcached.container module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Memcached Backend vendor.

*class* pytest\_celery.vendors.memcached.container.MemcachedContainer(*container*)[[source]](../_modules/pytest_celery/vendors/memcached/container.html#MemcachedContainer)
:   Bases: [`CeleryTestContainer`](pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")

    This class manages the lifecycle of a Memcached container.

    *property* celeryconfig*: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*
    :   Each container is responsible for providing the configuration values
        required for Celery. This property should be implemented to return the
        configuration values for the specific container.

        Raises:
        :   [**NotImplementedError**](https://docs.python.org/dev/library/exceptions.html#NotImplementedError "(in Python v3.15)") – There is no config available by default.

        Returns:
        :   Configuration values required for Celery.

        Return type:
        :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

    *property* client*: Client*
    :   Provides an API client for interacting with the container, if
        available.

        Subclasses should implement this to return an instance of the client
        specific to the service running in the container.

        Raises:
        :   [**NotImplementedError**](https://docs.python.org/dev/library/exceptions.html#NotImplementedError "(in Python v3.15)") – There is not client available by default.

        Returns:
        :   Client instance.

        Return type:
        :   Any

    *property* host\_url*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*

    *property* hostname*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*

    *classmethod* image() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/memcached/container.html#MemcachedContainer.image)

    *classmethod* initial\_env() → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/memcached/container.html#MemcachedContainer.initial_env)

    *property* port*: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*

    *classmethod* ports() → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/memcached/container.html#MemcachedContainer.ports)

    *classmethod* prefix() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/memcached/container.html#MemcachedContainer.prefix)

    *property* url*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*

    *classmethod* version() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/memcached/container.html#MemcachedContainer.version)

## pytest\_celery.vendors.memcached.defaults module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Memcached Backend vendor.

## pytest\_celery.vendors.memcached.fixtures module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Memcached Backend vendor.

pytest\_celery.vendors.memcached.fixtures.celery\_memcached\_backend(*default\_memcached\_backend: [MemcachedContainer](#pytest_celery.vendors.memcached.container.MemcachedContainer "pytest_celery.vendors.memcached.container.MemcachedContainer")*) → [MemcachedTestBackend](#pytest_celery.vendors.memcached.api.MemcachedTestBackend "pytest_celery.vendors.memcached.api.MemcachedTestBackend")[[source]](../_modules/pytest_celery/vendors/memcached/fixtures.html#celery_memcached_backend)
:   Creates a MemcachedTestBackend instance. Responsible for tearing down
    the node.

    Parameters:
    :   **default\_memcached\_backend** ([*MemcachedContainer*](#pytest_celery.vendors.memcached.container.MemcachedContainer "pytest_celery.vendors.memcached.container.MemcachedContainer")) – Instantiated MemcachedContainer.

pytest\_celery.vendors.memcached.fixtures.default\_memcached\_backend\_cls() → [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[MemcachedContainer](#pytest_celery.vendors.memcached.container.MemcachedContainer "pytest_celery.vendors.memcached.container.MemcachedContainer")][[source]](../_modules/pytest_celery/vendors/memcached/fixtures.html#default_memcached_backend_cls)
:   Default Memcached backend container class. Override to apply custom
    configuration globally.

    See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   API for managing the vendor’s container.

    Return type:
    :   [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[MemcachedContainer](#pytest_celery.vendors.memcached.container.MemcachedContainer "pytest_celery.vendors.memcached.container.MemcachedContainer")]

pytest\_celery.vendors.memcached.fixtures.default\_memcached\_backend\_env(*default\_memcached\_backend\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[MemcachedContainer](#pytest_celery.vendors.memcached.container.MemcachedContainer "pytest_celery.vendors.memcached.container.MemcachedContainer")]*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/memcached/fixtures.html#default_memcached_backend_env)
:   Environment variables for this vendor.

    Parameters:
    :   **default\_memcached\_backend\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*MemcachedContainer*](#pytest_celery.vendors.memcached.container.MemcachedContainer "pytest_celery.vendors.memcached.container.MemcachedContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Items to pass to the container’s environment.

    Return type:
    :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

pytest\_celery.vendors.memcached.fixtures.default\_memcached\_backend\_image(*default\_memcached\_backend\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[MemcachedContainer](#pytest_celery.vendors.memcached.container.MemcachedContainer "pytest_celery.vendors.memcached.container.MemcachedContainer")]*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/memcached/fixtures.html#default_memcached_backend_image)
:   Docker image for this vendor.

    Parameters:
    :   **default\_memcached\_backend\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*MemcachedContainer*](#pytest_celery.vendors.memcached.container.MemcachedContainer "pytest_celery.vendors.memcached.container.MemcachedContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Docker image name.

    Return type:
    :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

pytest\_celery.vendors.memcached.fixtures.default\_memcached\_backend\_ports(*default\_memcached\_backend\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[MemcachedContainer](#pytest_celery.vendors.memcached.container.MemcachedContainer "pytest_celery.vendors.memcached.container.MemcachedContainer")]*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/memcached/fixtures.html#default_memcached_backend_ports)
:   Port bindings for this vendor.

    Parameters:
    :   **default\_memcached\_backend\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*MemcachedContainer*](#pytest_celery.vendors.memcached.container.MemcachedContainer "pytest_celery.vendors.memcached.container.MemcachedContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Port bindings.

    Return type:
    :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

## Module contents

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the Memcached Backend vendor.