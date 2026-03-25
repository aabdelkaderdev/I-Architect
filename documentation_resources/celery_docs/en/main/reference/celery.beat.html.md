<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.beat.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.beat.html).

# `celery.beat`

The periodic task scheduler.

celery.beat.EmbeddedService(*app*, *max\_interval=None*, *\*\*kwargs*)[[source]](../_modules/celery/beat.html#EmbeddedService)
:   Return embedded clock service.

    Parameters:
    :   **thread** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Run threaded instead of as a separate process.
        Uses [`multiprocessing`](https://docs.python.org/dev/library/multiprocessing.html#module-multiprocessing "(in Python v3.15)") by default, if available.

class celery.beat.PersistentScheduler(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/beat.html#PersistentScheduler)
:   Scheduler backed by [`shelve`](https://docs.python.org/dev/library/shelve.html#module-shelve "(in Python v3.15)") database.

    close()[[source]](../_modules/celery/beat.html#PersistentScheduler.close)

    get\_schedule()[[source]](../_modules/celery/beat.html#PersistentScheduler.get_schedule)

    property info

    known\_suffixes = ('', '.db', '.dat', '.bak', '.dir')

    persistence = <module 'shelve' from '/home/docs/.asdf/installs/python/3.11.12/lib/python3.11/shelve.py'>

    property schedule

    set\_schedule(*schedule*)[[source]](../_modules/celery/beat.html#PersistentScheduler.set_schedule)

    setup\_schedule()[[source]](../_modules/celery/beat.html#PersistentScheduler.setup_schedule)

    sync()[[source]](../_modules/celery/beat.html#PersistentScheduler.sync)

class celery.beat.ScheduleEntry(*name=None*, *task=None*, *last\_run\_at=None*, *total\_run\_count=None*, *schedule=None*, *args=()*, *kwargs=None*, *options=None*, *relative=False*, *app=None*)[[source]](../_modules/celery/beat.html#ScheduleEntry)
:   An entry in the scheduler.

    Parameters:
    :   - **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – see [`name`](#celery.beat.ScheduleEntry.name "celery.beat.ScheduleEntry.name").
        - **schedule** ([*schedule*](celery.schedules.html#celery.schedules.schedule "celery.schedules.schedule")) – see [`schedule`](#celery.beat.ScheduleEntry.schedule "celery.beat.ScheduleEntry.schedule").
        - **args** (*Tuple*) – see [`args`](#celery.beat.ScheduleEntry.args "celery.beat.ScheduleEntry.args").
        - **kwargs** (*Dict*) – see [`kwargs`](#celery.beat.ScheduleEntry.kwargs "celery.beat.ScheduleEntry.kwargs").
        - **options** (*Dict*) – see [`options`](#celery.beat.ScheduleEntry.options "celery.beat.ScheduleEntry.options").
        - **last\_run\_at** ([*datetime*](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")) – see [`last_run_at`](#celery.beat.ScheduleEntry.last_run_at "celery.beat.ScheduleEntry.last_run_at").
        - **total\_run\_count** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – see [`total_run_count`](#celery.beat.ScheduleEntry.total_run_count "celery.beat.ScheduleEntry.total_run_count").
        - **relative** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Is the time relative to when the server starts?

    args = None
    :   Positional arguments to apply.

    default\_now()[[source]](../_modules/celery/beat.html#ScheduleEntry.default_now)

    editable\_fields\_equal(*other*)[[source]](../_modules/celery/beat.html#ScheduleEntry.editable_fields_equal)

    is\_due()[[source]](../_modules/celery/beat.html#ScheduleEntry.is_due)
    :   See [`is_due()`](celery.schedules.html#celery.schedules.schedule.is_due "celery.schedules.schedule.is_due").

    kwargs = None
    :   Keyword arguments to apply.

    last\_run\_at = None
    :   The time and date of when this task was last scheduled.

    name = None
    :   The task name

    next(*last\_run\_at=None*)
    :   Return new instance, with date and count fields updated.

    options = None
    :   Task execution options.

    schedule = None
    :   The schedule ([`schedule`](celery.schedules.html#celery.schedules.schedule "celery.schedules.schedule"))

    total\_run\_count = 0
    :   Total number of times this task has been scheduled.

    update(*other*)[[source]](../_modules/celery/beat.html#ScheduleEntry.update)
    :   Update values from another entry.

        Will only update “editable” fields:
        :   `task`, `schedule`, `args`, `kwargs`, `options`.

class celery.beat.Scheduler(*app*, *schedule=None*, *max\_interval=None*, *Producer=None*, *lazy=False*, *sync\_every\_tasks=None*, *\*\*kwargs*)[[source]](../_modules/celery/beat.html#Scheduler)
:   Scheduler for periodic tasks.

    The **celery beat** program may instantiate this class
    multiple times for introspection purposes, but then with the
    `lazy` argument set. It’s important for subclasses to
    be idempotent when this argument is set.

    Parameters:
    :   - **schedule** ([*schedule*](celery.schedules.html#celery.schedules.schedule "celery.schedules.schedule")) – see [`schedule`](#celery.beat.Scheduler.schedule "celery.beat.Scheduler.schedule").
        - **max\_interval** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – see [`max_interval`](#celery.beat.Scheduler.max_interval "celery.beat.Scheduler.max_interval").
        - **lazy** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Don’t set up the schedule.

    Entry
    :   alias of [`ScheduleEntry`](#celery.beat.ScheduleEntry "celery.beat.ScheduleEntry")

    add(*\*\*kwargs*)[[source]](../_modules/celery/beat.html#Scheduler.add)

    adjust(*n*, *drift=-0.01*)[[source]](../_modules/celery/beat.html#Scheduler.adjust)

    apply\_async(*entry*, *producer=None*, *advance=True*, *\*\*kwargs*)[[source]](../_modules/celery/beat.html#Scheduler.apply_async)

    apply\_entry(*entry*, *producer=None*)[[source]](../_modules/celery/beat.html#Scheduler.apply_entry)

    close()[[source]](../_modules/celery/beat.html#Scheduler.close)

    property connection

    get\_schedule()[[source]](../_modules/celery/beat.html#Scheduler.get_schedule)

    property info

    install\_default\_entries(*data*)[[source]](../_modules/celery/beat.html#Scheduler.install_default_entries)

    is\_due(*entry*)[[source]](../_modules/celery/beat.html#Scheduler.is_due)

    logger = <Logger celery.beat (WARNING)>

    max\_interval = 300
    :   Maximum time to sleep between re-checking the schedule.

    merge\_inplace(*b*)[[source]](../_modules/celery/beat.html#Scheduler.merge_inplace)

    populate\_heap(*event\_t=<class 'celery.beat.event\_t'>*, *heapify=<built-in function heapify>*)[[source]](../_modules/celery/beat.html#Scheduler.populate_heap)
    :   Populate the heap with the data contained in the schedule.

    property producer

    reserve(*entry*)[[source]](../_modules/celery/beat.html#Scheduler.reserve)

    property schedule
    :   The schedule dict/shelve.

    schedules\_equal(*old\_schedules*, *new\_schedules*)[[source]](../_modules/celery/beat.html#Scheduler.schedules_equal)

    send\_task(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/beat.html#Scheduler.send_task)

    set\_schedule(*schedule*)[[source]](../_modules/celery/beat.html#Scheduler.set_schedule)

    setup\_schedule()[[source]](../_modules/celery/beat.html#Scheduler.setup_schedule)

    should\_sync()[[source]](../_modules/celery/beat.html#Scheduler.should_sync)

    sync()[[source]](../_modules/celery/beat.html#Scheduler.sync)

    sync\_every = 180
    :   How often to sync the schedule (3 minutes by default)

    sync\_every\_tasks = None
    :   How many tasks can be called before a sync is forced.

    tick(*event\_t=<class 'celery.beat.event\_t'>*, *min=<built-in function min>*, *heappop=<built-in function heappop>*, *heappush=<built-in function heappush>*)[[source]](../_modules/celery/beat.html#Scheduler.tick)
    :   Run a tick - one iteration of the scheduler.

        Executes one due task per call.

        Returns:
        :   preferred delay in seconds for next call.

        Return type:
        :   [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")

    update\_from\_dict(*dict\_*)[[source]](../_modules/celery/beat.html#Scheduler.update_from_dict)

exception celery.beat.SchedulingError[[source]](../_modules/celery/beat.html#SchedulingError)
:   An error occurred while scheduling a task.

class celery.beat.Service(*app*, *max\_interval=None*, *schedule\_filename=None*, *scheduler\_cls=None*)[[source]](../_modules/celery/beat.html#Service)
:   Celery periodic task service.

    get\_scheduler(*lazy=False*, *extension\_namespace='celery.beat\_schedulers'*)[[source]](../_modules/celery/beat.html#Service.get_scheduler)

    property scheduler

    scheduler\_cls
    :   alias of [`PersistentScheduler`](#celery.beat.PersistentScheduler "celery.beat.PersistentScheduler")

    start(*embedded\_process=False*)[[source]](../_modules/celery/beat.html#Service.start)

    stop(*wait=False*)[[source]](../_modules/celery/beat.html#Service.stop)

    sync()[[source]](../_modules/celery/beat.html#Service.sync)