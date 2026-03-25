<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.saferepr.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.saferepr.html).

# `celery.utils.saferepr`

Streaming, truncating, non-recursive version of [`repr()`](https://docs.python.org/dev/library/functions.html#repr "(in Python v3.15)").

Differences from regular [`repr()`](https://docs.python.org/dev/library/functions.html#repr "(in Python v3.15)"):

- Sets are represented the Python 3 way: `{1, 2}` vs `set([1, 2])`.
- Unicode strings does not have the `u'` prefix, even on Python 2.
- Empty set formatted as `set()` (Python 3), not `set([])` (Python 2).
- Longs don’t have the `L` suffix.

Very slow with no limits, super quick with limits.

celery.utils.saferepr.reprstream(*stack: [deque](https://docs.python.org/dev/library/collections.html#collections.deque "(in Python v3.15)")*, *seen: [Set](https://docs.python.org/dev/library/typing.html#typing.Set "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *maxlevels: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 3*, *level: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 0*, *isinstance: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)") = <built-in function isinstance>*) → [Iterator](https://docs.python.org/dev/library/typing.html#typing.Iterator "(in Python v3.15)")[[Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")][[source]](../../_modules/celery/utils/saferepr.html#reprstream)
:   Streaming repr, yielding tokens.

celery.utils.saferepr.saferepr(*o: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *maxlen: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = None*, *maxlevels: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 3*, *seen: [Set](https://docs.python.org/dev/library/typing.html#typing.Set "(in Python v3.15)") = None*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/saferepr.html#saferepr)
:   Safe version of [`repr()`](https://docs.python.org/dev/library/functions.html#repr "(in Python v3.15)").

    Warning

    Make sure you set the maxlen argument, or it will be very slow
    for recursive objects. With the maxlen set, it’s often faster
    than built-in repr.