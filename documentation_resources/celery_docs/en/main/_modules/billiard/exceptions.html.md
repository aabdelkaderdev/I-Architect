<!-- Source: https://docs.celeryq.dev/en/main/_modules/billiard/exceptions.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/billiard/exceptions.html).

# Source code for billiard.exceptions

```
try:
    from multiprocessing import (
        ProcessError,
        BufferTooShort,
        TimeoutError,
        AuthenticationError,
    )
except ImportError:
    class ProcessError(Exception):             # noqa
        pass

    class BufferTooShort(ProcessError):        # noqa
        pass

    class TimeoutError(ProcessError):          # noqa
        pass

    class AuthenticationError(ProcessError):   # noqa
        pass

[docs]
class TimeLimitExceeded(Exception):
    """The time limit has been exceeded and the job has been terminated."""

    def __str__(self):
        return "TimeLimitExceeded%s" % (self.args, )

[docs]
class SoftTimeLimitExceeded(Exception):
    """The soft time limit has been exceeded. This exception is raised
    to give the task a chance to clean up."""

    def __str__(self):
        return "SoftTimeLimitExceeded%s" % (self.args, )

[docs]
class WorkerLostError(Exception):
    """The worker processing a job has exited prematurely."""

[docs]
class Terminated(Exception):
    """The worker processing a job has been terminated by user request."""

class RestartFreqExceeded(Exception):
    """Restarts too fast."""

class CoroStop(Exception):
    """Coroutine exit, as opposed to StopIteration which may
    mean it should be restarted."""
    pass
```