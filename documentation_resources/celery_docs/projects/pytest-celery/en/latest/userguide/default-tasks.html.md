<!-- Source: https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/default-tasks.html -->

This document describes the current stable version of pytest\_celery (1.3).
For development docs,
[go here](https://pytest-celery.readthedocs.io/en/main/userguide/default-tasks.html).

# Built-in Tasks

Release:
:   1.3

Date:
:   Mar 24, 2026

The plugin provides a list of built-in celery tasks that can be used out of the box. This page will
list all the available tasks.

To import the tasks, you can use the following code:

```
from pytest_celery import the, tasks, you, want
```

or

```
from pytest_celery.vendors.worker import tasks
```

Tip

The tasks are injected into the workers that use the default volume with:

```
volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
```

## 

Added in version 1.0.0.

pytest\_celery.vendors.worker.tasks

```
@shared_task
def add(x: int | float, y: int | float, z: int | float | None = None) -> int | float:
    """Pytest-celery internal task.

    This task adds two or three numbers together.

    Args:
        x (int | float): The first number.
        y (int | float): The second number.
        z (int | float | None, optional): The third number. Defaults to None.

    Returns:
        int | float: The sum of the numbers.
    """
    if z:
        return x + y + z
    else:
        return x + y
```

## 

Added in version 1.0.0.

pytest\_celery.vendors.worker.tasks

```
@shared_task(bind=True)
def add_replaced(
    self: Task,
    x: int | float,
    y: int | float,
    z: int | float | None = None,
    *,
    queue: str | None = None,
) -> None:
    """Pytest-celery internal task.

    This task replaces itself with the add task for the given arguments.

    Args:
        x (int | float): The first number.
        y (int | float): The second number.
        z (int | float | None, optional): The third number. Defaults to None.

    Raises:
        Ignore: Always raises Ignore.
    """
    queue = queue or "celery"
    raise self.replace(add.s(x, y, z).set(queue=queue))
```

## 

Added in version 1.0.0.

pytest\_celery.vendors.worker.tasks

```
@shared_task
def fail(*args: tuple) -> None:
    """Pytest-celery internal task.

    This task raises a RuntimeError with the given arguments.

    Args:
        *args (tuple): Arguments to pass to the RuntimeError.

    Raises:
        RuntimeError: Always raises a RuntimeError.
    """
    args = (("Task expected to fail",) + args,)
    raise RuntimeError(*args)
```

## 

Added in version 1.0.0.

pytest\_celery.vendors.worker.tasks

```
@shared_task
def identity(x: Any) -> Any:
    """Pytest-celery internal task.

    This task returns the input as is.

    Args:
        x (Any): Any value.

    Returns:
        Any: The input value.
    """
    return x
```

## 

Added in version 1.0.0.

pytest\_celery.vendors.worker.tasks

```
@shared_task
def noop(*args: tuple, **kwargs: dict) -> None:
    """Pytest-celery internal task.

    This is a no-op task that does nothing.

    Returns:
        None: Always returns None.
    """
    return celery.utils.noop(*args, **kwargs)
```

## 

Added in version 1.0.0.

pytest\_celery.vendors.worker.tasks

```
@shared_task
def ping() -> str:
    """Pytest-celery internal task.

    Used to check if the worker is up and running.

    Returns:
        str: Always returns "pong".
    """
    return "pong"
```

## 

Added in version 1.0.0.

pytest\_celery.vendors.worker.tasks

```
@shared_task
def sleep(seconds: float = 1, **kwargs: dict) -> bool:
    """Pytest-celery internal task.

    This task sleeps for the given number of seconds.

    Args:
        seconds (float, optional): The number of seconds to sleep. Defaults to 1.
        **kwargs (dict): Additional keyword arguments.

    Returns:
        bool: Always returns True.
    """
    time.sleep(seconds, **kwargs)
    return True
```

## 

Added in version 1.0.0.

pytest\_celery.vendors.worker.tasks

```
@shared_task
def xsum(nums: Iterable) -> int:
    """Pytest-celery internal task.

    This task sums a list of numbers, but also supports nested lists.

    Args:
        nums (Iterable): A list of numbers or nested lists.

    Returns:
        int: The sum of the numbers.
    """
    return sum(sum(num) if isinstance(num, Iterable) else num for num in nums)
```