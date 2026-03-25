<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.html).

# [`celery`](#module-celery "celery: Distributed processing") — Distributed processing

---

This module is the main entry-point for the Celery API.
It includes commonly needed things for calling tasks,
and creating Celery applications.

|  |  |
| --- | --- |
| [`Celery`](#celery.Celery "celery.Celery") | Celery application instance |
| [`group`](#celery.group "celery.group") | group tasks together |
| [`chain`](#celery.chain "celery.chain") | chain tasks together |
| [`chord`](#celery.chord "celery.chord") | chords enable callbacks for groups |
| [`signature()`](#celery.signature "celery.signature") | create a new task signature |
| [`Signature`](#celery.Signature "celery.Signature") | object describing a task invocation |
| [`current_app`](#celery.current_app "celery.current_app") | proxy to the current application instance |
| [`current_task`](#celery.current_task "celery.current_task") | proxy to the currently executing task |

## [`Celery`](#celery.Celery "celery.Celery") application objects

Added in version 2.5.

class celery.Celery(*main=None*, *loader=None*, *backend=None*, *amqp=None*, *events=None*, *log=None*, *control=None*, *set\_as\_current=True*, *tasks=None*, *broker=None*, *include=None*, *changes=None*, *config\_source=None*, *fixups=None*, *task\_cls=None*, *autofinalize=True*, *namespace=None*, *strict\_typing=True*, *\*\*kwargs*)[[source]](../_modules/celery/app/base.html#Celery)
:   Celery application.

    Parameters:
    :   **main** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of the main module if running as \_\_main\_\_.
        This is used as the prefix for auto-generated task names.

    Keyword Arguments:
    :   - **broker** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – URL of the default broker used.
        - **backend** (*Union**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *Type**[**celery.backends.base.Backend**]**]*) –

          The result store backend class, or the name of the backend
          class to use.

          Default is the value of the [`result_backend`](../userguide/configuration.html#std-setting-result_backend) setting.
        - **autofinalize** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If set to False a [`RuntimeError`](https://docs.python.org/dev/library/exceptions.html#RuntimeError "(in Python v3.15)")
          will be raised if the task registry or tasks are used before
          the app is finalized.
        - **set\_as\_current** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Make this the global current app.
        - **include** (*List**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – List of modules every worker should import.
        - **amqp** (*Union**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *Type**[*[*AMQP*](celery.app.amqp.html#celery.app.amqp.AMQP "celery.app.amqp.AMQP")*]**]*) – AMQP object or class name.
        - **events** (*Union**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *Type**[*[*celery.app.events.Events*](celery.app.events.html#celery.app.events.Events "celery.app.events.Events")*]**]*) – Events object or
          class name.
        - **log** (*Union**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *Type**[*[*Logging*](celery.app.log.html#celery.app.log.Logging "celery.app.log.Logging")*]**]*) – Log object or class name.
        - **control** (*Union**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *Type**[*[*celery.app.control.Control*](celery.app.control.html#celery.app.control.Control "celery.app.control.Control")*]**]*) – Control object
          or class name.
        - **tasks** (*Union**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *Type**[*[*TaskRegistry*](celery.app.registry.html#celery.app.registry.TaskRegistry "celery.app.registry.TaskRegistry")*]**]*) – A task registry, or the name of
          a registry class.
        - **fixups** (*List**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – List of fix-up plug-ins (e.g., see
          `celery.fixups.django`).
        - **config\_source** (*Union**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *class**]*) – Take configuration from a class,
          or object. Attributes may include any settings described in
          the documentation.
        - **task\_cls** (*Union**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *Type**[*[*celery.app.task.Task*](celery.app.task.html#celery.app.task.Task "celery.app.task.Task")*]**]*) – base task class to
          use. See [this section](../userguide/tasks.html#custom-task-cls-app-wide) for usage.

    user\_options = None
    :   Custom options for command-line programs.
        See [Adding new command-line options](../userguide/extending.html#extending-commandoptions)

    steps = None
    :   Custom bootsteps to extend and modify the worker.
        See [Installing Bootsteps](../userguide/extending.html#extending-bootsteps).

    current\_task
    :   Instance of task being executed, or `None`.

    current\_worker\_task
    :   The task currently being executed by a worker or `None`.

        Differs from [`current_task`](#celery.current_task "celery.current_task") in that it’s not affected
        by tasks calling other tasks directly, or eagerly.

    amqp
    :   [`amqp`](celery.app.amqp.html#celery.app.amqp.AMQP "celery.app.amqp.AMQP").

        Type:
        :   AMQP related functionality

    backend
    :   Current backend instance.

    loader
    :   Current loader instance.

    control
    :   [`control`](celery.app.control.html#celery.app.control.Control "celery.app.control.Control").

        Type:
        :   Remote control

    events
    :   `events`.

        Type:
        :   Consuming and sending events

    log
    :   [`log`](celery.app.log.html#celery.app.log.Logging "celery.app.log.Logging").

        Type:
        :   [Logging](celery.app.log.html#celery.app.log.Logging "celery.app.log.Logging")

    tasks
    :   Task registry.

        Warning

        Accessing this attribute will also auto-finalize the app.

    pool
    :   `pool`.

        Note

        This attribute is not related to the workers concurrency pool.

        Type:
        :   Broker connection pool

    producer\_pool

    Task
    :   Base task class for this app.

    timezone
    :   Current timezone for this app.

        This is a cached property taking the time zone from the
        [`timezone`](../userguide/configuration.html#std-setting-timezone) setting.

    builtin\_fixups = {'celery.fixups.django:fixup'}

    oid
    :   Universally unique identifier for this app.

    close()[[source]](../_modules/celery/app/base.html#Celery.close)
    :   Clean up after the application.

        Only necessary for dynamically created apps, and you should
        probably use the [`with`](https://docs.python.org/dev/reference/compound_stmts.html#with "(in Python v3.15)") statement instead.

        Example

        ```
        >>> with Celery(set_as_current=False) as app:
        ...     with app.connection_for_write() as conn:
        ...         pass
        ```

    signature(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/app/base.html#Celery.signature)
    :   Return a new [`Signature`](#celery.Signature "celery.Signature") bound to this app.

    bugreport()[[source]](../_modules/celery/app/base.html#Celery.bugreport)
    :   Return information useful in bug reports.

    config\_from\_object(*obj*, *silent=False*, *force=False*, *namespace=None*)[[source]](../_modules/celery/app/base.html#Celery.config_from_object)
    :   Read configuration from object.

        Object is either an actual object or the name of a module to import.

        Example

        ```
        >>> celery.config_from_object('myapp.celeryconfig')
        ```

        ```
        >>> from myapp import celeryconfig
        >>> celery.config_from_object(celeryconfig)
        ```

        Parameters:
        :   - **silent** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If true then import errors will be ignored.
            - **force** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Force reading configuration immediately.
              By default the configuration will be read only when required.

    config\_from\_envvar(*variable\_name*, *silent=False*, *force=False*)[[source]](../_modules/celery/app/base.html#Celery.config_from_envvar)
    :   Read configuration from environment variable.

        The value of the environment variable must be the name
        of a module to import.

        Example

        ```
        >>> os.environ['CELERY_CONFIG_MODULE'] = 'myapp.celeryconfig'
        >>> celery.config_from_envvar('CELERY_CONFIG_MODULE')
        ```

    autodiscover\_tasks(*packages=None*, *related\_name='tasks'*, *force=False*)[[source]](../_modules/celery/app/base.html#Celery.autodiscover_tasks)
    :   Auto-discover task modules.

        Searches a list of packages for a “tasks.py” module (or use
        related\_name argument).

        If the name is empty, this will be delegated to fix-ups (e.g., Django).

        For example if you have a directory layout like this:

        ```
        foo/__init__.py
           tasks.py
           models.py

        bar/__init__.py
            tasks.py
            models.py

        baz/__init__.py
            models.py
        ```

        Then calling `app.autodiscover_tasks(['foo', 'bar', 'baz'])` will
        result in the modules `foo.tasks` and `bar.tasks` being imported.

        Parameters:
        :   - **packages** (*List**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – List of packages to search.
              This argument may also be a callable, in which case the
              value returned is used (for lazy evaluation).
            - **related\_name** (*Optional**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – The name of the module to find. Defaults
              to “tasks”: meaning “look for ‘module.tasks’ for every
              module in `packages`.”. If `None` will only try to import
              the package, i.e. “look for ‘module’”.
            - **force** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – By default this call is lazy so that the actual
              auto-discovery won’t happen until an application imports
              the default modules. Forcing will cause the auto-discovery
              to happen immediately.

    add\_defaults(*fun*)[[source]](../_modules/celery/app/base.html#Celery.add_defaults)
    :   Add default configuration from dict `d`.

        If the argument is a callable function then it will be regarded
        as a promise, and it won’t be loaded until the configuration is
        actually needed.

        This method can be compared to:

        ```
        >>> celery.conf.update(d)
        ```

        with a difference that 1) no copy will be made and 2) the dict will
        not be transferred when the worker spawns child processes, so
        it’s important that the same configuration happens at import time
        when pickle restores the object on the other side.

    add\_periodic\_task(*schedule*, *sig*, *args=()*, *kwargs=()*, *name=None*, *\*\*opts*)[[source]](../_modules/celery/app/base.html#Celery.add_periodic_task)
    :   Add a periodic task to beat schedule.

        Celery beat store tasks based on sig or name if provided. Adding the
        same signature twice make the second task override the first one. To
        avoid the override, use distinct name for them.

    setup\_security(*allowed\_serializers=None*, *key=None*, *key\_password=None*, *cert=None*, *store=None*, *digest='sha256'*, *serializer='json'*)[[source]](../_modules/celery/app/base.html#Celery.setup_security)
    :   Setup the message-signing serializer.

        This will affect all application instances (a global operation).

        Disables untrusted serializers and if configured to use the `auth`
        serializer will register the `auth` serializer with the provided
        settings into the Kombu serializer registry.

        Parameters:
        :   - **allowed\_serializers** (*Set**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – List of serializer names, or
              content\_types that should be exempt from being disabled.
            - **key** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of private key file to use.
              Defaults to the [`security_key`](../userguide/configuration.html#std-setting-security_key) setting.
            - **key\_password** ([*bytes*](https://docs.python.org/dev/library/stdtypes.html#bytes "(in Python v3.15)")) – Password to decrypt the private key.
              Defaults to the [`security_key_password`](../userguide/configuration.html#std-setting-security_key_password) setting.
            - **cert** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of certificate file to use.
              Defaults to the [`security_certificate`](../userguide/configuration.html#std-setting-security_certificate) setting.
            - **store** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Directory containing certificates.
              Defaults to the [`security_cert_store`](../userguide/configuration.html#std-setting-security_cert_store) setting.
            - **digest** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Digest algorithm used when signing messages.
              Default is `sha256`.
            - **serializer** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Serializer used to encode messages after
              they’ve been signed. See [`task_serializer`](../userguide/configuration.html#std-setting-task_serializer) for
              the serializers supported. Default is `json`.

    task(*\*args*, *\*\*opts*)[[source]](../_modules/celery/app/base.html#Celery.task)
    :   Decorator to create a task class out of any callable.

        See [Task options](../userguide/tasks.html#task-options) for a list of the
        arguments that can be passed to this decorator.

        Examples

        ```
        @app.task
        def refresh_feed(url):
            store_feed(feedparser.parse(url))
        ```

        with setting extra options:

        ```
        @app.task(exchange='feeds')
        def refresh_feed(url):
            return store_feed(feedparser.parse(url))
        ```

        Note

        App Binding: For custom apps the task decorator will return
        a proxy object, so that the act of creating the task is not
        performed until the task is used or the task registry is accessed.

        If you’re depending on binding to be deferred, then you must
        not access any attributes on the returned object until the
        application is fully set up (finalized).

    send\_task(*name*, *args=None*, *kwargs=None*, *countdown=None*, *eta=None*, *task\_id=None*, *producer=None*, *connection=None*, *router=None*, *result\_cls=None*, *expires=None*, *publisher=None*, *link=None*, *link\_error=None*, *add\_to\_parent=True*, *group\_id=None*, *group\_index=None*, *retries=0*, *chord=None*, *reply\_to=None*, *time\_limit=None*, *soft\_time\_limit=None*, *root\_id=None*, *parent\_id=None*, *route\_name=None*, *shadow=None*, *chain=None*, *task\_type=None*, *replaced\_task\_nesting=0*, *\*\*options*)[[source]](../_modules/celery/app/base.html#Celery.send_task)
    :   Send task by name.

        Supports the same arguments as [`Task.apply_async()`](celery.app.task.html#celery.app.task.Task.apply_async "celery.app.task.Task.apply_async").

        Parameters:
        :   - **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of task to call (e.g., “tasks.add”).
            - **result\_cls** ([*AsyncResult*](celery.result.html#celery.result.AsyncResult "celery.result.AsyncResult")) – Specify custom result class.

    gen\_task\_name(*name*, *module*)[[source]](../_modules/celery/app/base.html#Celery.gen_task_name)

    AsyncResult
    :   Create new result instance.

        See also

        [`celery.result.AsyncResult`](celery.result.html#celery.result.AsyncResult "celery.result.AsyncResult").

    GroupResult
    :   Create new group result instance.

        See also

        [`celery.result.GroupResult`](celery.result.html#celery.result.GroupResult "celery.result.GroupResult").

    Worker
    :   Worker application.

        See also

        [`Worker`](celery.apps.worker.html#celery.apps.worker.Worker "celery.apps.worker.Worker").

    WorkController
    :   Embeddable worker.

        See also

        [`WorkController`](celery.worker.html#celery.worker.WorkController "celery.worker.WorkController").

    Beat
    :   **celery beat** scheduler application.

        See also

        [`Beat`](celery.apps.beat.html#celery.apps.beat.Beat "celery.apps.beat.Beat").

    connection\_for\_read(*url=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/base.html#Celery.connection_for_read)
    :   Establish connection used for consuming.

        See also

        [`connection()`](../userguide/extending.html#connection "connection") for supported arguments.

    connection\_for\_write(*url=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/base.html#Celery.connection_for_write)
    :   Establish connection used for producing.

        See also

        [`connection()`](../userguide/extending.html#connection "connection") for supported arguments.

    connection(*hostname=None*, *userid=None*, *password=None*, *virtual\_host=None*, *port=None*, *ssl=None*, *connect\_timeout=None*, *transport=None*, *transport\_options=None*, *heartbeat=None*, *login\_method=None*, *failover\_strategy=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/base.html#Celery.connection)
    :   Establish a connection to the message broker.

        Please use [`connection_for_read()`](#celery.Celery.connection_for_read "celery.Celery.connection_for_read") and
        [`connection_for_write()`](#celery.Celery.connection_for_write "celery.Celery.connection_for_write") instead, to convey the intent
        of use for this connection.

        Parameters:
        :   - **url** – Either the URL or the hostname of the broker to use.
            - **hostname** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – URL, Hostname/IP-address of the broker.
              If a URL is used, then the other argument below will
              be taken from the URL instead.
            - **userid** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Username to authenticate as.
            - **password** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Password to authenticate with
            - **virtual\_host** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Virtual host to use (domain).
            - **port** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – Port to connect to.
            - **ssl** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")*,* *Dict*) – Defaults to the [`broker_use_ssl`](../userguide/configuration.html#std-setting-broker_use_ssl)
              setting.
            - **transport** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – defaults to the `broker_transport`
              setting.
            - **transport\_options** (*Dict*) – Dictionary of transport specific options.
            - **heartbeat** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – AMQP Heartbeat in seconds (`pyamqp` only).
            - **login\_method** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Custom login method to use (AMQP only).
            - **failover\_strategy** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *Callable*) – Custom failover strategy.
            - **\*\*kwargs** – Additional arguments to [`kombu.Connection`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)").

        Returns:
        :   the lazy connection instance.

        Return type:
        :   [kombu.Connection](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")

    connection\_or\_acquire(*connection=None*, *pool=True*, *\*\_*, *\*\*\_\_*)[[source]](../_modules/celery/app/base.html#Celery.connection_or_acquire)
    :   Context used to acquire a connection from the pool.

        For use within a [`with`](https://docs.python.org/dev/reference/compound_stmts.html#with "(in Python v3.15)") statement to get a connection
        from the pool if one is not already provided.

        Parameters:
        :   **connection** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – If not provided, a connection
            will be acquired from the connection pool.

    producer\_or\_acquire(*producer=None*)[[source]](../_modules/celery/app/base.html#Celery.producer_or_acquire)
    :   Context used to acquire a producer from the pool.

        For use within a [`with`](https://docs.python.org/dev/reference/compound_stmts.html#with "(in Python v3.15)") statement to get a producer
        from the pool if one is not already provided

        Parameters:
        :   **producer** ([*kombu.Producer*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Producer "(in Kombu v5.6)")) – If not provided, a producer
            will be acquired from the producer pool.

    select\_queues(*queues=None*)[[source]](../_modules/celery/app/base.html#Celery.select_queues)
    :   Select subset of queues.

        Parameters:
        :   **queues** (*Sequence**[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – a list of queue names to keep.

    now()[[source]](../_modules/celery/app/base.html#Celery.now)
    :   Return the current time and date as a datetime.

    set\_current()[[source]](../_modules/celery/app/base.html#Celery.set_current)
    :   Make this the current app for this thread.

    set\_default()[[source]](../_modules/celery/app/base.html#Celery.set_default)
    :   Make this the default app for all threads.

    finalize(*auto=False*)[[source]](../_modules/celery/app/base.html#Celery.finalize)
    :   Finalize the app.

        This loads built-in tasks, evaluates pending task decorators,
        reads configuration, etc.

    on\_init()[[source]](../_modules/celery/app/base.html#Celery.on_init)
    :   Optional callback called at init.

    prepare\_config(*c*)[[source]](../_modules/celery/app/base.html#Celery.prepare_config)
    :   Prepare configuration before it is merged with the defaults.

    on\_configure
    :   Signal sent when app is loading configuration.

    on\_after\_configure
    :   Signal sent after app has prepared the configuration.

    on\_after\_finalize
    :   Signal sent after the app has been finalized — that is, after all
        pending task decorators have been evaluated, built-in tasks loaded,
        and every task registered at that point has been bound to the app.
        At this stage the task registry is initialized and stable enough to
        import and inspect task objects reliably.

        See [`finalize()`](#celery.Celery.finalize "celery.Celery.finalize") for more details on what
        finalization does.

    on\_after\_fork
    :   Signal sent in child process after fork.

## Canvas primitives

See [Canvas: Designing Work-flows](../userguide/canvas.html#guide-canvas) for more about creating task work-flows.

class celery.group(*\*tasks*, *\*\*options*)[[source]](../_modules/celery/canvas.html#group)
:   Creates a group of tasks to be executed in parallel.

    A group is lazy so you must call it to take action and evaluate
    the group.

    Note

    If only one argument is passed, and that argument is an iterable
    then that’ll be used as the list of tasks instead: this
    allows us to use `group` with generator expressions.

    Example

    ```
    >>> lazy_group = group([add.s(2, 2), add.s(4, 4)])
    >>> promise = lazy_group()  # <-- evaluate: returns lazy result.
    >>> promise.get()  # <-- will wait for the task to return
    [4, 8]
    ```

    Parameters:
    :   - **\*tasks** (*List**[*[*Signature*](#celery.Signature "celery.Signature")*]*) – A list of signatures that this group will
          call. If there’s only one argument, and that argument is an
          iterable, then that’ll define the list of signatures instead.
        - **\*\*options** (*Any*) – Execution options applied to all tasks
          in the group.

    Returns:
    :   signature that when called will then call all of the
        :   tasks in the group (and return a `GroupResult` instance
            that can be used to inspect the state of the group).

    Return type:
    :   [*group*](#celery.group "celery.group")

class celery.chain(*\*tasks*, *\*\*kwargs*)[[source]](../_modules/celery/canvas.html#chain)
:   Chain tasks together.

    Each tasks follows one another,
    by being applied as a callback of the previous task.

    Note

    If called with only one argument, then that argument must
    be an iterable of tasks to chain: this allows us
    to use generator expressions.

    Example

    This is effectively :

    ```
    >>> res = chain(add.s(2, 2), add.s(4))()
    >>> res.get()
    8
    ```

    Calling a chain will return the result of the last task in the chain.
    You can get to the other tasks by following the `result.parent`’s:

    ```
    >>> res.parent.get()
    4
    ```

    Using a generator expression:

    ```
    >>> lazy_chain = chain(add.s(i) for i in range(10))
    >>> res = lazy_chain(3)
    ```

    Parameters:
    :   **\*tasks** ([*Signature*](#celery.Signature "celery.Signature")) – List of task signatures to chain.
        If only one argument is passed and that argument is
        an iterable, then that’ll be used as the list of signatures
        to chain instead. This means that you can use a generator
        expression.

    Returns:
    :   A lazy signature that can be called to apply the first
        :   task in the chain. When that task succeeds the next task in the
            chain is applied, and so on.

    Return type:
    :   [*chain*](#celery.chain "celery.chain")

celery.chord
:   alias of `_chord`

celery.signature(*varies*, *\*args*, *\*\*kwargs*)[[source]](../_modules/celery/canvas.html#signature)
:   Create new signature.

    - if the first argument is a signature already then it’s cloned.
    - if the first argument is a dict, then a Signature version is returned.

    Returns:
    :   The resulting signature.

    Return type:
    :   [Signature](#celery.Signature "celery.Signature")

class celery.Signature(*task=None*, *args=None*, *kwargs=None*, *options=None*, *type=None*, *subtask\_type=None*, *immutable=False*, *app=None*, *\*\*ex*)[[source]](../_modules/celery/canvas.html#Signature)
:   Task Signature.

    Class that wraps the arguments and execution options
    for a single task invocation.

    Used as the parts in a [`group`](#celery.group "celery.group") and other constructs,
    or to pass tasks around as callbacks while being compatible
    with serializers with a strict type subset.

    Signatures can also be created from tasks:

    - Using the `.signature()` method that has the same signature
      as `Task.apply_async`:

      > ```
      > >>> add.signature(args=(1,), kwargs={'kw': 2}, options={})
      > ```
    - or the `.s()` shortcut that works for star arguments:

      > ```
      > >>> add.s(1, kw=2)
      > ```
    - the `.s()` shortcut does not allow you to specify execution options
      but there’s a chaining .set method that returns the signature:

      > ```
      > >>> add.s(2, 2).set(countdown=10).set(expires=30).delay()
      > ```

    Note

    You should use [`signature()`](#celery.signature "celery.signature") to create new signatures.
    The `Signature` class is the type returned by that function and
    should be used for `isinstance` checks for signatures.

    See also

    [Canvas: Designing Work-flows](../userguide/canvas.html#guide-canvas) for the complete guide.

    Parameters:
    :   - **task** (*Union**[**Type**[*[*celery.app.task.Task*](celery.app.task.html#celery.app.task.Task "celery.app.task.Task")*]**,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*]*) – Either a task
          class/instance, or the name of a task.
        - **args** (*Tuple*) – Positional arguments to apply.
        - **kwargs** (*Dict*) – Keyword arguments to apply.
        - **options** (*Dict*) – Additional options to `Task.apply_async()`.

    Note

    If the first argument is a [`dict`](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)"), the other
    arguments will be ignored and the values in the dict will be used
    instead:

    ```
    >>> s = signature('tasks.add', args=(2, 2))
    >>> signature(s)
    {'task': 'tasks.add', args=(2, 2), kwargs={}, options={}}
    ```

## Proxies

celery.current\_app
:   The currently set app for this thread.

celery.current\_task
:   The task currently being executed
    (only set in the worker, or when eager/apply is used).