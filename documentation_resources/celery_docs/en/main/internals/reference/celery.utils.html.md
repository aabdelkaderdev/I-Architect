<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.html).

# `celery.utils`

Utility functions.

Don’t import from here directly anymore, as these are only
here for backwards compatibility.

class celery.utils.cached\_property(*fget=None*, *fset=None*, *fdel=None*)[[source]](../../_modules/kombu/utils/objects.html#cached_property)
:   Implementation of Cached property.

    deleter(*fdel*)[[source]](../../_modules/kombu/utils/objects.html#cached_property.deleter)

    setter(*fset*)[[source]](../../_modules/kombu/utils/objects.html#cached_property.setter)

celery.utils.chunks(*it*, *n*)[[source]](../../_modules/celery/utils/functional.html#chunks)
:   Split an iterator into chunks with n elements each.

    Warning

    `it` must be an actual iterator, if you pass this a
    concrete sequence will get you repeating elements.

    So `chunks(iter(range(1000)), 10)` is fine, but
    `chunks(range(1000), 10)` is not.

    Example

    # n == 2
    >>> x = chunks(iter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 2)
    >>> list(x)
    [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10]]

    # n == 3
    >>> x = chunks(iter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 3)
    >>> list(x)
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10]]

celery.utils.gen\_task\_name(*app*, *name*, *module\_name*)[[source]](../../_modules/celery/utils/imports.html#gen_task_name)
:   Generate task name from name/module pair.

celery.utils.gen\_unique\_id(*\_uuid: Callable[[]*, *~uuid.UUID]=<function uuid4>*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")
:   Generate unique id in UUID4 format.

celery.utils.get\_cls\_by\_name(*name*, *aliases=None*, *imp=None*, *package=None*, *sep='.'*, *default=None*, *\*\*kwargs*)
:   Get symbol by qualified name.

    The name should be the full dot-separated path to the class:

    ```
    modulename.ClassName
    ```

    Example:

    ```
    celery.concurrency.processes.TaskPool
                                ^- class name
    ```

    or using ‘:’ to separate module and symbol:

    ```
    celery.concurrency.processes:TaskPool
    ```

    If aliases is provided, a dict containing short name/long name
    mappings, the name is looked up in the aliases first.

    Examples

    ```
    >>> symbol_by_name('celery.concurrency.processes.TaskPool')
    <class 'celery.concurrency.processes.TaskPool'>
    ```

    ```
    >>> symbol_by_name('default', {
    ...     'default': 'celery.concurrency.processes.TaskPool'})
    <class 'celery.concurrency.processes.TaskPool'>
    ```

    # Does not try to look up non-string names.
    >>> from celery.concurrency.processes import TaskPool
    >>> symbol\_by\_name(TaskPool) is TaskPool
    True

celery.utils.get\_full\_cls\_name(*obj*)
:   Return object name.

celery.utils.import\_from\_cwd(*module*, *imp=None*, *package=None*)[[source]](../../_modules/celery/utils/imports.html#import_from_cwd)
:   Import module, temporarily including modules in the current directory.

    Modules located in the current directory has
    precedence over modules located in sys.path.

celery.utils.instantiate(*name*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/imports.html#instantiate)
:   Instantiate class by name.

    See also

    `symbol_by_name()`.

celery.utils.memoize(*maxsize=None*, *keyfun=None*, *Cache=<class 'kombu.utils.functional.LRUCache'>*)[[source]](../../_modules/kombu/utils/functional.html#memoize)
:   Decorator to cache function return value.

celery.utils.nodename(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *hostname: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/nodenames.html#nodename)
:   Create node name from name/hostname pair.

celery.utils.nodesplit(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)"), [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")] | [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")][[source]](../../_modules/celery/utils/nodenames.html#nodesplit)
:   Split node name into tuple of name/hostname.

celery.utils.noop(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/functional.html#noop)
:   No operation.

    Takes any arguments/keyword arguments and does nothing.

celery.utils.uuid(*\_uuid: Callable[[]*, *~uuid.UUID]=<function uuid4>*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/kombu/utils/uuid.html#uuid)
:   Generate unique id in UUID4 format.

celery.utils.worker\_direct(*hostname: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [Queue](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)")*) → [Queue](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)")[[source]](../../_modules/celery/utils/nodenames.html#worker_direct)
:   Return the [`kombu.Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") being a direct route to a worker.

    Parameters:
    :   **hostname** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*Queue*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)")) – The fully qualified node name of
        a worker (e.g., `w1@example.com`). If passed a
        [`kombu.Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") instance it will simply return
        that instead.