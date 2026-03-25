<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.apps.multi.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.apps.multi.html).

# `celery.apps.multi`

Start/stop/manage workers.

class celery.apps.multi.Cluster(*nodes*, *cmd=None*, *env=None*, *on\_stopping\_preamble=None*, *on\_send\_signal=None*, *on\_still\_waiting\_for=None*, *on\_still\_waiting\_progress=None*, *on\_still\_waiting\_end=None*, *on\_node\_start=None*, *on\_node\_restart=None*, *on\_node\_shutdown\_ok=None*, *on\_node\_status=None*, *on\_node\_signal=None*, *on\_node\_signal\_dead=None*, *on\_node\_down=None*, *on\_child\_spawn=None*, *on\_child\_signalled=None*, *on\_child\_failure=None*)[[source]](../_modules/celery/apps/multi.html#Cluster)
:   Represent a cluster of workers.

    property data

    find(*name*)[[source]](../_modules/celery/apps/multi.html#Cluster.find)

    getpids(*on\_down=None*)[[source]](../_modules/celery/apps/multi.html#Cluster.getpids)

    kill()[[source]](../_modules/celery/apps/multi.html#Cluster.kill)

    restart(*sig=Signals.SIGTERM*)[[source]](../_modules/celery/apps/multi.html#Cluster.restart)

    send\_all(*sig*)[[source]](../_modules/celery/apps/multi.html#Cluster.send_all)

    shutdown\_nodes(*nodes*, *sig=Signals.SIGTERM*, *retry=None*)[[source]](../_modules/celery/apps/multi.html#Cluster.shutdown_nodes)

    start()[[source]](../_modules/celery/apps/multi.html#Cluster.start)

    start\_node(*node*)[[source]](../_modules/celery/apps/multi.html#Cluster.start_node)

    stop(*retry=None*, *callback=None*, *sig=Signals.SIGTERM*)[[source]](../_modules/celery/apps/multi.html#Cluster.stop)

    stopwait(*retry=2*, *callback=None*, *sig=Signals.SIGTERM*)[[source]](../_modules/celery/apps/multi.html#Cluster.stopwait)

class celery.apps.multi.Node(*name*, *cmd=None*, *append=None*, *options=None*, *extra\_args=None*)[[source]](../_modules/celery/apps/multi.html#Node)
:   Represents a node in a cluster.

    alive()[[source]](../_modules/celery/apps/multi.html#Node.alive)

    property argv\_with\_executable

    property executable

    classmethod from\_kwargs(*name*, *\*\*kwargs*)[[source]](../_modules/celery/apps/multi.html#Node.from_kwargs)

    getopt(*\*alt*)[[source]](../_modules/celery/apps/multi.html#Node.getopt)

    handle\_process\_exit(*retcode*, *on\_signalled=None*, *on\_failure=None*)[[source]](../_modules/celery/apps/multi.html#Node.handle_process_exit)

    property logfile

    property pid

    property pidfile

    prepare\_argv(*argv*, *path*)[[source]](../_modules/celery/apps/multi.html#Node.prepare_argv)

    send(*sig*, *on\_error=None*)[[source]](../_modules/celery/apps/multi.html#Node.send)

    start(*env=None*, *\*\*kwargs*)[[source]](../_modules/celery/apps/multi.html#Node.start)