<!-- Source: https://docs.celeryq.dev/en/main/_modules/celery/loaders/app.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/celery/loaders/app.html).

# Source code for celery.loaders.app

```
"""The default loader used with custom app instances."""
from .base import BaseLoader

__all__ = ('AppLoader',)

[docs]
class AppLoader(BaseLoader):
    """Default loader used when an app is specified."""
```