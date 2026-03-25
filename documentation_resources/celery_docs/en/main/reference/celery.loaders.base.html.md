<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.loaders.base.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.loaders.base.html).

# `celery.loaders.base`

Loader base class.

class celery.loaders.base.BaseLoader(*app*, *\*\*kwargs*)[[source]](../_modules/celery/loaders/base.html#BaseLoader)
:   Base class for loaders.

    Loaders handles,

    > - Reading celery client/worker configurations.
    > - What happens when a task starts?
    >   :   See [`on_task_init()`](#celery.loaders.base.BaseLoader.on_task_init "celery.loaders.base.BaseLoader.on_task_init").
    > - What happens when the worker starts?
    >   :   See [`on_worker_init()`](#celery.loaders.base.BaseLoader.on_worker_init "celery.loaders.base.BaseLoader.on_worker_init").
    > - What happens when the worker shuts down?
    >   :   See [`on_worker_shutdown()`](#celery.loaders.base.BaseLoader.on_worker_shutdown "celery.loaders.base.BaseLoader.on_worker_shutdown").
    > - What modules are imported to find tasks?

    autodiscover\_tasks(*packages*, *related\_name='tasks'*)[[source]](../_modules/celery/loaders/base.html#BaseLoader.autodiscover_tasks)

    builtin\_modules = frozenset({})

    cmdline\_config\_parser(*args*, *namespace='celery'*, *re\_type=re.compile('\\((\\w+)\\)')*, *extra\_types=None*, *override\_types=None*)[[source]](../_modules/celery/loaders/base.html#BaseLoader.cmdline_config_parser)

    property conf
    :   Loader configuration.

    config\_from\_object(*obj*, *silent=False*)[[source]](../_modules/celery/loaders/base.html#BaseLoader.config_from_object)

    configured = False

    property default\_modules

    find\_module(*module*)[[source]](../_modules/celery/loaders/base.html#BaseLoader.find_module)

    import\_default\_modules()[[source]](../_modules/celery/loaders/base.html#BaseLoader.import_default_modules)

    import\_from\_cwd(*module*, *imp=None*, *package=None*)[[source]](../_modules/celery/loaders/base.html#BaseLoader.import_from_cwd)

    import\_module(*module*, *package=None*)[[source]](../_modules/celery/loaders/base.html#BaseLoader.import_module)

    import\_task\_module(*module*)[[source]](../_modules/celery/loaders/base.html#BaseLoader.import_task_module)

    init\_worker()[[source]](../_modules/celery/loaders/base.html#BaseLoader.init_worker)

    init\_worker\_process()[[source]](../_modules/celery/loaders/base.html#BaseLoader.init_worker_process)

    now(*utc=True*)[[source]](../_modules/celery/loaders/base.html#BaseLoader.now)

    on\_process\_cleanup()[[source]](../_modules/celery/loaders/base.html#BaseLoader.on_process_cleanup)
    :   Called after a task is executed.

    on\_task\_init(*task\_id*, *task*)[[source]](../_modules/celery/loaders/base.html#BaseLoader.on_task_init)
    :   Called before a task is executed.

    on\_worker\_init()[[source]](../_modules/celery/loaders/base.html#BaseLoader.on_worker_init)
    :   Called when the worker (**celery worker**) starts.

    on\_worker\_process\_init()[[source]](../_modules/celery/loaders/base.html#BaseLoader.on_worker_process_init)
    :   Called when a child process starts.

    on\_worker\_shutdown()[[source]](../_modules/celery/loaders/base.html#BaseLoader.on_worker_shutdown)
    :   Called when the worker (**celery worker**) shuts down.

    override\_backends = {}

    read\_configuration(*env='CELERY\_CONFIG\_MODULE'*)[[source]](../_modules/celery/loaders/base.html#BaseLoader.read_configuration)

    shutdown\_worker()[[source]](../_modules/celery/loaders/base.html#BaseLoader.shutdown_worker)

    worker\_initialized = False