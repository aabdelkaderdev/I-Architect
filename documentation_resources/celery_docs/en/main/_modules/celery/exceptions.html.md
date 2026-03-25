<!-- Source: https://docs.celeryq.dev/en/main/_modules/celery/exceptions.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/celery/exceptions.html).

# Source code for celery.exceptions

```
"""Celery error types.

Error Hierarchy
===============

- :exc:`Exception`
    - :exc:`celery.exceptions.CeleryError`
        - :exc:`~celery.exceptions.ImproperlyConfigured`
        - :exc:`~celery.exceptions.SecurityError`
        - :exc:`~celery.exceptions.TaskPredicate`
            - :exc:`~celery.exceptions.Ignore`
            - :exc:`~celery.exceptions.Reject`
            - :exc:`~celery.exceptions.Retry`
        - :exc:`~celery.exceptions.TaskError`
            - :exc:`~celery.exceptions.QueueNotFound`
            - :exc:`~celery.exceptions.IncompleteStream`
            - :exc:`~celery.exceptions.NotRegistered`
            - :exc:`~celery.exceptions.AlreadyRegistered`
            - :exc:`~celery.exceptions.TimeoutError`
            - :exc:`~celery.exceptions.MaxRetriesExceededError`
            - :exc:`~celery.exceptions.TaskRevokedError`
            - :exc:`~celery.exceptions.InvalidTaskError`
            - :exc:`~celery.exceptions.ChordError`
        - :exc:`~celery.exceptions.BackendError`
            - :exc:`~celery.exceptions.BackendGetMetaError`
            - :exc:`~celery.exceptions.BackendStoreError`
    - :class:`kombu.exceptions.KombuError`
        - :exc:`~celery.exceptions.OperationalError`

            Raised when a transport connection error occurs while
            sending a message (be it a task, remote control command error).

            .. note::
                This exception does not inherit from
                :exc:`~celery.exceptions.CeleryError`.
    - **billiard errors** (prefork pool)
        - :exc:`~celery.exceptions.SoftTimeLimitExceeded`
        - :exc:`~celery.exceptions.TimeLimitExceeded`
        - :exc:`~celery.exceptions.WorkerLostError`
        - :exc:`~celery.exceptions.Terminated`
- :class:`UserWarning`
    - :class:`~celery.exceptions.CeleryWarning`
        - :class:`~celery.exceptions.AlwaysEagerIgnored`
        - :class:`~celery.exceptions.DuplicateNodenameWarning`
        - :class:`~celery.exceptions.FixupWarning`
        - :class:`~celery.exceptions.NotConfigured`
        - :class:`~celery.exceptions.SecurityWarning`
- :exc:`BaseException`
    - :exc:`SystemExit`
        - :exc:`~celery.exceptions.WorkerTerminate`
        - :exc:`~celery.exceptions.WorkerShutdown`
"""

import numbers

from billiard.exceptions import SoftTimeLimitExceeded, Terminated, TimeLimitExceeded, WorkerLostError
from click import ClickException
from kombu.exceptions import OperationalError

__all__ = (
    'reraise',
    # Warnings
    'CeleryWarning',
    'AlwaysEagerIgnored', 'DuplicateNodenameWarning',
    'FixupWarning', 'NotConfigured', 'SecurityWarning',

    # Core errors
    'CeleryError',
    'ImproperlyConfigured', 'SecurityError',

    # Kombu (messaging) errors.
    'OperationalError',

    # Task semi-predicates
    'TaskPredicate', 'Ignore', 'Reject', 'Retry',

    # Task related errors.
    'TaskError', 'QueueNotFound', 'IncompleteStream',
    'NotRegistered', 'AlreadyRegistered', 'TimeoutError',
    'MaxRetriesExceededError', 'TaskRevokedError',
    'InvalidTaskError', 'ChordError',

    # Backend related errors.
    'BackendError', 'BackendGetMetaError', 'BackendStoreError',

    # Billiard task errors.
    'SoftTimeLimitExceeded', 'TimeLimitExceeded',
    'WorkerLostError', 'Terminated',

    # Deprecation warnings (forcing Python to emit them).
    'CPendingDeprecationWarning', 'CDeprecationWarning',

    # Worker shutdown semi-predicates (inherits from SystemExit).
    'WorkerShutdown', 'WorkerTerminate',

    'CeleryCommandException',
)

from celery.utils.serialization import get_pickleable_exception

UNREGISTERED_FMT = """\
Task of kind {0} never registered, please make sure it's imported.\
"""

[docs]
def reraise(tp, value, tb=None):
    """Reraise exception."""
    if value.__traceback__ is not tb:
        raise value.with_traceback(tb)
    raise value

[docs]
class CeleryWarning(UserWarning):
    """Base class for all Celery warnings."""

[docs]
class AlwaysEagerIgnored(CeleryWarning):
    """send_task ignores :setting:`task_always_eager` option."""

[docs]
class DuplicateNodenameWarning(CeleryWarning):
    """Multiple workers are using the same nodename."""

[docs]
class FixupWarning(CeleryWarning):
    """Fixup related warning."""

[docs]
class NotConfigured(CeleryWarning):
    """Celery hasn't been configured, as no config module has been found."""

[docs]
class SecurityWarning(CeleryWarning):
    """Potential security issue found."""

[docs]
class CeleryError(Exception):
    """Base class for all Celery errors."""

[docs]
class TaskPredicate(CeleryError):
    """Base class for task-related semi-predicates."""

[docs]
class Retry(TaskPredicate):
    """The task is to be retried later."""

    #: Optional message describing context of retry.
    message = None

    #: Exception (if any) that caused the retry to happen.
    exc = None

    #: Time of retry (ETA), either :class:`numbers.Real` or
    #: :class:`~datetime.datetime`.
    when = None

    def __init__(self, message=None, exc=None, when=None, is_eager=False,
                 sig=None, **kwargs):
        from kombu.utils.encoding import safe_repr
        self.message = message
        if isinstance(exc, str):
            self.exc, self.excs = None, exc
        else:
            self.exc, self.excs = get_pickleable_exception(exc), safe_repr(exc) if exc else None
        self.when = when
        self.is_eager = is_eager
        self.sig = sig
        super().__init__(self, exc, when, **kwargs)

[docs]
    def humanize(self):
        if isinstance(self.when, numbers.Number):
            return f'in {self.when}s'
        return f'at {self.when}'

def __str__(self):
        if self.message:
            return self.message
        if self.excs:
            return f'Retry {self.humanize()}: {self.excs}'
        return f'Retry {self.humanize()}'

    def __reduce__(self):
        return self.__class__, (self.message, self.exc, self.when)

RetryTaskError = Retry  # XXX compat

[docs]
class Ignore(TaskPredicate):
    """A task can raise this to ignore doing state updates."""

[docs]
class Reject(TaskPredicate):
    """A task can raise this if it wants to reject/re-queue the message."""

    def __init__(self, reason=None, requeue=False):
        self.reason = reason
        self.requeue = requeue
        super().__init__(reason, requeue)

    def __repr__(self):
        return f'reject requeue={self.requeue}: {self.reason}'

[docs]
class ImproperlyConfigured(CeleryError):
    """Celery is somehow improperly configured."""

[docs]
class SecurityError(CeleryError):
    """Security related exception."""

[docs]
class TaskError(CeleryError):
    """Task related errors."""

[docs]
class QueueNotFound(KeyError, TaskError):
    """Task routed to a queue not in ``conf.queues``."""

[docs]
class IncompleteStream(TaskError):
    """Found the end of a stream of data, but the data isn't complete."""

[docs]
class NotRegistered(KeyError, TaskError):
    """The task is not registered."""

    def __repr__(self):
        return UNREGISTERED_FMT.format(self)

[docs]
class AlreadyRegistered(TaskError):
    """The task is already registered."""

# XXX Unused

[docs]
class TimeoutError(TaskError):
    """The operation timed out."""

[docs]
class MaxRetriesExceededError(TaskError):
    """The tasks max restart limit has been exceeded."""

    def __init__(self, *args, **kwargs):
        self.task_args = kwargs.pop("task_args", [])
        self.task_kwargs = kwargs.pop("task_kwargs", dict())
        super().__init__(*args, **kwargs)

[docs]
class TaskRevokedError(TaskError):
    """The task has been revoked, so no result available."""

[docs]
class InvalidTaskError(TaskError):
    """The task has invalid data or ain't properly constructed."""

[docs]
class ChordError(TaskError):
    """A task part of the chord raised an exception."""

[docs]
class CPendingDeprecationWarning(PendingDeprecationWarning):
    """Warning of pending deprecation."""

[docs]
class CDeprecationWarning(DeprecationWarning):
    """Warning of deprecation."""

[docs]
class WorkerTerminate(SystemExit):
    """Signals that the worker should terminate immediately."""

SystemTerminate = WorkerTerminate  # XXX compat

[docs]
class WorkerShutdown(SystemExit):
    """Signals that the worker should perform a warm shutdown."""

[docs]
class BackendError(Exception):
    """An issue writing or reading to/from the backend."""

[docs]
class BackendGetMetaError(BackendError):
    """An issue reading from the backend."""

    def __init__(self, *args, **kwargs):
        self.task_id = kwargs.get('task_id', "")

    def __repr__(self):
        return super().__repr__() + " task_id:" + self.task_id

[docs]
class BackendStoreError(BackendError):
    """An issue writing to the backend."""

    def __init__(self, *args, **kwargs):
        self.state = kwargs.get('state', "")
        self.task_id = kwargs.get('task_id', "")

    def __repr__(self):
        return super().__repr__() + " state:" + self.state + " task_id:" + self.task_id

[docs]
class CeleryCommandException(ClickException):
    """A general command exception which stores an exit code."""

    def __init__(self, message, exit_code):
        super().__init__(message=message)
        self.exit_code = exit_code
```