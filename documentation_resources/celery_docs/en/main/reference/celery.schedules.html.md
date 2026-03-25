<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.schedules.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.schedules.html).

# `celery.schedules`

Schedules define the intervals at which periodic tasks run.

exception celery.schedules.ParseException[[source]](../_modules/celery/schedules.html#ParseException)
:   Raised by [`crontab_parser`](#celery.schedules.crontab_parser "celery.schedules.crontab_parser") when the input can’t be parsed.

class celery.schedules.crontab(*minute: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")[[int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")] = '\*'*, *hour: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")[[int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")] = '\*'*, *day\_of\_week: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")[[int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")] = '\*'*, *day\_of\_month: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")[[int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")] = '\*'*, *month\_of\_year: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")[[int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")] = '\*'*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../_modules/celery/schedules.html#crontab)
:   Crontab schedule.

    A Crontab can be used as the `run_every` value of a
    periodic task entry to add *crontab(5)*-like scheduling.

    Like a *cron(5)*-job, you can specify units of time of when
    you’d like the task to execute. It’s a reasonably complete
    implementation of **cron**’s features, so it should provide a fair
    degree of scheduling needs.

    You can specify a minute, an hour, a day of the week, a day of the
    month, and/or a month in the year in any of the following formats:

    minute
    :   - A (list of) integers from 0-59 that represent the minutes of
          an hour of when execution should occur; or
        - A string representing a Crontab pattern. This may get pretty
          advanced, like `minute='*/15'` (for every quarter) or
          `minute='1,13,30-45,50-59/2'`.

    hour
    :   - A (list of) integers from 0-23 that represent the hours of
          a day of when execution should occur; or
        - A string representing a Crontab pattern. This may get pretty
          advanced, like `hour='*/3'` (for every three hours) or
          `hour='0,8-17/2'` (at midnight, and every two hours during
          office hours).

    day\_of\_week
    :   - A (list of) integers from 0-6, where Sunday = 0 and Saturday =
          6, that represent the days of a week that execution should
          occur.
        - A string representing a Crontab pattern. This may get pretty
          advanced, like `day_of_week='mon-fri'` (for weekdays only).
          (Beware that `day_of_week='*/2'` does not literally mean
          ‘every two days’, but ‘every day that is divisible by two’!)

    day\_of\_month
    :   - A (list of) integers from 1-31 that represents the days of the
          month that execution should occur.
        - A string representing a Crontab pattern. This may get pretty
          advanced, such as `day_of_month='2-30/2'` (for every even
          numbered day) or `day_of_month='1-7,15-21'` (for the first and
          third weeks of the month).

    month\_of\_year
    :   - A (list of) integers from 1-12 that represents the months of
          the year during which execution can occur.
        - A string representing a Crontab pattern. This may get pretty
          advanced, such as `month_of_year='*/3'` (for the first month
          of every quarter) or `month_of_year='2-12/2'` (for every even
          numbered month).

    nowfun
    :   Function returning the current date and time
        ([`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")).

    app
    :   The Celery app instance.

    It’s important to realize that any day on which execution should
    occur must be represented by entries in all three of the day and
    month attributes. For example, if `day_of_week` is 0 and
    `day_of_month` is every seventh day, only months that begin
    on Sunday and are also in the `month_of_year` attribute will have
    execution events. Or, `day_of_week` is 1 and `day_of_month`
    is ‘1-7,15-21’ means every first and third Monday of every month
    present in `month_of_year`.

    classmethod from\_string(*crontab: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [crontab](#celery.schedules.crontab "celery.schedules.crontab")[[source]](../_modules/celery/schedules.html#crontab.from_string)
    :   Create a Crontab from a cron expression string. For example `crontab.from_string('* * * * *')`.

        ```
        ┌───────────── minute (0–59)
        │ ┌───────────── hour (0–23)
        │ │ ┌───────────── day of the month (1–31)
        │ │ │ ┌───────────── month (1–12)
        │ │ │ │ ┌───────────── day of the week (0–6) (Sunday to Saturday)
        * * * * *
        ```

    is\_due(*last\_run\_at: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*) → [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)"), [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")][[source]](../_modules/celery/schedules.html#crontab.is_due)
    :   Return tuple of `(is_due, next_time_to_run)`.

        If [`beat_cron_starting_deadline`](../userguide/configuration.html#std-setting-beat_cron_starting_deadline) has been specified, the
        scheduler will make sure that the last\_run\_at time is within the
        deadline. This prevents tasks that could have been run according to
        the crontab, but didn’t, from running again unexpectedly.

        Note

        Next time to run is in seconds.

        SeeAlso:
        :   [`celery.schedules.schedule.is_due()`](#celery.schedules.schedule.is_due "celery.schedules.schedule.is_due") for more information.

    remaining\_delta(*last\_run\_at: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*, *tz: [tzinfo](https://docs.python.org/dev/library/datetime.html#datetime.tzinfo "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *ffwd: [type](../internals/reference/celery.backends.rpc.html#id5 "celery.backends.rpc.RPCBackend.Exchange.type") = <class 'celery.utils.time.ffwd'>*) → [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)"), [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)"), [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")][[source]](../_modules/celery/schedules.html#crontab.remaining_delta)

    remaining\_estimate(*last\_run\_at: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*, *ffwd: [type](../internals/reference/celery.backends.rpc.html#id5 "celery.backends.rpc.RPCBackend.Exchange.type") = <class 'celery.utils.time.ffwd'>*) → [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")[[source]](../_modules/celery/schedules.html#crontab.remaining_estimate)
    :   Estimate of next run time.

        Returns when the periodic task should run next as a
        [`timedelta`](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)").

class celery.schedules.crontab\_parser(*max\_: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 60*, *min\_: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 0*)[[source]](../_modules/celery/schedules.html#crontab_parser)
:   Parser for Crontab expressions.

    Any expression of the form ‘groups’
    (see BNF grammar below) is accepted and expanded to a set of numbers.
    These numbers represent the units of time that the Crontab needs to
    run on:

    ```
    digit   :: '0'..'9'
    dow     :: 'a'..'z'
    number  :: digit+ | dow+
    steps   :: number
    range   :: number ( '-' number ) ?
    numspec :: '*' | range
    expr    :: numspec ( '/' steps ) ?
    groups  :: expr ( ',' expr ) *
    ```

    The parser is a general purpose one, useful for parsing hours, minutes and
    day of week expressions. Example usage:

    ```
    >>> minutes = crontab_parser(60).parse('*/15')
    [0, 15, 30, 45]
    >>> hours = crontab_parser(24).parse('*/4')
    [0, 4, 8, 12, 16, 20]
    >>> day_of_week = crontab_parser(7).parse('*')
    [0, 1, 2, 3, 4, 5, 6]
    ```

    It can also parse day of month and month of year expressions if initialized
    with a minimum of 1. Example usage:

    ```
    >>> days_of_month = crontab_parser(31, 1).parse('*/3')
    [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31]
    >>> months_of_year = crontab_parser(12, 1).parse('*/2')
    [1, 3, 5, 7, 9, 11]
    >>> months_of_year = crontab_parser(12, 1).parse('2-12/2')
    [2, 4, 6, 8, 10, 12]
    ```

    The maximum possible expanded value returned is found by the formula:

    exception ParseException
    :   Raised by [`crontab_parser`](#celery.schedules.crontab_parser "celery.schedules.crontab_parser") when the input can’t be parsed.

    parse(*spec: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [set](https://docs.python.org/dev/library/stdtypes.html#set "(in Python v3.15)")[[int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")][[source]](../_modules/celery/schedules.html#crontab_parser.parse)

celery.schedules.maybe\_schedule(*s: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") | [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)") | BaseSchedule*, *relative: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*, *app: [Celery](celery.html#celery.Celery "celery.app.base.Celery") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") | [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)") | BaseSchedule[[source]](../_modules/celery/schedules.html#maybe_schedule)
:   Return schedule from number, timedelta, or actual schedule.

class celery.schedules.schedule(*run\_every: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") | [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *relative: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*, *nowfun: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *app: [Celery](celery.html#celery.Celery "celery.app.base.Celery") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*)[[source]](../_modules/celery/schedules.html#schedule)
:   Schedule for periodic task.

    Parameters:
    :   - **run\_every** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")*,* [*timedelta*](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")) – Time interval.
        - **relative** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If set to True the run time will be rounded to the
          resolution of the interval.
        - **nowfun** (*Callable*) – Function returning the current date and time
          ([`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")).
        - **app** ([*Celery*](celery.html#celery.Celery "celery.Celery")) – Celery app instance.

    property human\_seconds: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

    is\_due(*last\_run\_at: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*) → [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)"), [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")][[source]](../_modules/celery/schedules.html#schedule.is_due)
    :   Return tuple of `(is_due, next_time_to_check)`.

        Notes

        - next time to check is in seconds.
        - `(True, 20)`, means the task should be run now, and the next
          :   time to check is in 20 seconds.
        - `(False, 12.3)`, means the task is not due, but that the
          scheduler should check again in 12.3 seconds.

        The next time to check is used to save energy/CPU cycles,
        it does not need to be accurate but will influence the precision
        of your schedule. You must also keep in mind
        the value of [`beat_max_loop_interval`](../userguide/configuration.html#std-setting-beat_max_loop_interval),
        that decides the maximum number of seconds the scheduler can
        sleep between re-checking the periodic task intervals. So if you
        have a task that changes schedule at run-time then your next\_run\_at
        check will decide how long it will take before a change to the
        schedule takes effect. The max loop interval takes precedence
        over the next check at value returned.

        Scheduler max interval variance

        The default max loop interval may vary for different schedulers.
        For the default scheduler the value is 5 minutes, but for example
        the <https://pypi.org/project/django-celery-beat/> database scheduler the value
        is 5 seconds.

    relative: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False

    remaining\_estimate(*last\_run\_at: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*) → [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")[[source]](../_modules/celery/schedules.html#schedule.remaining_estimate)

    property seconds: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")

class celery.schedules.solar(*event: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *lat: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")*, *lon: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../_modules/celery/schedules.html#solar)
:   Solar event.

    A solar event can be used as the `run_every` value of a
    periodic task entry to schedule based on certain solar events.

    Notes

    Available event values are:

    > - `dawn_astronomical`
    > - `dawn_nautical`
    > - `dawn_civil`
    > - `sunrise`
    > - `solar_noon`
    > - `sunset`
    > - `dusk_civil`
    > - `dusk_nautical`
    > - `dusk_astronomical`

    Parameters:
    :   - **event** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Solar event that triggers this task.
          See note for available values.
        - **lat** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – The latitude of the observer.
        - **lon** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – The longitude of the observer.
        - **nowfun** (*Callable*) – Function returning the current date and time
          as a class:~datetime.datetime.
        - **app** ([*Celery*](celery.html#celery.Celery "celery.Celery")) – Celery app instance.

    is\_due(*last\_run\_at: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*) → [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)"), [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")][[source]](../_modules/celery/schedules.html#solar.is_due)
    :   Return tuple of `(is_due, next_time_to_run)`.

        Note

        next time to run is in seconds.

        See also

        [`celery.schedules.schedule.is_due()`](#celery.schedules.schedule.is_due "celery.schedules.schedule.is_due") for more information.

    remaining\_estimate(*last\_run\_at: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*) → [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")[[source]](../_modules/celery/schedules.html#solar.remaining_estimate)
    :   Return estimate of next time to run.

        Returns:
        :   when the periodic task should
            :   run next, or if it shouldn’t run today (e.g., the sun does
                not rise today), returns the time when the next check
                should take place.

        Return type:
        :   [*timedelta*](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")