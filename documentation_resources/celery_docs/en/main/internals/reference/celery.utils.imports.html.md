<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.imports.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.imports.html).

# `celery.utils.imports`

Utilities related to importing modules and symbols by name.

exception celery.utils.imports.NotAPackage[[source]](../../_modules/celery/utils/imports.html#NotAPackage)
:   Raised when importing a package, but it’s not a package.

celery.utils.imports.cwd\_in\_path()[[source]](../../_modules/celery/utils/imports.html#cwd_in_path)
:   Context adding the current working directory to sys.path.

celery.utils.imports.find\_module(*module*, *path=None*, *imp=None*)[[source]](../../_modules/celery/utils/imports.html#find_module)
:   Version of `imp.find_module()` supporting dots.

celery.utils.imports.gen\_task\_name(*app*, *name*, *module\_name*)[[source]](../../_modules/celery/utils/imports.html#gen_task_name)
:   Generate task name from name/module pair.

celery.utils.imports.import\_from\_cwd(*module*, *imp=None*, *package=None*)[[source]](../../_modules/celery/utils/imports.html#import_from_cwd)
:   Import module, temporarily including modules in the current directory.

    Modules located in the current directory has
    precedence over modules located in sys.path.

celery.utils.imports.instantiate(*name*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/imports.html#instantiate)
:   Instantiate class by name.

    See also

    [`symbol_by_name()`](#celery.utils.imports.symbol_by_name "celery.utils.imports.symbol_by_name").

celery.utils.imports.module\_file(*module*)[[source]](../../_modules/celery/utils/imports.html#module_file)
:   Return the correct original file name of a module.

celery.utils.imports.qualname(*obj*)[[source]](../../_modules/celery/utils/imports.html#qualname)
:   Return object name.

celery.utils.imports.reload\_from\_cwd(*module*, *reloader=None*)[[source]](../../_modules/celery/utils/imports.html#reload_from_cwd)
:   Reload module (ensuring that CWD is in sys.path).

celery.utils.imports.symbol\_by\_name(*name*, *aliases=None*, *imp=None*, *package=None*, *sep='.'*, *default=None*, *\*\*kwargs*)[[source]](../../_modules/kombu/utils/imports.html#symbol_by_name)
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