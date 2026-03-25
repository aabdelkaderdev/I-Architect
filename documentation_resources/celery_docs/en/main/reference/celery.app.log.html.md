<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.app.log.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.log.html).

# `celery.app.log`

Logging configuration.

The Celery instances logging section: `Celery.log`.

Sets up logging for the worker and other programs,
redirects standard outs, colors log output, patches logging
related compatibility fixes, and so on.

class celery.app.log.Logging(*app*)[[source]](../_modules/celery/app/log.html#Logging)
:   Application logging setup (app.log).

    already\_setup = False

    colored(*logfile=None*, *enabled=None*)[[source]](../_modules/celery/app/log.html#Logging.colored)

    get\_default\_logger(*name='celery'*, *\*\*kwargs*)[[source]](../_modules/celery/app/log.html#Logging.get_default_logger)

    redirect\_stdouts(*loglevel=None*, *name='celery.redirected'*)[[source]](../_modules/celery/app/log.html#Logging.redirect_stdouts)

    redirect\_stdouts\_to\_logger(*logger*, *loglevel=None*, *stdout=True*, *stderr=True*)[[source]](../_modules/celery/app/log.html#Logging.redirect_stdouts_to_logger)
    :   Redirect `sys.stdout` and `sys.stderr` to logger.

        Parameters:
        :   - **logger** ([*logging.Logger*](https://docs.python.org/dev/library/logging.html#logging.Logger "(in Python v3.15)")) – Logger instance to redirect to.
            - **loglevel** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – The loglevel redirected message
              will be logged as.

    setup(*loglevel=None*, *logfile=None*, *redirect\_stdouts=False*, *redirect\_level='WARNING'*, *colorize=None*, *hostname=None*)[[source]](../_modules/celery/app/log.html#Logging.setup)

    setup\_handlers(*logger*, *logfile*, *format*, *colorize*, *formatter=<class 'celery.utils.log.ColorFormatter'>*, *\*\*kwargs*)[[source]](../_modules/celery/app/log.html#Logging.setup_handlers)

    setup\_logging\_subsystem(*loglevel=None*, *logfile=None*, *format=None*, *colorize=None*, *hostname=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/log.html#Logging.setup_logging_subsystem)

    setup\_task\_loggers(*loglevel=None*, *logfile=None*, *format=None*, *colorize=None*, *propagate=False*, *\*\*kwargs*)[[source]](../_modules/celery/app/log.html#Logging.setup_task_loggers)
    :   Setup the task logger.

        If logfile is not specified, then sys.stderr is used.

        Will return the base task logger object.

    supports\_color(*colorize=None*, *logfile=None*)[[source]](../_modules/celery/app/log.html#Logging.supports_color)

class celery.app.log.TaskFormatter(*fmt=None*, *use\_color=True*)[[source]](../_modules/celery/app/log.html#TaskFormatter)
:   Formatter for tasks, adding the task name and id.

    format(*record*)[[source]](../_modules/celery/app/log.html#TaskFormatter.format)
    :   Format the specified record as text.

        The record’s attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.