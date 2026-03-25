<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.sysinfo.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.sysinfo.html).

# `celery.utils.sysinfo`

System information utilities.

class celery.utils.sysinfo.df(*path: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [bytes](https://docs.python.org/dev/library/stdtypes.html#bytes "(in Python v3.15)") | [PathLike](https://docs.python.org/dev/library/os.html#os.PathLike "(in Python v3.15)")*)[[source]](../../_modules/celery/utils/sysinfo.html#df)
:   Disk information.

    property available: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")

    property capacity: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")

    property stat: statvfs\_result

    property total\_blocks: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")

celery.utils.sysinfo.load\_average() → [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)"), ...][[source]](../../_modules/celery/utils/sysinfo.html#load_average)
:   Return system load average as a triple.