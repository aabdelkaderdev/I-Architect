<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.exceptions.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.exceptions.html).

# `celery.exceptions`

Celery error types.

## 

- [`Exception`](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)")
  :   - [`celery.exceptions.CeleryError`](#celery.exceptions.CeleryError "celery.exceptions.CeleryError")
        :   - [`ImproperlyConfigured`](#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured")
            - [`SecurityError`](#celery.exceptions.SecurityError "celery.exceptions.SecurityError")
            - [`TaskPredicate`](#celery.exceptions.TaskPredicate "celery.exceptions.TaskPredicate")
              :   - [`Ignore`](#celery.exceptions.Ignore "celery.exceptions.Ignore")
                  - [`Reject`](#celery.exceptions.Reject "celery.exceptions.Reject")
                  - [`Retry`](#celery.exceptions.Retry "celery.exceptions.Retry")
            - [`TaskError`](#celery.exceptions.TaskError "celery.exceptions.TaskError")
              :   - [`QueueNotFound`](#celery.exceptions.QueueNotFound "celery.exceptions.QueueNotFound")
                  - [`IncompleteStream`](#celery.exceptions.IncompleteStream "celery.exceptions.IncompleteStream")
                  - [`NotRegistered`](#celery.exceptions.NotRegistered "celery.exceptions.NotRegistered")
                  - [`AlreadyRegistered`](#celery.exceptions.AlreadyRegistered "celery.exceptions.AlreadyRegistered")
                  - [`TimeoutError`](#celery.exceptions.TimeoutError "celery.exceptions.TimeoutError")
                  - [`MaxRetriesExceededError`](#celery.exceptions.MaxRetriesExceededError "celery.exceptions.MaxRetriesExceededError")
                  - [`TaskRevokedError`](#celery.exceptions.TaskRevokedError "celery.exceptions.TaskRevokedError")
                  - [`InvalidTaskError`](#celery.exceptions.InvalidTaskError "celery.exceptions.InvalidTaskError")
                  - [`ChordError`](#celery.exceptions.ChordError "celery.exceptions.ChordError")
            - [`BackendError`](#celery.exceptions.BackendError "celery.exceptions.BackendError")
              :   - [`BackendGetMetaError`](#celery.exceptions.BackendGetMetaError "celery.exceptions.BackendGetMetaError")
                  - [`BackendStoreError`](#celery.exceptions.BackendStoreError "celery.exceptions.BackendStoreError")
      - `kombu.exceptions.KombuError`
        :   - [`OperationalError`](#celery.exceptions.OperationalError "celery.exceptions.OperationalError")

              > Raised when a transport connection error occurs while
              > sending a message (be it a task, remote control command error).
              >
              > Note
              >
              > This exception does not inherit from
              > [`CeleryError`](#celery.exceptions.CeleryError "celery.exceptions.CeleryError").
      - **billiard errors** (prefork pool)
        :   - [`SoftTimeLimitExceeded`](#celery.exceptions.SoftTimeLimitExceeded "celery.exceptions.SoftTimeLimitExceeded")
            - [`TimeLimitExceeded`](#celery.exceptions.TimeLimitExceeded "celery.exceptions.TimeLimitExceeded")
            - [`WorkerLostError`](#celery.exceptions.WorkerLostError "celery.exceptions.WorkerLostError")
            - [`Terminated`](#celery.exceptions.Terminated "celery.exceptions.Terminated")
- [`UserWarning`](https://docs.python.org/dev/library/exceptions.html#UserWarning "(in Python v3.15)")
  :   - [`CeleryWarning`](#celery.exceptions.CeleryWarning "celery.exceptions.CeleryWarning")
        :   - [`AlwaysEagerIgnored`](#celery.exceptions.AlwaysEagerIgnored "celery.exceptions.AlwaysEagerIgnored")
            - [`DuplicateNodenameWarning`](#celery.exceptions.DuplicateNodenameWarning "celery.exceptions.DuplicateNodenameWarning")
            - [`FixupWarning`](#celery.exceptions.FixupWarning "celery.exceptions.FixupWarning")
            - [`NotConfigured`](#celery.exceptions.NotConfigured "celery.exceptions.NotConfigured")
            - [`SecurityWarning`](#celery.exceptions.SecurityWarning "celery.exceptions.SecurityWarning")
- [`BaseException`](https://docs.python.org/dev/library/exceptions.html#BaseException "(in Python v3.15)")
  :   - [`SystemExit`](https://docs.python.org/dev/library/exceptions.html#SystemExit "(in Python v3.15)")
        :   - [`WorkerTerminate`](#celery.exceptions.WorkerTerminate "celery.exceptions.WorkerTerminate")
            - [`WorkerShutdown`](#celery.exceptions.WorkerShutdown "celery.exceptions.WorkerShutdown")

exception celery.exceptions.AlreadyRegistered[[source]](../_modules/celery/exceptions.html#AlreadyRegistered)
:   The task is already registered.

exception celery.exceptions.AlwaysEagerIgnored[[source]](../_modules/celery/exceptions.html#AlwaysEagerIgnored)
:   send\_task ignores [`task_always_eager`](../userguide/configuration.html#std-setting-task_always_eager) option.

exception celery.exceptions.BackendError[[source]](../_modules/celery/exceptions.html#BackendError)
:   An issue writing or reading to/from the backend.

exception celery.exceptions.BackendGetMetaError(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/exceptions.html#BackendGetMetaError)
:   An issue reading from the backend.

exception celery.exceptions.BackendStoreError(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/exceptions.html#BackendStoreError)
:   An issue writing to the backend.

exception celery.exceptions.CDeprecationWarning[[source]](../_modules/celery/exceptions.html#CDeprecationWarning)
:   Warning of deprecation.

exception celery.exceptions.CPendingDeprecationWarning[[source]](../_modules/celery/exceptions.html#CPendingDeprecationWarning)
:   Warning of pending deprecation.

exception celery.exceptions.CeleryCommandException(*message*, *exit\_code*)[[source]](../_modules/celery/exceptions.html#CeleryCommandException)
:   A general command exception which stores an exit code.

exception celery.exceptions.CeleryError[[source]](../_modules/celery/exceptions.html#CeleryError)
:   Base class for all Celery errors.

exception celery.exceptions.CeleryWarning[[source]](../_modules/celery/exceptions.html#CeleryWarning)
:   Base class for all Celery warnings.

exception celery.exceptions.ChordError[[source]](../_modules/celery/exceptions.html#ChordError)
:   A task part of the chord raised an exception.

exception celery.exceptions.DuplicateNodenameWarning[[source]](../_modules/celery/exceptions.html#DuplicateNodenameWarning)
:   Multiple workers are using the same nodename.

exception celery.exceptions.FixupWarning[[source]](../_modules/celery/exceptions.html#FixupWarning)
:   Fixup related warning.

exception celery.exceptions.Ignore[[source]](../_modules/celery/exceptions.html#Ignore)
:   A task can raise this to ignore doing state updates.

exception celery.exceptions.ImproperlyConfigured[[source]](../_modules/celery/exceptions.html#ImproperlyConfigured)
:   Celery is somehow improperly configured.

exception celery.exceptions.IncompleteStream[[source]](../_modules/celery/exceptions.html#IncompleteStream)
:   Found the end of a stream of data, but the data isn’t complete.

exception celery.exceptions.InvalidTaskError[[source]](../_modules/celery/exceptions.html#InvalidTaskError)
:   The task has invalid data or ain’t properly constructed.

exception celery.exceptions.MaxRetriesExceededError(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/exceptions.html#MaxRetriesExceededError)
:   The tasks max restart limit has been exceeded.

exception celery.exceptions.NotConfigured[[source]](../_modules/celery/exceptions.html#NotConfigured)
:   Celery hasn’t been configured, as no config module has been found.

exception celery.exceptions.NotRegistered[[source]](../_modules/celery/exceptions.html#NotRegistered)
:   The task is not registered.

exception celery.exceptions.OperationalError[[source]](../_modules/kombu/exceptions.html#OperationalError)
:   Recoverable message transport connection error.

exception celery.exceptions.QueueNotFound[[source]](../_modules/celery/exceptions.html#QueueNotFound)
:   Task routed to a queue not in `conf.queues`.

exception celery.exceptions.Reject(*reason=None*, *requeue=False*)[[source]](../_modules/celery/exceptions.html#Reject)
:   A task can raise this if it wants to reject/re-queue the message.

exception celery.exceptions.Retry(*message=None*, *exc=None*, *when=None*, *is\_eager=False*, *sig=None*, *\*\*kwargs*)[[source]](../_modules/celery/exceptions.html#Retry)
:   The task is to be retried later.

    exc = None
    :   Exception (if any) that caused the retry to happen.

    humanize()[[source]](../_modules/celery/exceptions.html#Retry.humanize)

    message = None
    :   Optional message describing context of retry.

    when = None
    :   Time of retry (ETA), either [`numbers.Real`](https://docs.python.org/dev/library/numbers.html#numbers.Real "(in Python v3.15)") or
        [`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)").

exception celery.exceptions.SecurityError[[source]](../_modules/celery/exceptions.html#SecurityError)
:   Security related exception.

exception celery.exceptions.SecurityWarning[[source]](../_modules/celery/exceptions.html#SecurityWarning)
:   Potential security issue found.

exception celery.exceptions.SoftTimeLimitExceeded[[source]](../_modules/billiard/exceptions.html#SoftTimeLimitExceeded)
:   The soft time limit has been exceeded. This exception is raised
    to give the task a chance to clean up.

exception celery.exceptions.TaskError[[source]](../_modules/celery/exceptions.html#TaskError)
:   Task related errors.

exception celery.exceptions.TaskPredicate[[source]](../_modules/celery/exceptions.html#TaskPredicate)
:   Base class for task-related semi-predicates.

exception celery.exceptions.TaskRevokedError[[source]](../_modules/celery/exceptions.html#TaskRevokedError)
:   The task has been revoked, so no result available.

exception celery.exceptions.Terminated[[source]](../_modules/billiard/exceptions.html#Terminated)
:   The worker processing a job has been terminated by user request.

exception celery.exceptions.TimeLimitExceeded[[source]](../_modules/billiard/exceptions.html#TimeLimitExceeded)
:   The time limit has been exceeded and the job has been terminated.

exception celery.exceptions.TimeoutError[[source]](../_modules/celery/exceptions.html#TimeoutError)
:   The operation timed out.

exception celery.exceptions.WorkerLostError[[source]](../_modules/billiard/exceptions.html#WorkerLostError)
:   The worker processing a job has exited prematurely.

exception celery.exceptions.WorkerShutdown[[source]](../_modules/celery/exceptions.html#WorkerShutdown)
:   Signals that the worker should perform a warm shutdown.

exception celery.exceptions.WorkerTerminate[[source]](../_modules/celery/exceptions.html#WorkerTerminate)
:   Signals that the worker should terminate immediately.

celery.exceptions.reraise(*tp*, *value*, *tb=None*)[[source]](../_modules/celery/exceptions.html#reraise)
:   Reraise exception.