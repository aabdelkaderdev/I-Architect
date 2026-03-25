<!-- Source: https://docs.celeryq.dev/projects/pytest-celery/en/latest/reference/pytest_celery.vendors.worker.html -->

This document describes the current stable version of pytest\_celery (1.3).
For development docs,
[go here](https://pytest-celery.readthedocs.io/en/main/reference/pytest_celery.vendors.worker.html).

# pytest\_celery.vendors.worker package

## Subpackages

## Submodules

## pytest\_celery.vendors.worker.container module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the [Built-in Celery Worker](../getting-started/vendors.html#built-in-worker) vendor.

*class* pytest\_celery.vendors.worker.container.CeleryWorkerContainer(*container*)[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer)
:   Bases: [`CeleryTestContainer`](pytest_celery.api.html#pytest_celery.api.container.CeleryTestContainer "pytest_celery.api.container.CeleryTestContainer")

    This is the base class for all Celery worker containers. It is
    preconfigured for a built-in Celery worker image and should be customized
    for your own worker image.

    The purpose of this class is manipulating the container volume and
    configurations to warm up the worker container according to the test case requirements.

    Responsibility Scope:
    :   Prepare the worker container with the required filesystem, configurations and
        dependencies of your project.

    *classmethod* app\_module() → [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.app_module)
    :   A preconfigured module that contains the Celery app instance.

        The module is manipulated at runtime to inject the required
        configurations from the test case.

    *classmethod* buildargs() → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.buildargs)
    :   Build arguments for the built-in worker image.

    *classmethod* command(*\*args: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *debugpy: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*, *wait\_for\_client: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*, *\*\*kwargs: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*) → [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")][[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.command)
    :   Override the CMD instruction in the Dockerfile.

        This method should be overridden in derived classes to provide the
        specific command and its arguments required to start the container.

        Parameters:
        :   - **\*args** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Additional command-line arguments.
            - **debugpy** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Enable debugpy. Defaults to False.
            - **wait\_for\_client** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Wait for a debugger to be attached. Defaults to True.
            - **\*\*kwargs** ([*dict*](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")) – Additional keyword arguments.

        Raises:
        :   [**NotImplementedError**](https://docs.python.org/dev/library/exceptions.html#NotImplementedError "(in Python v3.15)") – Rely on the Dockerfile if not set otherwise by default.

        Returns:
        :   A list containing the command to run in the container as
            :   the first element, followed by the command-line arguments.

        Return type:
        :   [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")]

    *classmethod* initial\_content(*worker\_tasks: [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *worker\_signals: [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *worker\_app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *app\_module: [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *utils\_module: [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.initial_content)
    :   Defines the initial content of the worker container.

        See more: pytest\_docker\_tools.volume()

        Parameters:
        :   - **worker\_tasks** ([*set*](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)") *|* *None**,* *optional*) – Set of tasks modules. Defaults to None.
            - **worker\_signals** ([*set*](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)") *|* *None**,* *optional*) – Set of signals handlers modules. Defaults to None.
            - **worker\_app** (*Celery* *|* *None**,* *optional*) – Celery app instance. Defaults to None.
            - **app\_module** (*ModuleType* *|* *None**,* *optional*) – app module. Defaults to None.
            - **utils\_module** (*ModuleType* *|* *None**,* *optional*) – utils module. Defaults to None.

        Returns:
        :   Custom volume content for the worker container.

        Return type:
        :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

    *classmethod* initial\_env(*celery\_worker\_cluster\_config: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*, *initial: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.initial_env)
    :   Defines the environment variables for the worker container.

        See more: pytest\_docker\_tools.container()

        Parameters:
        :   - **celery\_worker\_cluster\_config** ([*dict*](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")) – Environment variables to set.
            - **initial** ([*dict*](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)") *|* *None**,* *optional*) – Additional variables. Defaults to None.

        Returns:
        :   Environment variables set for the worker container from the test case.

        Return type:
        :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

    *classmethod* log\_level() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.log_level)
    :   Celery worker log level.

    *classmethod* ports() → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.ports)
    :   Ports to expose from the worker container.

    *classmethod* pytest\_celery\_pkg() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.pytest_celery_pkg)
    :   The pytest-celery package to install in the worker container.

        Returns:
        :   pip install spec for pytest-celery.

        Return type:
        :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

    *property* ready\_prompt*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*
    :   A log string that indicates the container has finished starting up
        and is ready to use.

        Returns:
        :   A string to wait for or None for no wait. Defaults to None.

        Return type:
        :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | None

    *classmethod* signals\_modules() → [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.signals_modules)
    :   Signals handlers modules.

        This is an optional feature that can be used to inject signals
        handlers that needs to in the context of the worker container.

    *classmethod* tasks\_modules() → [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.tasks_modules)
    :   Tasks modules.

    *classmethod* utils\_module() → [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.utils_module)
    :   A utility helper module for running python code in the worker
        container context.

    *classmethod* version() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.version)
    :   Celery version to use for the worker container.

    *classmethod* worker\_name() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.worker_name)
    :   Celery worker name.

    *classmethod* worker\_queue() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/container.html#CeleryWorkerContainer.worker_queue)
    :   Celery worker queue.

## pytest\_celery.vendors.worker.defaults module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the [Built-in Celery Worker](../getting-started/vendors.html#built-in-worker) vendor.

## pytest\_celery.vendors.worker.fixtures module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the [Built-in Celery Worker](../getting-started/vendors.html#built-in-worker) vendor.

pytest\_celery.vendors.worker.fixtures.celery\_setup\_worker(*default\_worker\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryTestWorker](pytest_celery.api.html#pytest_celery.api.worker.CeleryTestWorker "pytest_celery.api.worker.CeleryTestWorker")]*, *default\_worker\_container: [CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*, *default\_worker\_app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)")*) → [CeleryTestWorker](pytest_celery.api.html#pytest_celery.api.worker.CeleryTestWorker "pytest_celery.api.worker.CeleryTestWorker")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#celery_setup_worker)
:   Creates a CeleryTestWorker instance. Responsible for tearing down the
    node.

    Parameters:
    :   - **default\_worker\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryTestWorker*](pytest_celery.api.html#pytest_celery.api.worker.CeleryTestWorker "pytest_celery.api.worker.CeleryTestWorker")*]*) – Interface class.
        - **default\_worker\_container** ([*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")) – Instantiated CeleryWorkerContainer.
        - **default\_worker\_app** (*Celery*) – Celery app instance.

pytest\_celery.vendors.worker.fixtures.default\_worker\_app(*celery\_setup\_app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)")*) → [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_app)
:   Celery app instance for this worker.

    Parameters:
    :   **celery\_setup\_app** (*Celery*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Celery app instance.

    Return type:
    :   Celery

pytest\_celery.vendors.worker.fixtures.default\_worker\_app\_module(*default\_worker\_container\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*) → [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_app_module)
:   App module for this worker.

    Parameters:
    :   **default\_worker\_container\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   App module.

    Return type:
    :   ModuleType

pytest\_celery.vendors.worker.fixtures.default\_worker\_celery\_log\_level(*default\_worker\_container\_session\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_celery_log_level)
:   Log level for this worker.

    Parameters:
    :   **default\_worker\_container\_session\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Log level.

    Return type:
    :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

pytest\_celery.vendors.worker.fixtures.default\_worker\_celery\_version(*default\_worker\_container\_session\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_celery_version)
:   Celery version for this worker.

    Parameters:
    :   **default\_worker\_container\_session\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Celery version.

    Return type:
    :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

pytest\_celery.vendors.worker.fixtures.default\_worker\_celery\_worker\_name(*default\_worker\_container\_session\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_celery_worker_name)
:   Name of the worker.

    Parameters:
    :   **default\_worker\_container\_session\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Worker name.

    Return type:
    :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

pytest\_celery.vendors.worker.fixtures.default\_worker\_celery\_worker\_queue(*default\_worker\_container\_session\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_celery_worker_queue)
:   Worker queue for this worker.

    Parameters:
    :   **default\_worker\_container\_session\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Worker queue.

    Return type:
    :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

pytest\_celery.vendors.worker.fixtures.default\_worker\_cls() → [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryTestWorker](pytest_celery.api.html#pytest_celery.api.worker.CeleryTestWorker "pytest_celery.api.worker.CeleryTestWorker")][[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_cls)
:   Default worker class. Override to apply custom configuration globally.

    See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   API for managing the vendor’s node.

    Return type:
    :   [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryTestWorker](pytest_celery.api.html#pytest_celery.api.worker.CeleryTestWorker "pytest_celery.api.worker.CeleryTestWorker")]

pytest\_celery.vendors.worker.fixtures.default\_worker\_command(*default\_worker\_container\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*) → [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")][[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_command)
:   Command to run the container.

    Parameters:
    :   **default\_worker\_container\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Docker CMD instruction.

    Return type:
    :   [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")]

pytest\_celery.vendors.worker.fixtures.default\_worker\_container\_cls() → [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")][[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_container_cls)
:   Default worker container class. Override to apply custom configuration
    globally.

    See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   API for managing the vendor’s container.

    Return type:
    :   [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]

pytest\_celery.vendors.worker.fixtures.default\_worker\_container\_session\_cls() → [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")][[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_container_session_cls)
:   Default worker container session class. Override to apply custom
    configuration globally.

    See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   API for managing the vendor’s container.

    Return type:
    :   [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]

pytest\_celery.vendors.worker.fixtures.default\_worker\_env(*default\_worker\_container\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*, *celery\_worker\_cluster\_config: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_env)
:   Environment variables for this worker.

    Parameters:
    :   - **default\_worker\_container\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).
        - **celery\_worker\_cluster\_config** ([*dict*](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")) – Broker & Backend clusters configuration.

    Returns:
    :   Items to pass to the container’s environment.

    Return type:
    :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

pytest\_celery.vendors.worker.fixtures.default\_worker\_initial\_content(*default\_worker\_container\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*, *default\_worker\_app\_module: [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)")*, *default\_worker\_utils\_module: [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)")*, *default\_worker\_tasks: [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")*, *default\_worker\_signals: [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")*, *default\_worker\_app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)")*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_initial_content)
:   Initial content for this worker’s volume.

    This is applied on a worker container when using the following volume configuration:

    ```
    default_worker_container = container(
        ...
        volumes={"{default_worker_volume.name}": DEFAULT_WORKER_VOLUME},
        ...
    )
    ```

    Note

    More volumes may be added additionally.

    Parameters:
    :   - **default\_worker\_container\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).
        - **default\_worker\_app\_module** (*ModuleType*) – App module to inject.
        - **default\_worker\_utils\_module** (*ModuleType*) – Utils module to inject.
        - **default\_worker\_tasks** ([*set*](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")) – Tasks modules to inject.
        - **default\_worker\_signals** ([*set*](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")) – Signals modules to inject.
        - **default\_worker\_app** (*Celery*) – Celery app to initialize the worker with.

    Returns:
    :   Initial volume content (dict of files).

    Return type:
    :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

pytest\_celery.vendors.worker.fixtures.default\_worker\_ports(*default\_worker\_container\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_ports)
:   Port bindings for this vendor.

    Parameters:
    :   **default\_worker\_container\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Port bindings.

    Return type:
    :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

pytest\_celery.vendors.worker.fixtures.default\_worker\_pytest\_celery\_pkg(*default\_worker\_container\_session\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_pytest_celery_pkg)
:   The pytest-celery package to install in the worker container.

    Parameters:
    :   **default\_worker\_container\_session\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   pip install spec for pytest-celery.

    Return type:
    :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

pytest\_celery.vendors.worker.fixtures.default\_worker\_signals(*default\_worker\_container\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*) → [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_signals)
:   Signals modules set for this worker.

    Parameters:
    :   **default\_worker\_container\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Signals modules.

    Return type:
    :   [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")

pytest\_celery.vendors.worker.fixtures.default\_worker\_tasks(*default\_worker\_container\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*) → [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_tasks)
:   Tasks modules set for this worker.

    Parameters:
    :   **default\_worker\_container\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Tasks modules.

    Return type:
    :   [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")

pytest\_celery.vendors.worker.fixtures.default\_worker\_utils\_module(*default\_worker\_container\_cls: [type](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")[[CeleryWorkerContainer](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")]*) → [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/fixtures.html#default_worker_utils_module)
:   Utils module for this worker.

    Parameters:
    :   **default\_worker\_container\_cls** ([*type*](https://docs.python.org/dev/library/functions.html#type "(in Python v3.15)")*[*[*CeleryWorkerContainer*](#pytest_celery.vendors.worker.container.CeleryWorkerContainer "pytest_celery.vendors.worker.container.CeleryWorkerContainer")*]*) – See also: [Vendor Class](../getting-started/vendors.html#vendor-class).

    Returns:
    :   Utils module.

    Return type:
    :   ModuleType

## pytest\_celery.vendors.worker.tasks module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the [Built-in Celery Worker](../getting-started/vendors.html#built-in-worker) vendor.

*(task)*pytest\_celery.vendors.worker.tasks.add(*x: 'int | float'*, *y: 'int | float'*, *z: 'int | float | None' = None*) → 'int | float'[[source]](../_modules/pytest_celery/vendors/worker/tasks.html#add)
:   Pytest-celery internal task.

    This task adds two or three numbers together.

    Parameters:
    :   - **x** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") *|* [*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – The first number.
        - **y** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") *|* [*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – The second number.
        - **z** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") *|* [*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") *|* *None**,* *optional*) – The third number. Defaults to None.

    Returns:
    :   The sum of the numbers.

    Return type:
    :   [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")

*(task)*pytest\_celery.vendors.worker.tasks.add\_replaced(*x: 'int | float'*, *y: 'int | float'*, *z: 'int | float | None' = None*, *\**, *queue: 'str | None' = None*) → 'None'[[source]](../_modules/pytest_celery/vendors/worker/tasks.html#add_replaced)
:   Pytest-celery internal task.

    This task replaces itself with the add task for the given arguments.

    Parameters:
    :   - **x** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") *|* [*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – The first number.
        - **y** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") *|* [*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – The second number.
        - **z** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") *|* [*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") *|* *None**,* *optional*) – The third number. Defaults to None.

    Raises:
    :   **Ignore** – Always raises Ignore.

*(task)*pytest\_celery.vendors.worker.tasks.fail(*\*args: 'tuple'*) → 'None'[[source]](../_modules/pytest_celery/vendors/worker/tasks.html#fail)
:   Pytest-celery internal task.

    This task raises a RuntimeError with the given arguments.

    Parameters:
    :   **\*args** ([*tuple*](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")) – Arguments to pass to the RuntimeError.

    Raises:
    :   [**RuntimeError**](https://docs.python.org/dev/library/exceptions.html#RuntimeError "(in Python v3.15)") – Always raises a RuntimeError.

*(task)*pytest\_celery.vendors.worker.tasks.identity(*x: 'Any'*) → 'Any'[[source]](../_modules/pytest_celery/vendors/worker/tasks.html#identity)
:   Pytest-celery internal task.

    This task returns the input as is.

    Parameters:
    :   **x** (*Any*) – Any value.

    Returns:
    :   The input value.

    Return type:
    :   Any

*(task)*pytest\_celery.vendors.worker.tasks.noop(*\*args: 'tuple'*, *\*\*kwargs: 'dict'*) → 'None'[[source]](../_modules/pytest_celery/vendors/worker/tasks.html#noop)
:   Pytest-celery internal task.

    This is a no-op task that does nothing.

    Returns:
    :   Always returns None.

    Return type:
    :   None

*(task)*pytest\_celery.vendors.worker.tasks.ping() → 'str'[[source]](../_modules/pytest_celery/vendors/worker/tasks.html#ping)
:   Pytest-celery internal task.

    Used to check if the worker is up and running.

    Returns:
    :   Always returns “pong”.

    Return type:
    :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

*(task)*pytest\_celery.vendors.worker.tasks.sleep(*seconds: 'float' = 1*, *\*\*kwargs: 'dict'*) → 'bool'[[source]](../_modules/pytest_celery/vendors/worker/tasks.html#sleep)
:   Pytest-celery internal task.

    This task sleeps for the given number of seconds.

    Parameters:
    :   - **seconds** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")*,* *optional*) – The number of seconds to sleep. Defaults to 1.
        - **\*\*kwargs** ([*dict*](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")) – Additional keyword arguments.

    Returns:
    :   Always returns True.

    Return type:
    :   [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")

*(task)*pytest\_celery.vendors.worker.tasks.xsum(*nums: 'Iterable'*) → 'int'[[source]](../_modules/pytest_celery/vendors/worker/tasks.html#xsum)
:   Pytest-celery internal task.

    This task sums a list of numbers, but also supports nested lists.

    Parameters:
    :   **nums** (*Iterable*) – A list of numbers or nested lists.

    Returns:
    :   The sum of the numbers.

    Return type:
    :   [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")

## pytest\_celery.vendors.worker.volume module

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the [Built-in Celery Worker](../getting-started/vendors.html#built-in-worker) vendor.

*class* pytest\_celery.vendors.worker.volume.WorkerInitialContent(*app\_module: [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *utils\_module: [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*)[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent)
:   Bases: [`object`](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")

    This class is responsible for generating the initial content for the
    worker container volume.

    Responsibility Scope:
    :   Prepare the worker container with the required filesystem, configurations and
        dependencies for your project.

    *class* Parser[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent.Parser)
    :   Bases: [`object`](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")

        Parser for the initial content of the worker container.

        app\_name(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent.Parser.app_name)
        :   Generates the Celery app initialization string.

            Parameters:
            :   **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") *|* *None**,* *optional*) – The app name. Defaults to None.

            Returns:
            :   app = Celery(name)

            Return type:
            :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

        config(*app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent.Parser.config)
        :   Generates the Celery app configuration changes.

            Parameters:
            :   **app** (*Celery* *|* *None**,* *optional*) – Celery app with possibly changed config. Defaults to None.

            Raises:
            :   [**TypeError**](https://docs.python.org/dev/library/exceptions.html#TypeError "(in Python v3.15)") – If the app.conf.changes property is not a dict.

            Returns:
            :   config = {key: value, …} or config = None

            Return type:
            :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

        imports\_src(*modules: [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")[[ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)")]*) → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent.Parser.imports_src)
        :   Parse the given modules and return a dict with the source code
            of the modules.

            Parameters:
            :   **modules** ([*set*](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")*[**ModuleType**]*) – A set of modules to parse.

            Returns:
            :   A dict with the source code of the modules.

            Return type:
            :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

        imports\_str(*modules: [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")[[ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)")]*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent.Parser.imports_str)
        :   Parse the given modules and return a string with the import
            statements.

            Parameters:
            :   **modules** ([*set*](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")*[**ModuleType**]*) – A set of modules to parse.

            Returns:
            :   “from module import \*” statements.

            Return type:
            :   [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

    add\_modules(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *modules: [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")[[ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)")]*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent.add_modules)
    :   Adds a set of modules to the initial content.

        Parameters:
        :   - **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Arbitrary unique name for the set of modules.
            - **modules** ([*set*](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")*[**ModuleType**]*) – A set of modules to add.

    generate() → [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent.generate)
    :   Generates the initial content for the worker container.

        Returns:
        :   Initial content volume for the worker container.

        Return type:
        :   [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")

    set\_app\_module(*app\_module: [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent.set_app_module)
    :   Injects an app module into the initial content.

    set\_app\_name(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent.set_app_name)
    :   Sets the Celery app name.

        Parameters:
        :   **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") *|* *None**,* *optional*) – The app name. Defaults to None.

    set\_config\_from\_object(*app: [Celery](https://docs.celeryq.dev/en/main/reference/celery.html#celery.Celery "(in Celery v5.6)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent.set_config_from_object)
    :   Sets the Celery app configuration from the given app.

        Parameters:
        :   **app** (*Celery* *|* *None**,* *optional*) – Celery app with possibly changed config. Defaults to None.

    set\_utils\_module(*utils\_module: [ModuleType](https://docs.python.org/dev/library/types.html#types.ModuleType "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/pytest_celery/vendors/worker/volume.html#WorkerInitialContent.set_utils_module)
    :   Injects a utils module into the initial content.

## Module contents

The pytest-celery plugin provides a set of built-in components called
[Vendors](../getting-started/vendors.html#vendors).

This module is part of the [Built-in Celery Worker](../getting-started/vendors.html#built-in-worker) vendor.