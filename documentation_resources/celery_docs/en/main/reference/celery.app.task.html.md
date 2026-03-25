<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.app.task.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.task.html).

# `celery.app.task`

Task implementation: request context and the task base class.

class celery.app.task.Context(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/app/task.html#Context)
:   Task request variables (Task.request).

class celery.app.task.Task[[source]](../_modules/celery/app/task.html#Task)
:   Task base class.

    Note

    When called tasks apply the [`run()`](#celery.app.task.Task.run "celery.app.task.Task.run") method. This method must
    be defined by all tasks (that is unless the `__call__()` method
    is overridden).

    AsyncResult(*task\_id*, *\*\*kwargs*)[[source]](../_modules/celery/app/task.html#Task.AsyncResult)
    :   Get AsyncResult instance for the specified task.

        Parameters:
        :   **task\_id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Task id to get result for.

    exception MaxRetriesExceededError(*\*args*, *\*\*kwargs*)
    :   The tasks max restart limit has been exceeded.

    exception OperationalError
    :   Recoverable message transport connection error.

    Request = 'celery.worker.request:Request'
    :   Request class used, or the qualified name of one.

    Strategy = 'celery.worker.strategy:default'
    :   Execution strategy used, or the qualified name of one.

    abstract = True
    :   Deprecated attribute `abstract` here for compatibility.

    acks\_late = False
    :   When enabled messages for this task will be acknowledged **after**
        the task has been executed, and not *right before* (the
        default behavior).

        Please note that this means the task may be executed twice if the
        worker crashes mid execution.

        The application default can be overridden with the
        [`task_acks_late`](../userguide/configuration.html#std-setting-task_acks_late) setting.

    acks\_on\_failure = True
    :   When enabled messages for this task will be acknowledged on failure.
        Falls back to [`acks_on_failure_or_timeout`](#celery.app.task.Task.acks_on_failure_or_timeout "celery.app.task.Task.acks_on_failure_or_timeout") if `None`.

        Configuring this setting only applies to tasks that are
        acknowledged **after** they have been executed and only if
        [`task_acks_late`](../userguide/configuration.html#std-setting-task_acks_late) is enabled.

        The application default can be overridden with the
        [`task_acks_on_failure`](../userguide/configuration.html#std-setting-task_acks_on_failure) setting.

    acks\_on\_failure\_or\_timeout = True
    :   When enabled messages for this task will be acknowledged even if it
        fails or times out.

        Configuring this setting only applies to tasks that are
        acknowledged **after** they have been executed and only if
        [`task_acks_late`](../userguide/configuration.html#std-setting-task_acks_late) is enabled.

        The application default can be overridden with the
        [`task_acks_on_failure_or_timeout`](../userguide/configuration.html#std-setting-task_acks_on_failure_or_timeout) setting.

        Deprecated since version 6.0: Use [`acks_on_failure`](#celery.app.task.Task.acks_on_failure "celery.app.task.Task.acks_on_failure") and [`acks_on_timeout`](#celery.app.task.Task.acks_on_timeout "celery.app.task.Task.acks_on_timeout") instead.

    acks\_on\_timeout = True
    :   When enabled messages for this task will be acknowledged on timeout.
        Falls back to [`acks_on_failure_or_timeout`](#celery.app.task.Task.acks_on_failure_or_timeout "celery.app.task.Task.acks_on_failure_or_timeout") if `None`.

        Configuring this setting only applies to tasks that are
        acknowledged **after** they have been executed and only if
        [`task_acks_late`](../userguide/configuration.html#std-setting-task_acks_late) is enabled.

        The application default can be overridden with the
        [`task_acks_on_timeout`](../userguide/configuration.html#std-setting-task_acks_on_timeout) setting.

    add\_to\_chord(*sig*, *lazy=False*)[[source]](../_modules/celery/app/task.html#Task.add_to_chord)
    :   Add signature to the chord the current task is a member of.

        Added in version 4.0.

        Currently only supported by the Redis result backend.

        Parameters:
        :   - **sig** ([*Signature*](celery.html#celery.Signature "celery.Signature")) – Signature to extend chord with.
            - **lazy** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If enabled the new task won’t actually be called,
              and `sig.delay()` must be called manually.

    after\_return(*status*, *retval*, *task\_id*, *args*, *kwargs*, *einfo*)[[source]](../_modules/celery/app/task.html#Task.after_return)
    :   Handler called after the task returns.

        Parameters:
        :   - **status** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Current task state.
            - **retval** (*Any*) – Task return value/exception.
            - **task\_id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Unique id of the task.
            - **args** (*Tuple*) – Original arguments for the task.
            - **kwargs** (*Dict*) – Original keyword arguments for the task.
            - **einfo** (*ExceptionInfo*) – Exception information.

        Returns:
        :   The return value of this handler is ignored.

        Return type:
        :   None

    apply(*args=None*, *kwargs=None*, *link=None*, *link\_error=None*, *task\_id=None*, *retries=None*, *throw=None*, *logfile=None*, *loglevel=None*, *headers=None*, *\*\*options*)[[source]](../_modules/celery/app/task.html#Task.apply)
    :   Execute this task locally, by blocking until the task returns.

        Parameters:
        :   - **args** (*Tuple*) – positional arguments passed on to the task.
            - **kwargs** (*Dict*) – keyword arguments passed on to the task.
            - **throw** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Re-raise task exceptions.
              Defaults to the [`task_eager_propagates`](../userguide/configuration.html#std-setting-task_eager_propagates) setting.

        Returns:
        :   pre-evaluated result.

        Return type:
        :   [celery.result.EagerResult](celery.result.html#celery.result.EagerResult "celery.result.EagerResult")

    apply\_async(*args=None*, *kwargs=None*, *task\_id=None*, *producer=None*, *link=None*, *link\_error=None*, *shadow=None*, *\*\*options*)[[source]](../_modules/celery/app/task.html#Task.apply_async)
    :   Apply tasks asynchronously by sending a message.

        Parameters:
        :   - **args** (*Tuple*) – The positional arguments to pass on to the task.
            - **kwargs** (*Dict*) – The keyword arguments to pass on to the task.
            - **countdown** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Number of seconds into the future that the
              task should execute. Defaults to immediate execution.
            - **eta** ([*datetime*](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")) – Absolute time and date of when the task
              should be executed. May not be specified if countdown
              is also supplied.
            - **expires** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")*,* [*datetime*](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")) – Datetime or
              seconds in the future for the task should expire.
              The task won’t be executed after the expiration time.
            - **shadow** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Override task name used in logs/monitoring.
              Default is retrieved from [`shadow_name()`](#celery.app.task.Task.shadow_name "celery.app.task.Task.shadow_name").
            - **connection** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Reuse existing broker connection
              instead of acquiring one from the connection pool.
            - **retry** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If enabled sending of the task message will be
              retried in the event of connection loss or failure.
              Default is taken from the [`task_publish_retry`](../userguide/configuration.html#std-setting-task_publish_retry)
              setting. Note that you need to handle the
              producer/connection manually for this to work.
            - **retry\_policy** (*Mapping*) – Override the retry policy used.
              See the [`task_publish_retry_policy`](../userguide/configuration.html#std-setting-task_publish_retry_policy) setting.
            - **time\_limit** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – If set, overrides the default time limit.
            - **soft\_time\_limit** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – If set, overrides the default soft
              time limit.
            - **queue** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*kombu.Queue*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)")) – The queue to route the task to.
              This must be a key present in [`task_queues`](../userguide/configuration.html#std-setting-task_queues), or
              [`task_create_missing_queues`](../userguide/configuration.html#std-setting-task_create_missing_queues) must be
              enabled. See [Routing Tasks](../userguide/routing.html#guide-routing) for more
              information.
            - **exchange** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*kombu.Exchange*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Exchange "(in Kombu v5.6)")) – Named custom exchange to send the
              task to. Usually not used in combination with the `queue`
              argument.
            - **routing\_key** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Custom routing key used to route the task to a
              worker server. If in combination with a `queue` argument
              only used to specify custom routing keys to topic exchanges.
            - **priority** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – The task priority, a number between 0 and 9.
              Defaults to the [`priority`](#celery.app.task.Task.priority "celery.app.task.Task.priority") attribute.
            - **serializer** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Serialization method to use.
              Can be pickle, json, yaml, msgpack or any custom
              serialization method that’s been registered
              with `kombu.serialization.registry`.
              Defaults to the [`serializer`](../userguide/tasks.html#Task.serializer "Task.serializer") attribute.
            - **compression** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Optional compression method
              to use. Can be one of `zlib`, `bzip2`,
              or any custom compression methods registered with
              [`kombu.compression.register()`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.compression.html#kombu.compression.register "(in Kombu v5.6)").
              Defaults to the [`task_compression`](../userguide/configuration.html#std-setting-task_compression) setting.
            - **link** ([*Signature*](celery.html#celery.Signature "celery.Signature")) – A single, or a list of tasks signatures
              to apply if the task returns successfully.
            - **link\_error** ([*Signature*](celery.html#celery.Signature "celery.Signature")) – A single, or a list of task signatures
              to apply if an error occurs while executing the task.
            - **producer** ([*kombu.Producer*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Producer "(in Kombu v5.6)")) – custom producer to use when publishing
              the task.
            - **add\_to\_parent** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If set to True (default) and the task
              is applied while executing another task, then the result
              will be appended to the parent tasks `request.children`
              attribute. Trailing can also be disabled by default using the
              [`trail`](#celery.app.task.Task.trail "celery.app.task.Task.trail") attribute
            - **ignore\_result** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If set to False (default) the result
              of a task will be stored in the backend. If set to True
              the result will not be stored. This can also be set
              using the [`ignore_result`](../userguide/tasks.html#Task.ignore_result "Task.ignore_result") in the app.task decorator.
            - **publisher** ([*kombu.Producer*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Producer "(in Kombu v5.6)")) – Deprecated alias to `producer`.
            - **headers** (*Dict*) – Message headers to be included in the message.
              The headers can be used as an overlay for custom labeling
              using the [Stamping](../userguide/canvas.html#canvas-stamping) feature.
            - **task\_id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Optional argument to override the default task id.
              By default, Celery generates a unique id (UUID4) for every task
              submission. You can instead provide your own string identifier.
              If supplied, this value will be used as the task’s id instead
              of generating one automatically. Be careful to avoid collisions
              when overriding task ids.

        Returns:
        :   Promise of future evaluation.

        Return type:
        :   [celery.result.AsyncResult](celery.result.html#celery.result.AsyncResult "celery.result.AsyncResult")

        Raises:
        :   - [**TypeError**](https://docs.python.org/dev/library/exceptions.html#TypeError "(in Python v3.15)") – If not enough arguments are passed, or too many
              arguments are passed. Note that signature checks may
              be disabled by specifying `@task(typing=False)`.
            - [**ValueError**](https://docs.python.org/dev/library/exceptions.html#ValueError "(in Python v3.15)") – If soft\_time\_limit and time\_limit both are set
              but soft\_time\_limit is greater than time\_limit
            - [**kombu.exceptions.OperationalError**](celery.exceptions.html#celery.exceptions.OperationalError "kombu.exceptions.OperationalError") – If a connection to the
              transport cannot be made, or if the connection is lost.

        Note

        Also supports all keyword arguments supported by
        [`kombu.Producer.publish()`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Producer.publish "(in Kombu v5.6)").

    property backend
    :   The result store backend used for this task.

    before\_start(*task\_id*, *args*, *kwargs*)[[source]](../_modules/celery/app/task.html#Task.before_start)
    :   Handler called before the task starts.

        Added in version 5.2.

        Parameters:
        :   - **task\_id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Unique id of the task to execute.
            - **args** (*Tuple*) – Original arguments for the task to execute.
            - **kwargs** (*Dict*) – Original keyword arguments for the task to execute.

        Returns:
        :   The return value of this handler is ignored.

        Return type:
        :   None

    chunks(*it*, *n*)[[source]](../_modules/celery/app/task.html#Task.chunks)
    :   Create a `chunks` task for this task.

    default\_retry\_delay = 180
    :   Default time in seconds before a retry of the task should be
        executed. 3 minutes by default.

    delay(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/app/task.html#Task.delay)
    :   Star argument version of [`apply_async()`](#celery.app.task.Task.apply_async "celery.app.task.Task.apply_async").

        Does not support the extra options enabled by [`apply_async()`](#celery.app.task.Task.apply_async "celery.app.task.Task.apply_async").

        Parameters:
        :   - **\*args** (*Any*) – Positional arguments passed on to the task.
            - **\*\*kwargs** (*Any*) – Keyword arguments passed on to the task.

        Returns:
        :   Future promise.

        Return type:
        :   [celery.result.AsyncResult](celery.result.html#celery.result.AsyncResult "celery.result.AsyncResult")

    expires = None
    :   Default task expiry time.

    ignore\_result = False
    :   If enabled the worker won’t store task state and return values
        for this task. Defaults to the [`task_ignore_result`](../userguide/configuration.html#std-setting-task_ignore_result)
        setting.

    map(*it*)[[source]](../_modules/celery/app/task.html#Task.map)
    :   Create a `xmap` task from `it`.

    max\_retries = 3
    :   Maximum number of retries before giving up. If set to `None`,
        it will **never** stop retrying.

    name = None
    :   Name of the task.

    classmethod on\_bound(*app*)[[source]](../_modules/celery/app/task.html#Task.on_bound)
    :   Called when the task is bound to an app.

        Note

        This class method can be defined to do additional actions when
        the task class is bound to an app.

    on\_failure(*exc*, *task\_id*, *args*, *kwargs*, *einfo*)[[source]](../_modules/celery/app/task.html#Task.on_failure)
    :   Error handler.

        This is run by the worker when the task fails.

        Parameters:
        :   - **exc** ([*Exception*](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)")) – The exception raised by the task.
            - **task\_id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Unique id of the failed task.
            - **args** (*Tuple*) – Original arguments for the task that failed.
            - **kwargs** (*Dict*) – Original keyword arguments for the task that failed.
            - **einfo** (*ExceptionInfo*) – Exception information.

        Returns:
        :   The return value of this handler is ignored.

        Return type:
        :   None

    on\_replace(*sig*)[[source]](../_modules/celery/app/task.html#Task.on_replace)
    :   Handler called when the task is replaced.

        Must return super().on\_replace(sig) when overriding to ensure the task replacement
        is properly handled.

        Added in version 5.3.

        Parameters:
        :   **sig** ([*Signature*](celery.html#celery.Signature "celery.Signature")) – signature to replace with.

    on\_retry(*exc*, *task\_id*, *args*, *kwargs*, *einfo*)[[source]](../_modules/celery/app/task.html#Task.on_retry)
    :   Retry handler.

        This is run by the worker when the task is to be retried.

        Parameters:
        :   - **exc** ([*Exception*](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)")) – The exception sent to [`retry()`](#celery.app.task.Task.retry "celery.app.task.Task.retry").
            - **task\_id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Unique id of the retried task.
            - **args** (*Tuple*) – Original arguments for the retried task.
            - **kwargs** (*Dict*) – Original keyword arguments for the retried task.
            - **einfo** (*ExceptionInfo*) – Exception information.

        Returns:
        :   The return value of this handler is ignored.

        Return type:
        :   None

    on\_success(*retval*, *task\_id*, *args*, *kwargs*)[[source]](../_modules/celery/app/task.html#Task.on_success)
    :   Success handler.

        Run by the worker if the task executes successfully.

        Parameters:
        :   - **retval** (*Any*) – The return value of the task.
            - **task\_id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Unique id of the executed task.
            - **args** (*Tuple*) – Original arguments for the executed task.
            - **kwargs** (*Dict*) – Original keyword arguments for the executed task.

        Returns:
        :   The return value of this handler is ignored.

        Return type:
        :   None

    priority = None
    :   Default task priority.

    rate\_limit = None
    :   `None` (no rate
        limit), ‘100/s’ (hundred tasks a second), ‘100/m’ (hundred tasks
        a minute),`’100/h’` (hundred tasks an hour)

        Type:
        :   Rate limit for this task type. Examples

    reject\_on\_worker\_lost = None
    :   Even if [`acks_late`](../userguide/tasks.html#Task.acks_late "Task.acks_late") is enabled, the worker will
        acknowledge tasks when the worker process executing them abruptly
        exits or is signaled (e.g., `KILL`/`INT`, etc).

        Setting this to true allows the message to be re-queued instead,
        so that the task will execute again by the same worker, or another
        worker.

        Warning: Enabling this can cause message loops; make sure you know
        what you’re doing.

    replace(*sig*)[[source]](../_modules/celery/app/task.html#Task.replace)
    :   Replace this task, with a new task inheriting the task id.

        Execution of the host task ends immediately and no subsequent statements
        will be run.

        Added in version 4.0.

        Parameters:
        :   - **sig** ([*Signature*](celery.html#celery.Signature "celery.Signature")) – signature to replace with.
            - **visitor** (*StampingVisitor*) – Visitor API object.

        Raises:
        :   - **~@Ignore** – This is always raised when called in asynchronous context.
            - **It is best to always use return self.replace****(****...****)** **to convey** –
            - **to the reader that the task won't continue after being replaced.** –

    property request
    :   Get current request object.

    request\_stack = <celery.utils.threads.\_LocalStack object>
    :   Task request stack, the current request will be the topmost.

    resultrepr\_maxsize = 1024
    :   Max length of result representation used in logs and events.

    retry(*args=None*, *kwargs=None*, *exc=None*, *throw=True*, *eta=None*, *countdown=None*, *max\_retries=None*, *\*\*options*)[[source]](../_modules/celery/app/task.html#Task.retry)
    :   Retry the task, adding it to the back of the queue.

        Example

        ```
        >>> from imaginary_twitter_lib import Twitter
        >>> from proj.celery import app
        ```

        ```
        >>> @app.task(bind=True)
        ... def tweet(self, auth, message):
        ...     twitter = Twitter(oauth=auth)
        ...     try:
        ...         twitter.post_status_update(message)
        ...     except twitter.FailWhale as exc:
        ...         # Retry in 5 minutes.
        ...         raise self.retry(countdown=60 * 5, exc=exc)
        ```

        Note

        Although the task will never return above as retry raises an
        exception to notify the worker, we use raise in front of the
        retry to convey that the rest of the block won’t be executed.

        Parameters:
        :   - **args** (*Tuple*) – Positional arguments to retry with.
            - **kwargs** (*Dict*) – Keyword arguments to retry with.
            - **exc** ([*Exception*](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)")) –

              Custom exception to report when the max retry
              limit has been exceeded (default:
              [`MaxRetriesExceededError`](celery.exceptions.html#celery.exceptions.MaxRetriesExceededError "celery.exceptions.MaxRetriesExceededError")).

              If this argument is set and retry is called while
              an exception was raised (`sys.exc_info()` is set)
              it will attempt to re-raise the current exception.

              If no exception was raised it will raise the `exc`
              argument provided.
            - **countdown** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time in seconds to delay the retry for.
            - **eta** ([*datetime*](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")) – Explicit time and date to run the
              retry at.
            - **max\_retries** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – If set, overrides the default retry limit for
              this execution. Changes to this parameter don’t propagate to
              subsequent task retry attempts. A value of `None`,
              means “use the default”, so if you want infinite retries you’d
              have to set the [`max_retries`](../userguide/tasks.html#id0 "Task.max_retries") attribute of the task to
              `None` first.
            - **time\_limit** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – If set, overrides the default time limit.
            - **soft\_time\_limit** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – If set, overrides the default soft
              time limit.
            - **throw** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If this is `False`, don’t raise the
              [`Retry`](celery.exceptions.html#celery.exceptions.Retry "celery.exceptions.Retry") exception, that tells the worker to mark
              the task as being retried. Note that this means the task
              will be marked as failed if the task raises an exception,
              or successful if it returns after the retry call.
            - **\*\*options** (*Any*) – Extra options to pass on to [`apply_async()`](#celery.app.task.Task.apply_async "celery.app.task.Task.apply_async").

        Raises:
        :   [**celery.exceptions.Retry**](celery.exceptions.html#celery.exceptions.Retry "celery.exceptions.Retry") – To tell the worker that the task has been re-sent for retry.
            This always happens, unless the throw keyword argument
            has been explicitly set to `False`, and is considered
            normal operation.

    run(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/app/task.html#Task.run)
    :   The body of the task executed by workers.

    s(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/app/task.html#Task.s)
    :   Create signature.

        Shortcut for `.s(*a, **k) -> .signature(a, k)`.

    send\_event(*type\_*, *retry=True*, *retry\_policy=None*, *\*\*fields*)[[source]](../_modules/celery/app/task.html#Task.send_event)
    :   Send monitoring event message.

        This can be used to add custom event types in <https://pypi.org/project/Flower/>
        and other monitors.

        Parameters:
        :   **type** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Type of event, e.g. `"task-failed"`.

        Keyword Arguments:
        :   - **retry** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Retry sending the message
              if the connection is lost. Default is taken from the
              [`task_publish_retry`](../userguide/configuration.html#std-setting-task_publish_retry) setting.
            - **retry\_policy** (*Mapping*) – Retry settings. Default is taken
              from the [`task_publish_retry_policy`](../userguide/configuration.html#std-setting-task_publish_retry_policy) setting.
            - **\*\*fields** (*Any*) – Map containing information about the event.
              Must be JSON serializable.

    send\_events = True
    :   If enabled the worker will send monitoring events related to
        this task (but only if the worker is configured to send
        task related events).
        Note that this has no effect on the task-failure event case
        where a task is not registered (as it will have no task class
        to check this flag).

    serializer = 'json'
    :   The name of a serializer that are registered with
        `kombu.serialization.registry`. Default is ‘json’.

    shadow\_name(*args*, *kwargs*, *options*)[[source]](../_modules/celery/app/task.html#Task.shadow_name)
    :   Override for custom task name in worker logs/monitoring.

        Example

        ```
        from celery.utils.imports import qualname

        def shadow_name(task, args, kwargs, options):
            return qualname(args[0])

        @app.task(shadow_name=shadow_name, serializer='pickle')
        def apply_function_async(fun, *args, **kwargs):
            return fun(*args, **kwargs)
        ```

        Parameters:
        :   - **args** (*Tuple*) – Task positional arguments.
            - **kwargs** (*Dict*) – Task keyword arguments.
            - **options** (*Dict*) – Task execution options.

    si(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/app/task.html#Task.si)
    :   Create immutable signature.

        Shortcut for `.si(*a, **k) -> .signature(a, k, immutable=True)`.

    signature(*args=None*, *\*starargs*, *\*\*starkwargs*)[[source]](../_modules/celery/app/task.html#Task.signature)
    :   Create signature.

        Returns:
        :   object for
            :   this task, wrapping arguments and execution options
                for a single task invocation.

        Return type:
        :   [`signature`](celery.html#celery.signature "celery.signature")

    soft\_time\_limit = None
    :   Soft time limit.
        Defaults to the [`task_soft_time_limit`](../userguide/configuration.html#std-setting-task_soft_time_limit) setting.

    starmap(*it*)[[source]](../_modules/celery/app/task.html#Task.starmap)
    :   Create a `xstarmap` task from `it`.

    store\_errors\_even\_if\_ignored = False
    :   When enabled errors will be stored even if the task is otherwise
        configured to ignore results.

    subtask(*args=None*, *\*starargs*, *\*\*starkwargs*)
    :   Create signature.

        Returns:
        :   object for
            :   this task, wrapping arguments and execution options
                for a single task invocation.

        Return type:
        :   [`signature`](celery.html#celery.signature "celery.signature")

    throws = ()
    :   Tuple of expected exceptions.

        These are errors that are expected in normal operation
        and that shouldn’t be regarded as a real error by the worker.
        Currently this means that the state will be updated to an error
        state, but the worker won’t log the event as an error.

    time\_limit = None
    :   Hard time limit.
        Defaults to the [`task_time_limit`](../userguide/configuration.html#std-setting-task_time_limit) setting.

    track\_started = False
    :   If enabled the task will report its status as ‘started’ when the task
        is executed by a worker. Disabled by default as the normal behavior
        is to not report that level of granularity. Tasks are either pending,
        finished, or waiting to be retried.

        Having a ‘started’ status can be useful for when there are long
        running tasks and there’s a need to report what task is currently
        running.

        The application default can be overridden using the
        [`task_track_started`](../userguide/configuration.html#std-setting-task_track_started) setting.

    trail = True
    :   If enabled the request will keep track of subtasks started by
        this task, and this information will be sent with the result
        (`result.children`).

    typing = True
    :   Enable argument checking.
        You can set this to false if you don’t want the signature to be
        checked when calling the task.
        Defaults to `Celery.strict_typing`.

    update\_state(*task\_id=None*, *state=None*, *meta=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/task.html#Task.update_state)
    :   Update task state.

        Parameters:
        :   - **task\_id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Id of the task to update.
              Defaults to the id of the current task.
            - **state** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – New state.
            - **meta** (*Dict*) – State meta-data.

celery.app.task.TaskType
:   Here for backwards compatibility as tasks no longer use a custom meta-class.