<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.state.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.state.html).

# `celery.worker.state`

Internal worker state (global).

This includes the currently active and reserved tasks,
statistics, and revoked tasks.

class celery.worker.state.Persistent(*state*, *filename*, *clock=None*)[[source]](../_modules/celery/worker/state.html#Persistent)
:   Stores worker state between restarts.

    This is the persistent data stored by the worker when
    [`celery worker --statedb`](cli.html#cmdoption-celery-worker-S) is enabled.

    Currently only stores revoked task id’s.

    close()[[source]](../_modules/celery/worker/state.html#Persistent.close)

    compress(*data*, */*, *level=-1*, *wbits=15*)
    :   Returns a bytes object containing compressed data.

        data
        :   Binary data to be compressed.

        level
        :   Compression level, in 0-9 or -1.

        wbits
        :   The window buffer size and container format.

    property db

    decompress(*data*, */*, *wbits=15*, *bufsize=16384*)
    :   Returns a bytes object containing the uncompressed data.

        data
        :   Compressed data.

        wbits
        :   The window buffer size and container format.

        bufsize
        :   The initial output buffer size.

    merge()[[source]](../_modules/celery/worker/state.html#Persistent.merge)

    open()[[source]](../_modules/celery/worker/state.html#Persistent.open)

    protocol = 4

    save()[[source]](../_modules/celery/worker/state.html#Persistent.save)

    storage = <module 'shelve' from '/home/docs/.asdf/installs/python/3.11.12/lib/python3.11/shelve.py'>

    sync()[[source]](../_modules/celery/worker/state.html#Persistent.sync)

celery.worker.state.SOFTWARE\_INFO = {'sw\_ident': 'py-celery', 'sw\_sys': 'Linux', 'sw\_ver': '5.6.2'}
:   Worker software/platform information.

celery.worker.state.active\_requests = set()
:   set of currently active [`Request`](celery.worker.request.html#celery.worker.request.Request "celery.worker.request.Request")’s.

celery.worker.state.maybe\_shutdown()[[source]](../_modules/celery/worker/state.html#maybe_shutdown)
:   Shutdown if flags have been set.

celery.worker.state.reserved\_requests = set()
:   set of all reserved [`Request`](celery.worker.request.html#celery.worker.request.Request "celery.worker.request.Request")’s.

celery.worker.state.revoked = <LimitedSet(0): maxlen=50000, expires=10800.0, minlen=0>
:   the list of currently revoked tasks. Persistent if `statedb` set.

celery.worker.state.task\_accepted(*request*, *\_all\_total\_count=None*, *add\_request=<method-wrapper '\_\_setitem\_\_' of dict object>*, *add\_active\_request=<bound method WeakSet.add of set()>*, *add\_to\_total\_count=<bound method Counter.update of Counter()>*)[[source]](../_modules/celery/worker/state.html#task_accepted)
:   Update global state when a task has been accepted.

celery.worker.state.task\_ready(*request*, *successful=False*, *remove\_request=<built-in method pop of dict object>*, *discard\_active\_request=<bound method WeakSet.discard of set()>*, *discard\_reserved\_request=<bound method WeakSet.discard of set()>*)[[source]](../_modules/celery/worker/state.html#task_ready)
:   Update global state when a task is ready.

celery.worker.state.task\_reserved(*request*, *add\_request=<method-wrapper '\_\_setitem\_\_' of dict object>*, *add\_reserved\_request=<bound method WeakSet.add of set()>*)[[source]](../_modules/celery/worker/state.html#task_reserved)
:   Update global state when a task has been reserved.

celery.worker.state.total\_count = {}
:   count of tasks accepted by the worker, sorted by type.