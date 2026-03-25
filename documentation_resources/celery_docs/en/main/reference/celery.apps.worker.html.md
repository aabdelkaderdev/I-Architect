<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.apps.worker.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.apps.worker.html).

# `celery.apps.worker`

Worker command-line program.

This module is the ‘program-version’ of [`celery.worker`](celery.worker.html#module-celery.worker "celery.worker").

It does everything necessary to run that module
as an actual application, like installing signal handlers,
platform tweaks, and so on.

class celery.apps.worker.Worker(*app=None*, *hostname=None*, *\*\*kwargs*)[[source]](../_modules/celery/apps/worker.html#Worker)
:   Worker as a program.

    emit\_banner()[[source]](../_modules/celery/apps/worker.html#Worker.emit_banner)

    extra\_info()[[source]](../_modules/celery/apps/worker.html#Worker.extra_info)

    install\_platform\_tweaks(*worker*)[[source]](../_modules/celery/apps/worker.html#Worker.install_platform_tweaks)
    :   Install platform specific tweaks and workarounds.

    macOS\_proxy\_detection\_workaround()[[source]](../_modules/celery/apps/worker.html#Worker.macOS_proxy_detection_workaround)
    :   See <https://github.com/celery/celery/issues#issue/161>.

    on\_after\_init(*purge=False*, *no\_color=None*, *redirect\_stdouts=None*, *redirect\_stdouts\_level=None*, *\*\*kwargs*)[[source]](../_modules/celery/apps/worker.html#Worker.on_after_init)

    on\_before\_init(*quiet=False*, *\*\*kwargs*)[[source]](../_modules/celery/apps/worker.html#Worker.on_before_init)

    on\_consumer\_ready(*consumer*)[[source]](../_modules/celery/apps/worker.html#Worker.on_consumer_ready)

    on\_init\_blueprint()[[source]](../_modules/celery/apps/worker.html#Worker.on_init_blueprint)

    on\_start()[[source]](../_modules/celery/apps/worker.html#Worker.on_start)

    purge\_messages()[[source]](../_modules/celery/apps/worker.html#Worker.purge_messages)

    set\_process\_status(*info*)[[source]](../_modules/celery/apps/worker.html#Worker.set_process_status)

    setup\_logging(*colorize=None*)[[source]](../_modules/celery/apps/worker.html#Worker.setup_logging)

    startup\_info(*artlines=True*)[[source]](../_modules/celery/apps/worker.html#Worker.startup_info)

    tasklist(*include\_builtins=True*, *sep='\n'*, *int\_='celery.'*)[[source]](../_modules/celery/apps/worker.html#Worker.tasklist)