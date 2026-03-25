<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.nodenames.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.nodenames.html).

# `celery.utils.nodenames`

Worker name utilities.

celery.utils.nodenames.anon\_nodename(*hostname: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *prefix: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'gen'*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/nodenames.html#anon_nodename)
:   Return the nodename for this process (not a worker).

    This is used for e.g. the origin task message field.

celery.utils.nodenames.default\_nodename(*hostname: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/nodenames.html#default_nodename)
:   Return the default nodename for this process.

celery.utils.nodenames.gethostname() → string
:   Return the current host name.

celery.utils.nodenames.host\_format(*s: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *host: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *\*\*extra: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/nodenames.html#host_format)
:   Format host %x abbreviations.

celery.utils.nodenames.node\_format(*s: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *\*\*extra: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/nodenames.html#node_format)
:   Format worker node name ([name@host.com](mailto:name%40host.com)).

celery.utils.nodenames.nodename(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *hostname: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/nodenames.html#nodename)
:   Create node name from name/hostname pair.

celery.utils.nodenames.nodesplit(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)"), [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")] | [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")][[source]](../../_modules/celery/utils/nodenames.html#nodesplit)
:   Split node name into tuple of name/hostname.

celery.utils.nodenames.worker\_direct(*hostname: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [Queue](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)")*) → [Queue](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)")[[source]](../../_modules/celery/utils/nodenames.html#worker_direct)
:   Return the [`kombu.Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") being a direct route to a worker.

    Parameters:
    :   **hostname** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*Queue*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)")) – The fully qualified node name of
        a worker (e.g., `w1@example.com`). If passed a
        [`kombu.Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") instance it will simply return
        that instead.