<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.utils.debug.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.utils.debug.html).

# `celery.utils.debug`

## 

This module can be used to diagnose and sample the memory usage
used by parts of your application.

For example, to sample the memory usage of calling tasks you can do this:

```
from celery.utils.debug import sample_mem, memdump

from tasks import add

try:
    for i in range(100):
        for j in range(100):
            add.delay(i, j)
        sample_mem()
finally:
    memdump()
```

## 

Utilities for debugging memory usage, blocking calls, etc.

celery.utils.debug.sample\_mem()[[source]](../_modules/celery/utils/debug.html#sample_mem)
:   Sample RSS memory usage.

    Statistics can then be output by calling [`memdump()`](#celery.utils.debug.memdump "celery.utils.debug.memdump").

celery.utils.debug.memdump(*samples=10*, *file=None*)[[source]](../_modules/celery/utils/debug.html#memdump)
:   Dump memory statistics.

    Will print a sample of all RSS memory samples added by
    calling [`sample_mem()`](#celery.utils.debug.sample_mem "celery.utils.debug.sample_mem"), and in addition print
    used RSS memory after [`gc.collect()`](https://docs.python.org/dev/library/gc.html#gc.collect "(in Python v3.15)").

celery.utils.debug.sample(*x*, *n*, *k=0*)[[source]](../_modules/celery/utils/debug.html#sample)
:   Given a list x a sample of length `n` of that list is returned.

    For example, if n is 10, and x has 100 items, a list of every tenth.
    item is returned.

    `k` can be used as offset.

celery.utils.debug.mem\_rss()[[source]](../_modules/celery/utils/debug.html#mem_rss)
:   Return RSS memory usage as a humanized string.

celery.utils.debug.ps()[[source]](../_modules/celery/utils/debug.html#ps)
:   Return the global `psutil.Process` instance.

    Note

    Returns `None` if <https://pypi.org/project/psutil/> is not installed.