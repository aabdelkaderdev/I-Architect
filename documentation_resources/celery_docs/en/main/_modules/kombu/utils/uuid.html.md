<!-- Source: https://docs.celeryq.dev/en/main/_modules/kombu/utils/uuid.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/kombu/utils/uuid.html).

# Source code for kombu.utils.uuid

```
"""UUID utilities."""
from __future__ import annotations

from typing import Callable
from uuid import UUID, uuid4

[docs]
def uuid(_uuid: Callable[[], UUID] = uuid4) -> str:
    """Generate unique id in UUID4 format.

    See Also
    --------
        For now this is provided by :func:`uuid.uuid4`.
    """
    return str(_uuid())
```