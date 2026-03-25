<!-- Source: https://docs.celeryq.dev/projects/pytest-celery/en/latest/reference/pytest_celery.vendors.rabbitmq.html -->

This document describes the current stable version of pytest\_celery (1.3).
For development docs,
[go here](https://pytest-celery.readthedocs.io/en/main/reference/pytest_celery.vendors.rabbitmq.html).

# pytest\_celery.vendors.rabbitmq package

## Submodules

## pytest\_celery.vendors.rabbitmq.api module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the RabbitMQ Broker vendor.

*class* pytest\_celery.vendors.rabbitmq.api.RabbitMQTestBroker(*container: [CeleryTestContainer](pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")*, *app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)") = None*)[[source]](../_modules/pytest_celery/vendors/rabbitmq/api.html#RabbitMQTestBroker)
:   Bases: [`CeleryTestBroker`](pytest_celery.api.html#pytest_celery.api.broker.CeleryTestBroker "pytest_celery.api.broker.CeleryTestBroker")

## pytest\_celery.vendors.rabbitmq.container module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the RabbitMQ Broker vendor.

*class* pytest\_celery.vendors.rabbitmq.container.RabbitMQContainer(*container*)[[source]](../_modules/pytest_celery/vendors/rabbitmq/container.html#RabbitMQContainer)
:   Bases: [`CeleryTestContainer`](pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")

    This class manages the lifecycle of a RabbitMQ container.

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

    *property* client*: [Connection](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.connection.html#kombu.connection.Connection "(in Kombu v5.6)")*
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

    *classmethod* image() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/rabbitmq/container.html#RabbitMQContainer.image)

    *classmethod* initial\_env() → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/rabbitmq/container.html#RabbitMQContainer.initial_env)

    *property* port*: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*

    *classmethod* ports() → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/rabbitmq/container.html#RabbitMQContainer.ports)

    *classmethod* prefix() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/rabbitmq/container.html#RabbitMQContainer.prefix)

    *property* ready\_prompt*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")*
    :   A log string that indicates the container has finished starting up
        and is ready to use.

        Returns:
        :   A string to wait for or None for no wait. Defaults to None.

        Return type:
        :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | None

    *property* url*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*

    *classmethod* version() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/rabbitmq/container.html#RabbitMQContainer.version)

    *property* vhost*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*

## pytest\_celery.vendors.rabbitmq.defaults module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the RabbitMQ Broker vendor.

## pytest\_celery.vendors.rabbitmq.fixtures module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the RabbitMQ Broker vendor.

pytest\_celery.vendors.rabbitmq.fixtures.celery\_rabbitmq\_broker(*default\_rabbitmq\_broker: [RabbitMQContainer](#pytest_celery.vendors.rabbitmq.container.RabbitMQContainer "pytest_celery.vendors.rabbitmq.container.RabbitMQContainer")*) → [RabbitMQTestBroker](#pytest_celery.vendors.rabbitmq.api.RabbitMQTestBroker "pytest_celery.vendors.rabbitmq.api.RabbitMQTestBroker")[[source]](../_modules/pytest_celery/vendors/rabbitmq/fixtures.html#celery_rabbitmq_broker)
:   Creates a RabbitMQTestBroker instance. Responsible for tearing down the
    node.

    Parameters:
    :   **default\_rabbitmq\_broker** ([*RabbitMQContainer*](#pytest_celery.vendors.rabbitmq.container.RabbitMQContainer "pytest_celery.vendors.rabbitmq.container.RabbitMQContainer")) – Instantiated RabbitMQContainer.

pytest\_celery.vendors.rabbitmq.fixtures.default\_rabbitmq\_broker\_cls() → [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RabbitMQContainer](#pytest_celery.vendors.rabbitmq.container.RabbitMQContainer "pytest_celery.vendors.rabbitmq.container.RabbitMQContainer")][[source]](../_modules/pytest_celery/vendors/rabbitmq/fixtures.html#default_rabbitmq_broker_cls)
:   Default RabbitMQ broker container class. Override to apply custom
    configuration globally.

    See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   API for managing the vendor’s container.

    Return type:
    :   [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RabbitMQContainer](#pytest_celery.vendors.rabbitmq.container.RabbitMQContainer "pytest_celery.vendors.rabbitmq.container.RabbitMQContainer")]

pytest\_celery.vendors.rabbitmq.fixtures.default\_rabbitmq\_broker\_env(*default\_rabbitmq\_broker\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RabbitMQContainer](#pytest_celery.vendors.rabbitmq.container.RabbitMQContainer "pytest_celery.vendors.rabbitmq.container.RabbitMQContainer")]*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/rabbitmq/fixtures.html#default_rabbitmq_broker_env)
:   Environment variables for this vendor.

    Parameters:
    :   **default\_rabbitmq\_broker\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*RabbitMQContainer*](#pytest_celery.vendors.rabbitmq.container.RabbitMQContainer "pytest_celery.vendors.rabbitmq.container.RabbitMQContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Items to pass to the container’s environment.

    Return type:
    :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

pytest\_celery.vendors.rabbitmq.fixtures.default\_rabbitmq\_broker\_image(*default\_rabbitmq\_broker\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RabbitMQContainer](#pytest_celery.vendors.rabbitmq.container.RabbitMQContainer "pytest_celery.vendors.rabbitmq.container.RabbitMQContainer")]*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/rabbitmq/fixtures.html#default_rabbitmq_broker_image)
:   Sets the image name for this vendor.

    Parameters:
    :   **default\_rabbitmq\_broker\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*RabbitMQContainer*](#pytest_celery.vendors.rabbitmq.container.RabbitMQContainer "pytest_celery.vendors.rabbitmq.container.RabbitMQContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Docker image name.

    Return type:
    :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

pytest\_celery.vendors.rabbitmq.fixtures.default\_rabbitmq\_broker\_ports(*default\_rabbitmq\_broker\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[RabbitMQContainer](#pytest_celery.vendors.rabbitmq.container.RabbitMQContainer "pytest_celery.vendors.rabbitmq.container.RabbitMQContainer")]*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/rabbitmq/fixtures.html#default_rabbitmq_broker_ports)
:   Port bindings for this vendor.

    Parameters:
    :   **default\_rabbitmq\_broker\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*RabbitMQContainer*](#pytest_celery.vendors.rabbitmq.container.RabbitMQContainer "pytest_celery.vendors.rabbitmq.container.RabbitMQContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Port bindings.

    Return type:
    :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

## Module contents

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the RabbitMQ Broker vendor.