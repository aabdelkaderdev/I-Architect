<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.deprecated.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.deprecated.html).

# `celery.utils.deprecated`

Deprecation utilities.

celery.utils.deprecated.Callable(*deprecation=None*, *removal=None*, *alternative=None*, *description=None*)[[source]](../../_modules/celery/utils/deprecated.html#Callable)
:   Decorator for deprecated functions.

    A deprecation warning will be emitted when the function is called.

    Parameters:
    :   - **deprecation** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Version that marks first deprecation, if this
          argument isn’t set a `PendingDeprecationWarning` will be
          emitted instead.
        - **removal** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Future version when this feature will be removed.
        - **alternative** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Instructions for an alternative solution (if any).
        - **description** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Description of what’s being deprecated.

celery.utils.deprecated.Property(*deprecation=None*, *removal=None*, *alternative=None*, *description=None*)[[source]](../../_modules/celery/utils/deprecated.html#Property)
:   Decorator for deprecated properties.

celery.utils.deprecated.warn(*description=None*, *deprecation=None*, *removal=None*, *alternative=None*, *stacklevel=2*)[[source]](../../_modules/celery/utils/deprecated.html#warn)
:   Warn of (pending) deprecation.