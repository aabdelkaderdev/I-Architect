<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.bin.worker.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.bin.worker.html).

# `celery.bin.worker`

Program used to start a Celery worker instance.

class celery.bin.worker.Autoscale[[source]](../_modules/celery/bin/worker.html#Autoscale)
:   Autoscaling parameter.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/worker.html#Autoscale.convert)
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   - **value** – The value to convert.
            - **param** – The parameter that is using this type to convert
              its value. May be `None`.
            - **ctx** – The current context that arrived at this value. May
              be `None`.

    name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = '<min workers>, <max workers>'
    :   the descriptive name of this type

class celery.bin.worker.CeleryBeat[[source]](../_modules/celery/bin/worker.html#CeleryBeat)
:   Celery Beat flag.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/worker.html#CeleryBeat.convert)
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   - **value** – The value to convert.
            - **param** – The parameter that is using this type to convert
              its value. May be `None`.
            - **ctx** – The current context that arrived at this value. May
              be `None`.

    name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'beat'
    :   the descriptive name of this type

class celery.bin.worker.Hostname[[source]](../_modules/celery/bin/worker.html#Hostname)
:   Hostname option.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/worker.html#Hostname.convert)
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   - **value** – The value to convert.
            - **param** – The parameter that is using this type to convert
              its value. May be `None`.
            - **ctx** – The current context that arrived at this value. May
              be `None`.

    name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'hostname'
    :   the descriptive name of this type

class celery.bin.worker.WorkersPool[[source]](../_modules/celery/bin/worker.html#WorkersPool)
:   Workers pool option.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/worker.html#WorkersPool.convert)
    :   For a given value from the parser, normalize it and find its
        matching normalized value in the list of choices. Then return the
        matched “original” choice.

    name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'pool'
    :   the descriptive name of this type

celery.bin.worker.detach(*path*, *argv*, *logfile=None*, *pidfile=None*, *uid=None*, *gid=None*, *umask=None*, *workdir=None*, *fake=False*, *app=None*, *executable=None*, *hostname=None*)[[source]](../_modules/celery/bin/worker.html#detach)
:   Detach program by argv.