<!-- Source: https://docs.celeryq.dev/en/main/_modules/celery/security/utils.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/celery/security/utils.html).

# Source code for celery.security.utils

```
"""Utilities used by the message signing serializer."""
import sys
from contextlib import contextmanager

import cryptography.exceptions
from cryptography.hazmat.primitives import hashes

from celery.exceptions import SecurityError, reraise

__all__ = ('get_digest_algorithm', 'reraise_errors',)

[docs]
def get_digest_algorithm(digest='sha256'):
    """Convert string to hash object of cryptography library."""
    assert digest is not None
    return getattr(hashes, digest.upper())()

[docs]
@contextmanager
def reraise_errors(msg='{0!r}', errors=None):
    """Context reraising crypto errors as :exc:`SecurityError`."""
    errors = (cryptography.exceptions,) if errors is None else errors
    try:
        yield
    except errors as exc:
        reraise(SecurityError,
                SecurityError(msg.format(exc)),
                sys.exc_info()[2])
```