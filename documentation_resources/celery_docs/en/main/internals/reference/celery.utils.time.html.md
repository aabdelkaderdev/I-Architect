<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.time.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.time.html).

# `celery.utils.time`

Utilities related to dates, times, intervals, and timezones.

class celery.utils.time.LocalTimezone[[source]](../../_modules/celery/utils/time.html#LocalTimezone)
:   Local time implementation. Provided in \_Zone to the app when enable\_utc is disabled.
    Otherwise, \_Zone provides a UTC ZoneInfo instance as the timezone implementation for the application.

    Note

    Used only when the [`enable_utc`](../../userguide/configuration.html#std-setting-enable_utc) setting is disabled.

    dst(*dt: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*) → [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#LocalTimezone.dst)
    :   datetime -> DST offset as timedelta positive east of UTC.

    fromutc(*dt: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*) → [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#LocalTimezone.fromutc)
    :   datetime in UTC -> datetime in local time.

    tzname(*dt: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#LocalTimezone.tzname)
    :   datetime -> string name of time zone.

    utcoffset(*dt: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*) → [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#LocalTimezone.utcoffset)
    :   datetime -> timedelta showing offset from UTC, negative values indicating West of UTC

celery.utils.time.adjust\_timestamp(*ts: float, offset: int, here: ~typing.Callable[[...], float] = <function utcoffset>*) → [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#adjust_timestamp)
:   Adjust timestamp based on provided utcoffset.

celery.utils.time.delta\_resolution(*dt: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*, *delta: [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")*) → [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#delta_resolution)
:   Round a [`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)") to the resolution of timedelta.

    If the [`timedelta`](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)") is in days, the
    [`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)") will be rounded to the nearest days,
    if the [`timedelta`](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)") is in hours the
    [`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)") will be rounded to the nearest hour,
    and so on until seconds, which will just return the original
    [`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)").

class celery.utils.time.ffwd(*year=None*, *month=None*, *weeks=0*, *weekday=None*, *day=None*, *hour=None*, *minute=None*, *second=None*, *microsecond=None*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../../_modules/celery/utils/time.html#ffwd)
:   Version of `dateutil.relativedelta` that only supports addition.

celery.utils.time.get\_exponential\_backoff\_interval(*factor: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*, *retries: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*, *maximum: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*, *full\_jitter: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*) → [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#get_exponential_backoff_interval)
:   Calculate the exponential backoff wait time.

celery.utils.time.humanize\_seconds(*secs: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*, *prefix: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*, *sep: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*, *now: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'now'*, *microseconds: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#humanize_seconds)
:   Show seconds in human form.

    For example, 60 becomes “1 minute”, and 7200 becomes “2 hours”.

    Parameters:
    :   - **prefix** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – can be used to add a preposition to the output
          (e.g., ‘in’ will give ‘in 1 second’, but add nothing to ‘now’).
        - **now** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Literal ‘now’.
        - **microseconds** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Include microseconds.

celery.utils.time.is\_naive(*dt: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*) → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#is_naive)
:   Return True if [`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)") is naive, meaning it doesn’t have timezone info set.

celery.utils.time.localize(*dt: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*, *tz: [tzinfo](https://docs.python.org/dev/library/datetime.html#datetime.tzinfo "(in Python v3.15)")*) → [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#localize)
:   Convert aware [`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)") to another timezone.

    Using a ZoneInfo timezone will give the most flexibility in terms of ambiguous DST handling.

celery.utils.time.make\_aware(*dt: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*, *tz: [tzinfo](https://docs.python.org/dev/library/datetime.html#datetime.tzinfo "(in Python v3.15)")*) → [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#make_aware)
:   Set timezone for a [`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)") object.

celery.utils.time.maybe\_iso8601(*dt: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)") | [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") | [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#maybe_iso8601)
:   Either `datetime | str -> datetime` or `None -> None`.

celery.utils.time.maybe\_make\_aware(*dt: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*, *tz: [tzinfo](https://docs.python.org/dev/library/datetime.html#datetime.tzinfo "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *naive\_as\_utc: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*) → [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#maybe_make_aware)
:   Convert dt to aware datetime, do nothing if dt is already aware.

celery.utils.time.maybe\_timedelta(*delta: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*) → [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#maybe_timedelta)
:   Convert integer to timedelta, if argument is an integer.

celery.utils.time.rate(*r: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#rate)
:   Convert rate string (“100/m”, “2/h” or “0.5/s”) to seconds.

celery.utils.time.remaining(*start: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*, *ends\_in: [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")*, *now: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *relative: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*) → [timedelta](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#remaining)
:   Calculate the real remaining time for a start date and a timedelta.

    For example, “how many seconds left for 30 seconds after start?”

    Parameters:
    :   - **start** ([*datetime*](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")) – Starting date.
        - **ends\_in** ([*timedelta*](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")) – The end delta.
        - **relative** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If enabled the end time will be calculated
          using [`delta_resolution()`](#celery.utils.time.delta_resolution "celery.utils.time.delta_resolution") (i.e., rounded to the
          resolution of ends\_in).
        - **now** ([*datetime*](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")) – Current time and date.
          Defaults to `datetime.now(timezone.utc)()`.

    Returns:
    :   Remaining time.

    Return type:
    :   [*timedelta*](https://docs.python.org/dev/library/datetime.html#datetime.timedelta "(in Python v3.15)")

celery.utils.time.to\_utc(*dt: [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")*) → [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#to_utc)
:   Convert naive [`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)") to UTC.

celery.utils.time.utcoffset(*time: ~types.ModuleType = <module 'time' (built-in)>, localtime: ~typing.Callable[[...], ~time.struct\_time] = <built-in function localtime>*) → [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#utcoffset)
:   Return the current offset to UTC in hours.

celery.utils.time.weekday(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")[[source]](../../_modules/celery/utils/time.html#weekday)
:   Return the position of a weekday: 0 - 7, where 0 is Sunday.

    Example

    ```
    >>> weekday('sunday'), weekday('sun'), weekday('mon')
    (0, 0, 1)
    ```