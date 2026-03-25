<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.result.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.result.html).

# `celery.result`

Task results/state and results for groups of tasks.

class celery.result.AsyncResult(*id*, *backend=None*, *task\_name=None*, *app=None*, *parent=None*)[[source]](../_modules/celery/result.html#AsyncResult)
:   Query task state.

    Parameters:
    :   - **id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – See [`id`](#celery.result.AsyncResult.id "celery.result.AsyncResult.id").
        - **backend** (*Backend*) – See [`backend`](#celery.result.AsyncResult.backend "celery.result.AsyncResult.backend").

    exception TimeoutError
    :   Error raised for timeouts.

    app = None

    property args

    as\_list()[[source]](../_modules/celery/result.html#AsyncResult.as_list)
    :   Return as a list of task IDs.

    as\_tuple()[[source]](../_modules/celery/result.html#AsyncResult.as_tuple)

    backend = None
    :   The task result backend to use.

    build\_graph(*intermediate=False*, *formatter=None*)[[source]](../_modules/celery/result.html#AsyncResult.build_graph)

    property children

    collect(*intermediate=False*, *\*\*kwargs*)[[source]](../_modules/celery/result.html#AsyncResult.collect)
    :   Collect results as they return.

        Iterator, like [`get()`](#celery.result.AsyncResult.get "celery.result.AsyncResult.get") will wait for the task to complete,
        but will also follow [`AsyncResult`](#celery.result.AsyncResult "celery.result.AsyncResult") and [`ResultSet`](#celery.result.ResultSet "celery.result.ResultSet")
        returned by the task, yielding `(result, value)` tuples for each
        result in the tree.

        An example would be having the following tasks:

        ```
        from celery import group
        from proj.celery import app

        @app.task(trail=True)
        def A(how_many):
            return group(B.s(i) for i in range(how_many))()

        @app.task(trail=True)
        def B(i):
            return pow2.delay(i)

        @app.task(trail=True)
        def pow2(i):
            return i ** 2
        ```

        ```
        >>> from celery.result import ResultBase
        >>> from proj.tasks import A

        >>> result = A.delay(10)
        >>> [v for v in result.collect()
        ...  if not isinstance(v, (ResultBase, tuple))]
        [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
        ```

        Note

        The `Task.trail` option must be enabled
        so that the list of children is stored in `result.children`.
        This is the default but enabled explicitly for illustration.

        Yields:
        :   *Tuple[AsyncResult, Any]* – tuples containing the result instance
            of the child task, and the return value of that task.

    property date\_done
    :   UTC date and time.

    exists()[[source]](../_modules/celery/result.html#AsyncResult.exists)
    :   Return `True` if a result exists in the backend for this task.

        This can be used to distinguish between a task that is truly
        pending (waiting for execution) and a task ID that has never
        been submitted or whose result has been forgotten/expired.

        Without this method, both cases return `PENDING` as the state,
        making them indistinguishable.

        Added in version 5.7.0.

        Returns:
        :   `True` if the backend has a result stored for
            :   this task ID, `False` otherwise.

        Return type:
        :   [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")

    failed()[[source]](../_modules/celery/result.html#AsyncResult.failed)
    :   Return `True` if the task failed.

    forget()[[source]](../_modules/celery/result.html#AsyncResult.forget)
    :   Forget the result of this task and its parents.

    get(*timeout=None*, *propagate=True*, *interval=0.5*, *no\_ack=True*, *follow\_parents=True*, *callback=None*, *on\_message=None*, *on\_interval=None*, *disable\_sync\_subtasks=True*, *EXCEPTION\_STATES=frozenset({'FAILURE', 'RETRY', 'REVOKED'})*, *PROPAGATE\_STATES=frozenset({'FAILURE', 'REVOKED'})*)[[source]](../_modules/celery/result.html#AsyncResult.get)
    :   Wait until task is ready, and return its result.

        Warning

        Waiting for tasks within a task may lead to deadlocks.
        Please read [Avoid launching synchronous subtasks](../userguide/tasks.html#task-synchronous-subtasks).

        Warning

        Backends use resources to store and transmit results. To ensure
        that resources are released, you must eventually call
        [`get()`](#celery.result.AsyncResult.get "celery.result.AsyncResult.get") or [`forget()`](#celery.result.AsyncResult.forget "celery.result.AsyncResult.forget") on
        EVERY [`AsyncResult`](#celery.result.AsyncResult "celery.result.AsyncResult") instance returned after calling
        a task.

        Parameters:
        :   - **timeout** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – How long to wait, in seconds, before the
              operation times out. This is the setting for the publisher
              (celery client) and is different from timeout parameter of
              @app.task, which is the setting for the worker. The task
              isn’t terminated even if timeout occurs.
            - **propagate** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Re-raise exception if the task failed.
            - **interval** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time to wait (in seconds) before retrying to
              retrieve the result. Note that this does not have any effect
              when using the RPC/redis result store backends, as they don’t
              use polling.
            - **no\_ack** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Enable amqp no ack (automatically acknowledge
              message). If this is `False` then the message will
              **not be acked**.
            - **follow\_parents** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Re-raise any exception raised by
              parent tasks.
            - **disable\_sync\_subtasks** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Disable tasks to wait for sub tasks
              this is the default configuration. CAUTION do not enable this
              unless you must.

        Raises:
        :   - [**celery.exceptions.TimeoutError**](celery.exceptions.html#celery.exceptions.TimeoutError "celery.exceptions.TimeoutError") – if timeout isn’t
              `None` and the result does not arrive within
              timeout seconds.
            - [**Exception**](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)") – If the remote call raised an exception then that
              exception will be re-raised in the caller process.

    get\_leaf()[[source]](../_modules/celery/result.html#AsyncResult.get_leaf)

    property graph

    id = None
    :   The task’s UUID.

    property ignored
    :   If True, task result retrieval is disabled.

    property info
    :   Task return value.

        Note

        When the task has been executed, this contains the return value.
        If the task raised an exception, this will be the exception
        instance.

    iterdeps(*intermediate=False*)[[source]](../_modules/celery/result.html#AsyncResult.iterdeps)

    property kwargs

    maybe\_reraise(*propagate=True*, *callback=None*)

    maybe\_throw(*propagate=True*, *callback=None*)[[source]](../_modules/celery/result.html#AsyncResult.maybe_throw)

    property name

    property queue

    ready()[[source]](../_modules/celery/result.html#AsyncResult.ready)
    :   Return `True` if the task has executed.

        If the task is still running, pending, or is waiting
        for retry then `False` is returned.

    property result
    :   Task return value.

        Note

        When the task has been executed, this contains the return value.
        If the task raised an exception, this will be the exception
        instance.

    property retries

    revoke(*connection=None*, *terminate=False*, *signal=None*, *wait=False*, *timeout=None*)[[source]](../_modules/celery/result.html#AsyncResult.revoke)
    :   Send revoke signal to all workers.

        Any worker receiving the task, or having reserved the
        task, *must* ignore it.

        Parameters:
        :   - **terminate** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Also terminate the process currently working
              on the task (if any).
            - **signal** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of signal to send to process if terminate.
              Default is TERM.
            - **wait** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Wait for replies from workers.
              The `timeout` argument specifies the seconds to wait.
              Disabled by default.
            - **timeout** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time in seconds to wait for replies when
              `wait` is enabled.

    revoke\_by\_stamped\_headers(*headers*, *connection=None*, *terminate=False*, *signal=None*, *wait=False*, *timeout=None*)[[source]](../_modules/celery/result.html#AsyncResult.revoke_by_stamped_headers)
    :   Send revoke signal to all workers only for tasks with matching headers values.

        Any worker receiving the task, or having reserved the
        task, *must* ignore it.
        All header fields *must* match.

        Parameters:
        :   - **headers** ([*dict*](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*[*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* *Union**(*[*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*list*](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")*)**]*) – Headers to match when revoking tasks.
            - **terminate** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Also terminate the process currently working
              on the task (if any).
            - **signal** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of signal to send to process if terminate.
              Default is TERM.
            - **wait** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Wait for replies from workers.
              The `timeout` argument specifies the seconds to wait.
              Disabled by default.
            - **timeout** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time in seconds to wait for replies when
              `wait` is enabled.

    property state
    :   The tasks current state.

        Possible values includes:

        > *PENDING*
        >
        > > The task is waiting for execution.
        >
        > *STARTED*
        >
        > > The task has been started.
        >
        > *RETRY*
        >
        > > The task is to be retried, possibly because of failure.
        >
        > *FAILURE*
        >
        > > The task raised an exception, or has exceeded the retry limit.
        > > The [`result`](#celery.result.AsyncResult.result "celery.result.AsyncResult.result") attribute then contains the
        > > exception raised by the task.
        >
        > *SUCCESS*
        >
        > > The task executed successfully. The [`result`](#celery.result.AsyncResult.result "celery.result.AsyncResult.result") attribute
        > > then contains the tasks return value.

    property status
    :   The tasks current state.

        Possible values includes:

        > *PENDING*
        >
        > > The task is waiting for execution.
        >
        > *STARTED*
        >
        > > The task has been started.
        >
        > *RETRY*
        >
        > > The task is to be retried, possibly because of failure.
        >
        > *FAILURE*
        >
        > > The task raised an exception, or has exceeded the retry limit.
        > > The [`result`](#celery.result.AsyncResult.result "celery.result.AsyncResult.result") attribute then contains the
        > > exception raised by the task.
        >
        > *SUCCESS*
        >
        > > The task executed successfully. The [`result`](#celery.result.AsyncResult.result "celery.result.AsyncResult.result") attribute
        > > then contains the tasks return value.

    successful()[[source]](../_modules/celery/result.html#AsyncResult.successful)
    :   Return `True` if the task executed successfully.

    property supports\_native\_join

    property task\_id
    :   Compat. alias to [`id`](#celery.result.AsyncResult.id "celery.result.AsyncResult.id").

    then(*callback*, *on\_error=None*, *weak=False*)[[source]](../_modules/celery/result.html#AsyncResult.then)

    throw(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/result.html#AsyncResult.throw)

    property traceback
    :   Get the traceback of a failed task.

    wait(*timeout=None*, *propagate=True*, *interval=0.5*, *no\_ack=True*, *follow\_parents=True*, *callback=None*, *on\_message=None*, *on\_interval=None*, *disable\_sync\_subtasks=True*, *EXCEPTION\_STATES=frozenset({'FAILURE', 'RETRY', 'REVOKED'})*, *PROPAGATE\_STATES=frozenset({'FAILURE', 'REVOKED'})*)
    :   Wait until task is ready, and return its result.

        Warning

        Waiting for tasks within a task may lead to deadlocks.
        Please read [Avoid launching synchronous subtasks](../userguide/tasks.html#task-synchronous-subtasks).

        Warning

        Backends use resources to store and transmit results. To ensure
        that resources are released, you must eventually call
        [`get()`](#celery.result.AsyncResult.get "celery.result.AsyncResult.get") or [`forget()`](#celery.result.AsyncResult.forget "celery.result.AsyncResult.forget") on
        EVERY [`AsyncResult`](#celery.result.AsyncResult "celery.result.AsyncResult") instance returned after calling
        a task.

        Parameters:
        :   - **timeout** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – How long to wait, in seconds, before the
              operation times out. This is the setting for the publisher
              (celery client) and is different from timeout parameter of
              @app.task, which is the setting for the worker. The task
              isn’t terminated even if timeout occurs.
            - **propagate** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Re-raise exception if the task failed.
            - **interval** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time to wait (in seconds) before retrying to
              retrieve the result. Note that this does not have any effect
              when using the RPC/redis result store backends, as they don’t
              use polling.
            - **no\_ack** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Enable amqp no ack (automatically acknowledge
              message). If this is `False` then the message will
              **not be acked**.
            - **follow\_parents** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Re-raise any exception raised by
              parent tasks.
            - **disable\_sync\_subtasks** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Disable tasks to wait for sub tasks
              this is the default configuration. CAUTION do not enable this
              unless you must.

        Raises:
        :   - [**celery.exceptions.TimeoutError**](celery.exceptions.html#celery.exceptions.TimeoutError "celery.exceptions.TimeoutError") – if timeout isn’t
              `None` and the result does not arrive within
              timeout seconds.
            - [**Exception**](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)") – If the remote call raised an exception then that
              exception will be re-raised in the caller process.

    property worker

class celery.result.EagerResult(*id*, *ret\_value*, *state*, *traceback=None*, *name=None*)[[source]](../_modules/celery/result.html#EagerResult)
:   Result that we know has already been executed.

    forget()[[source]](../_modules/celery/result.html#EagerResult.forget)
    :   Forget the result of this task and its parents.

    get(*timeout=None*, *propagate=True*, *disable\_sync\_subtasks=True*, *\*\*kwargs*)[[source]](../_modules/celery/result.html#EagerResult.get)
    :   Wait until task is ready, and return its result.

        Warning

        Waiting for tasks within a task may lead to deadlocks.
        Please read [Avoid launching synchronous subtasks](../userguide/tasks.html#task-synchronous-subtasks).

        Warning

        Backends use resources to store and transmit results. To ensure
        that resources are released, you must eventually call
        [`get()`](#celery.result.AsyncResult.get "celery.result.AsyncResult.get") or [`forget()`](#celery.result.AsyncResult.forget "celery.result.AsyncResult.forget") on
        EVERY [`AsyncResult`](#celery.result.AsyncResult "celery.result.AsyncResult") instance returned after calling
        a task.

        Parameters:
        :   - **timeout** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – How long to wait, in seconds, before the
              operation times out. This is the setting for the publisher
              (celery client) and is different from timeout parameter of
              @app.task, which is the setting for the worker. The task
              isn’t terminated even if timeout occurs.
            - **propagate** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Re-raise exception if the task failed.
            - **interval** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time to wait (in seconds) before retrying to
              retrieve the result. Note that this does not have any effect
              when using the RPC/redis result store backends, as they don’t
              use polling.
            - **no\_ack** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Enable amqp no ack (automatically acknowledge
              message). If this is `False` then the message will
              **not be acked**.
            - **follow\_parents** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Re-raise any exception raised by
              parent tasks.
            - **disable\_sync\_subtasks** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Disable tasks to wait for sub tasks
              this is the default configuration. CAUTION do not enable this
              unless you must.

        Raises:
        :   - [**celery.exceptions.TimeoutError**](celery.exceptions.html#celery.exceptions.TimeoutError "celery.exceptions.TimeoutError") – if timeout isn’t
              `None` and the result does not arrive within
              timeout seconds.
            - [**Exception**](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)") – If the remote call raised an exception then that
              exception will be re-raised in the caller process.

    ready()[[source]](../_modules/celery/result.html#EagerResult.ready)
    :   Return `True` if the task has executed.

        If the task is still running, pending, or is waiting
        for retry then `False` is returned.

    property result
    :   The tasks return value.

    revoke(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/result.html#EagerResult.revoke)
    :   Send revoke signal to all workers.

        Any worker receiving the task, or having reserved the
        task, *must* ignore it.

        Parameters:
        :   - **terminate** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Also terminate the process currently working
              on the task (if any).
            - **signal** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of signal to send to process if terminate.
              Default is TERM.
            - **wait** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Wait for replies from workers.
              The `timeout` argument specifies the seconds to wait.
              Disabled by default.
            - **timeout** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time in seconds to wait for replies when
              `wait` is enabled.

    property state
    :   The tasks state.

    property status
    :   The tasks state.

    property supports\_native\_join

    then(*callback*, *on\_error=None*, *weak=False*)[[source]](../_modules/celery/result.html#EagerResult.then)

    property traceback
    :   The traceback if the task failed.

    wait(*timeout=None*, *propagate=True*, *disable\_sync\_subtasks=True*, *\*\*kwargs*)
    :   Wait until task is ready, and return its result.

        Warning

        Waiting for tasks within a task may lead to deadlocks.
        Please read [Avoid launching synchronous subtasks](../userguide/tasks.html#task-synchronous-subtasks).

        Warning

        Backends use resources to store and transmit results. To ensure
        that resources are released, you must eventually call
        [`get()`](#celery.result.AsyncResult.get "celery.result.AsyncResult.get") or [`forget()`](#celery.result.AsyncResult.forget "celery.result.AsyncResult.forget") on
        EVERY [`AsyncResult`](#celery.result.AsyncResult "celery.result.AsyncResult") instance returned after calling
        a task.

        Parameters:
        :   - **timeout** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – How long to wait, in seconds, before the
              operation times out. This is the setting for the publisher
              (celery client) and is different from timeout parameter of
              @app.task, which is the setting for the worker. The task
              isn’t terminated even if timeout occurs.
            - **propagate** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Re-raise exception if the task failed.
            - **interval** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time to wait (in seconds) before retrying to
              retrieve the result. Note that this does not have any effect
              when using the RPC/redis result store backends, as they don’t
              use polling.
            - **no\_ack** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Enable amqp no ack (automatically acknowledge
              message). If this is `False` then the message will
              **not be acked**.
            - **follow\_parents** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Re-raise any exception raised by
              parent tasks.
            - **disable\_sync\_subtasks** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Disable tasks to wait for sub tasks
              this is the default configuration. CAUTION do not enable this
              unless you must.

        Raises:
        :   - [**celery.exceptions.TimeoutError**](celery.exceptions.html#celery.exceptions.TimeoutError "celery.exceptions.TimeoutError") – if timeout isn’t
              `None` and the result does not arrive within
              timeout seconds.
            - [**Exception**](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)") – If the remote call raised an exception then that
              exception will be re-raised in the caller process.

class celery.result.GroupResult(*id=None*, *results=None*, *parent=None*, *\*\*kwargs*)[[source]](../_modules/celery/result.html#GroupResult)
:   Like [`ResultSet`](#celery.result.ResultSet "celery.result.ResultSet"), but with an associated id.

    This type is returned by [`group`](celery.html#celery.group "celery.group").

    It enables inspection of the tasks state and return values as
    a single entity.

    Parameters:
    :   - **id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – The id of the group.
        - **results** (*Sequence**[*[*AsyncResult*](#celery.result.AsyncResult "celery.result.AsyncResult")*]*) – List of result instances.
        - **parent** ([*ResultBase*](#celery.result.ResultBase "celery.result.ResultBase")) – Parent result of this group.

    as\_tuple()[[source]](../_modules/celery/result.html#GroupResult.as_tuple)

    property children

    delete(*backend=None*)[[source]](../_modules/celery/result.html#GroupResult.delete)
    :   Remove this result if it was previously saved.

    id = None
    :   The UUID of the group.

    classmethod restore(*id*, *backend=None*, *app=None*)[[source]](../_modules/celery/result.html#GroupResult.restore)
    :   Restore previously saved group result.

    results = None
    :   List/iterator of results in the group

    save(*backend=None*)[[source]](../_modules/celery/result.html#GroupResult.save)
    :   Save group-result for later retrieval using [`restore()`](#celery.result.GroupResult.restore "celery.result.GroupResult.restore").

        Example

        ```
        >>> def save_and_restore(result):
        ...     result.save()
        ...     result = GroupResult.restore(result.id)
        ```

class celery.result.ResultBase[[source]](../_modules/celery/result.html#ResultBase)
:   Base class for results.

    parent = None
    :   Parent result (if part of a chain)

class celery.result.ResultSet(*results*, *app=None*, *ready\_barrier=None*, *\*\*kwargs*)[[source]](../_modules/celery/result.html#ResultSet)
:   A collection of results.

    Parameters:
    :   **results** (*Sequence**[*[*AsyncResult*](#celery.result.AsyncResult "celery.result.AsyncResult")*]*) – List of result instances.

    add(*result*)[[source]](../_modules/celery/result.html#ResultSet.add)
    :   Add [`AsyncResult`](#celery.result.AsyncResult "celery.result.AsyncResult") as a new member of the set.

        Does nothing if the result is already a member.

    property app

    property backend

    clear()[[source]](../_modules/celery/result.html#ResultSet.clear)
    :   Remove all results from this set.

    completed\_count()[[source]](../_modules/celery/result.html#ResultSet.completed_count)
    :   Task completion count.

        Note that complete means successful in this context. In other words, the
        return value of this method is the number of `successful` tasks.

        Returns:
        :   the number of complete (i.e. successful) tasks.

        Return type:
        :   [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")

    discard(*result*)[[source]](../_modules/celery/result.html#ResultSet.discard)
    :   Remove result from the set if it is a member.

        Does nothing if it’s not a member.

    failed()[[source]](../_modules/celery/result.html#ResultSet.failed)
    :   Return true if any of the tasks failed.

        Returns:
        :   true if one of the tasks failed.
            :   (i.e., raised an exception)

        Return type:
        :   [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")

    forget()[[source]](../_modules/celery/result.html#ResultSet.forget)
    :   Forget about (and possible remove the result of) all the tasks.

    get(*timeout=None*, *propagate=True*, *interval=0.5*, *callback=None*, *no\_ack=True*, *on\_message=None*, *disable\_sync\_subtasks=True*, *on\_interval=None*)[[source]](../_modules/celery/result.html#ResultSet.get)
    :   See [`join()`](#celery.result.ResultSet.join "celery.result.ResultSet.join").

        This is here for API compatibility with [`AsyncResult`](#celery.result.AsyncResult "celery.result.AsyncResult"),
        in addition it uses [`join_native()`](#celery.result.ResultSet.join_native "celery.result.ResultSet.join_native") if available for the
        current result backend.

    iter\_native(*timeout=None*, *interval=0.5*, *no\_ack=True*, *on\_message=None*, *on\_interval=None*)[[source]](../_modules/celery/result.html#ResultSet.iter_native)
    :   Backend optimized version of `iterate()`.

        Added in version 2.2.

        Note that this does not support collecting the results
        for different task types using different backends.

        This is currently only supported by the amqp, Redis and cache
        result backends.

    join(*timeout=None*, *propagate=True*, *interval=0.5*, *callback=None*, *no\_ack=True*, *on\_message=None*, *disable\_sync\_subtasks=True*, *on\_interval=None*)[[source]](../_modules/celery/result.html#ResultSet.join)
    :   Gather the results of all tasks as a list in order.

        Note

        This can be an expensive operation for result store
        backends that must resort to polling (e.g., database).

        You should consider using [`join_native()`](#celery.result.ResultSet.join_native "celery.result.ResultSet.join_native") if your backend
        supports it.

        Warning

        Waiting for tasks within a task may lead to deadlocks.
        Please see [Avoid launching synchronous subtasks](../userguide/tasks.html#task-synchronous-subtasks).

        Parameters:
        :   - **timeout** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – The number of seconds to wait for results
              before the operation times out.
            - **propagate** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If any of the tasks raises an exception,
              the exception will be re-raised when this flag is set.
            - **interval** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time to wait (in seconds) before retrying to
              retrieve a result from the set. Note that this does not have
              any effect when using the amqp result store backend,
              as it does not use polling.
            - **callback** (*Callable*) – Optional callback to be called for every
              result received. Must have signature `(task_id, value)`
              No results will be returned by this function if a callback
              is specified. The order of results is also arbitrary when a
              callback is used. To get access to the result object for
              a particular id you’ll have to generate an index first:
              `index = {r.id: r for r in gres.results.values()}`
              Or you can create new result objects on the fly:
              `result = app.AsyncResult(task_id)` (both will
              take advantage of the backend cache anyway).
            - **no\_ack** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Automatic message acknowledgment (Note that if this
              is set to `False` then the messages
              *will not be acknowledged*).
            - **disable\_sync\_subtasks** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Disable tasks to wait for sub tasks
              this is the default configuration. CAUTION do not enable this
              unless you must.

        Raises:
        :   [**celery.exceptions.TimeoutError**](celery.exceptions.html#celery.exceptions.TimeoutError "celery.exceptions.TimeoutError") – if `timeout` isn’t
            `None` and the operation takes longer than `timeout`
            seconds.

    join\_native(*timeout=None*, *propagate=True*, *interval=0.5*, *callback=None*, *no\_ack=True*, *on\_message=None*, *on\_interval=None*, *disable\_sync\_subtasks=True*)[[source]](../_modules/celery/result.html#ResultSet.join_native)
    :   Backend optimized version of [`join()`](#celery.result.ResultSet.join "celery.result.ResultSet.join").

        Added in version 2.2.

        Note that this does not support collecting the results
        for different task types using different backends.

        This is currently only supported by the amqp, Redis and cache
        result backends.

    maybe\_reraise(*callback=None*, *propagate=True*)

    maybe\_throw(*callback=None*, *propagate=True*)[[source]](../_modules/celery/result.html#ResultSet.maybe_throw)

    ready()[[source]](../_modules/celery/result.html#ResultSet.ready)
    :   Did all of the tasks complete? (either by success of failure).

        Returns:
        :   true if all of the tasks have been executed.

        Return type:
        :   [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")

    remove(*result*)[[source]](../_modules/celery/result.html#ResultSet.remove)
    :   Remove result from the set; it must be a member.

        Raises:
        :   [**KeyError**](https://docs.python.org/dev/library/exceptions.html#KeyError "(in Python v3.15)") – if the result isn’t a member.

    results = None
    :   List of results in in the set.

    revoke(*connection=None*, *terminate=False*, *signal=None*, *wait=False*, *timeout=None*)[[source]](../_modules/celery/result.html#ResultSet.revoke)
    :   Send revoke signal to all workers for all tasks in the set.

        Parameters:
        :   - **terminate** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Also terminate the process currently working
              on the task (if any).
            - **signal** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of signal to send to process if terminate.
              Default is TERM.
            - **wait** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Wait for replies from worker.
              The `timeout` argument specifies the number of seconds
              to wait. Disabled by default.
            - **timeout** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time in seconds to wait for replies when
              the `wait` argument is enabled.

    successful()[[source]](../_modules/celery/result.html#ResultSet.successful)
    :   Return true if all tasks successful.

        Returns:
        :   true if all of the tasks finished
            :   successfully (i.e. didn’t raise an exception).

        Return type:
        :   [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")

    property supports\_native\_join

    then(*callback*, *on\_error=None*, *weak=False*)[[source]](../_modules/celery/result.html#ResultSet.then)

    update(*results*)[[source]](../_modules/celery/result.html#ResultSet.update)
    :   Extend from iterable of results.

    waiting()[[source]](../_modules/celery/result.html#ResultSet.waiting)
    :   Return true if any of the tasks are incomplete.

        Returns:
        :   true if one of the tasks are still
            :   waiting for execution.

        Return type:
        :   [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")

celery.result.result\_from\_tuple(*r*, *app=None*)[[source]](../_modules/celery/result.html#result_from_tuple)
:   Deserialize result from tuple.