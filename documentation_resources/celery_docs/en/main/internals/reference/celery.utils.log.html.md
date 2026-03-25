<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.log.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.log.html).

# `celery.utils.log`

Logging utilities.

class celery.utils.log.ColorFormatter(*fmt=None*, *use\_color=True*)[[source]](../../_modules/celery/utils/log.html#ColorFormatter)
:   Logging formatter that adds colors based on severity.

    COLORS = {'black': <bound method colored.black of ''>, 'blue': <bound method colored.blue of ''>, 'cyan': <bound method colored.cyan of ''>, 'green': <bound method colored.green of ''>, 'magenta': <bound method colored.magenta of ''>, 'red': <bound method colored.red of ''>, 'white': <bound method colored.white of ''>, 'yellow': <bound method colored.yellow of ''>}
    :   Loglevel -> Color mapping.

    colors = {'CRITICAL': <bound method colored.magenta of ''>, 'DEBUG': <bound method colored.blue of ''>, 'ERROR': <bound method colored.red of ''>, 'WARNING': <bound method colored.yellow of ''>}

    format(*record*)[[source]](../../_modules/celery/utils/log.html#ColorFormatter.format)
    :   Format the specified record as text.

        The record’s attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.

    formatException(*ei*)[[source]](../../_modules/celery/utils/log.html#ColorFormatter.formatException)
    :   Format and return the specified exception information as a string.

        This default implementation just uses
        traceback.print\_exception()

class celery.utils.log.LoggingProxy(*logger*, *loglevel=None*)[[source]](../../_modules/celery/utils/log.html#LoggingProxy)
:   Forward file object to [`logging.Logger`](https://docs.python.org/dev/library/logging.html#logging.Logger "(in Python v3.15)") instance.

    Parameters:
    :   - **logger** ([*Logger*](https://docs.python.org/dev/library/logging.html#logging.Logger "(in Python v3.15)")) – Logger instance to forward to.
        - **loglevel** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Log level to use when logging messages.

    close()[[source]](../../_modules/celery/utils/log.html#LoggingProxy.close)

    closed = False

    flush()[[source]](../../_modules/celery/utils/log.html#LoggingProxy.flush)

    isatty()[[source]](../../_modules/celery/utils/log.html#LoggingProxy.isatty)
    :   Here for file support.

    loglevel = 40

    mode = 'w'

    name = None

    write(*data: AnyStr*) → [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")[[source]](../../_modules/celery/utils/log.html#LoggingProxy.write)
    :   Write message to logging object.

    writelines(*sequence: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")]*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/log.html#LoggingProxy.writelines)
    :   Write list of strings to file.

        The sequence can be any iterable object producing strings.
        This is equivalent to calling [`write()`](#celery.utils.log.LoggingProxy.write "celery.utils.log.LoggingProxy.write") for each string.

celery.utils.log.get\_logger(*name*)[[source]](../../_modules/celery/utils/log.html#get_logger)
:   Get logger by name.

celery.utils.log.get\_multiprocessing\_logger()[[source]](../../_modules/celery/utils/log.html#get_multiprocessing_logger)
:   Return the multiprocessing logger.

celery.utils.log.get\_task\_logger(*name*)[[source]](../../_modules/celery/utils/log.html#get_task_logger)
:   Get logger for task module by name.

celery.utils.log.in\_sighandler()[[source]](../../_modules/celery/utils/log.html#in_sighandler)
:   Context that records that we are in a signal handler.

celery.utils.log.mlevel(*level*)[[source]](../../_modules/celery/utils/log.html#mlevel)
:   Convert level name/int to log level.

celery.utils.log.reset\_multiprocessing\_logger()[[source]](../../_modules/celery/utils/log.html#reset_multiprocessing_logger)
:   Reset multiprocessing logging setup.

celery.utils.log.set\_in\_sighandler(*value*)[[source]](../../_modules/celery/utils/log.html#set_in_sighandler)
:   Set flag signifying that we’re inside a signal handler.