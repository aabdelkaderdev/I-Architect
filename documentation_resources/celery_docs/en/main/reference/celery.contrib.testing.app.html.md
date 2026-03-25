<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.contrib.testing.app.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.testing.app.html).

# `celery.contrib.testing.app`

## 

Create Celery app instances used for testing.

celery.contrib.testing.app.DEFAULT\_TEST\_CONFIG = {'accept\_content': {'json'}, 'broker\_heartbeat': 0, 'broker\_url': 'memory://', 'enable\_utc': True, 'result\_backend': 'cache+memory://', 'timezone': 'UTC', 'worker\_hijack\_root\_logger': False, 'worker\_log\_color': False}
:   Contains the default configuration values for the test app.

celery.contrib.testing.app.TestApp(*name=None*, *config=None*, *enable\_logging=False*, *set\_as\_current=False*, *log=<class 'celery.contrib.testing.app.UnitLogging'>*, *backend=None*, *broker=None*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/app.html#TestApp)
:   App used for testing.

class celery.contrib.testing.app.Trap[[source]](../_modules/celery/contrib/testing/app.html#Trap)
:   Trap that pretends to be an app but raises an exception instead.

    This to protect from code that does not properly pass app instances,
    then falls back to the current\_app.

class celery.contrib.testing.app.UnitLogging(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/app.html#UnitLogging)
:   Sets up logging for the test application.

celery.contrib.testing.app.set\_trap(*app*)[[source]](../_modules/celery/contrib/testing/app.html#set_trap)
:   Contextmanager that installs the trap app.

    The trap means that anything trying to use the current or default app
    will raise an exception.

celery.contrib.testing.app.setup\_default\_app(*app*, *use\_trap=False*)[[source]](../_modules/celery/contrib/testing/app.html#setup_default_app)
:   Setup default app for testing.

    Ensures state is clean after the test returns.