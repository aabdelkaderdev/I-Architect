<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.apps.beat.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.apps.beat.html).

# `celery.apps.beat`

Beat command-line program.

This module is the ‘program-version’ of [`celery.beat`](celery.beat.html#module-celery.beat "celery.beat").

It does everything necessary to run that module
as an actual application, like installing signal handlers
and so on.

class celery.apps.beat.Beat(*max\_interval: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *app: [Celery](celery.html#celery.Celery "celery.app.base.Celery") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *socket\_timeout: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 30*, *pidfile: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *no\_color: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *loglevel: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'WARN'*, *logfile: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *schedule: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *scheduler: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *scheduler\_cls: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *redirect\_stdouts: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *redirect\_stdouts\_level: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *quiet: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../_modules/celery/apps/beat.html#Beat)
:   Beat as a service.

    class Service(*app*, *max\_interval=None*, *schedule\_filename=None*, *scheduler\_cls=None*)
    :   Celery periodic task service.

        get\_scheduler(*lazy=False*, *extension\_namespace='celery.beat\_schedulers'*)

        property scheduler

        scheduler\_cls
        :   alias of [`PersistentScheduler`](celery.beat.html#celery.beat.PersistentScheduler "celery.beat.PersistentScheduler")

        start(*embedded\_process=False*)

        stop(*wait=False*)

        sync()

    app: [Celery](celery.html#celery.Celery "celery.app.base.Celery") = None

    banner(*service: [Service](celery.beat.html#celery.beat.Service "celery.beat.Service")*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/celery/apps/beat.html#Beat.banner)

    init\_loader() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/apps/beat.html#Beat.init_loader)

    install\_sync\_handler(*service: [Service](celery.beat.html#celery.beat.Service "celery.beat.Service")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/apps/beat.html#Beat.install_sync_handler)
    :   Install a SIGTERM + SIGINT handler saving the schedule.

    run() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/apps/beat.html#Beat.run)

    set\_process\_title() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/apps/beat.html#Beat.set_process_title)

    setup\_logging(*colorize: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/apps/beat.html#Beat.setup_logging)

    start\_scheduler() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/apps/beat.html#Beat.start_scheduler)

    startup\_info(*service: [Service](celery.beat.html#celery.beat.Service "celery.beat.Service")*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../_modules/celery/apps/beat.html#Beat.startup_info)