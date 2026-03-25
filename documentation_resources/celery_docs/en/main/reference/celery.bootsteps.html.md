<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.bootsteps.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.bootsteps.html).

# `celery.bootsteps`

A directed acyclic graph of reusable components.

class celery.bootsteps.Blueprint(*steps=None*, *name=None*, *on\_start=None*, *on\_close=None*, *on\_stopped=None*)[[source]](../_modules/celery/bootsteps.html#Blueprint)
:   Blueprint containing bootsteps that can be applied to objects.

    Parameters:
    :   - **Sequence****[****Union****[****str** ([*steps*](celery.html#celery.Celery.steps "celery.Celery.steps")) – List of steps.
        - **Step****]****]** – List of steps.
        - **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Set explicit name for this blueprint.
        - **on\_start** (*Callable*) – Optional callback applied after blueprint start.
        - **on\_close** (*Callable*) – Optional callback applied before blueprint close.
        - **on\_stopped** (*Callable*) – Optional callback applied after
          blueprint stopped.

    GraphFormatter
    :   alias of `StepFormatter`

    property alias

    apply(*parent*, *\*\*kwargs*)[[source]](../_modules/celery/bootsteps.html#Blueprint.apply)
    :   Apply the steps in this blueprint to an object.

        This will apply the `__init__` and `include` methods
        of each step, with the object as argument:

        ```
        step = Step(obj)
        ...
        step.include(obj)
        ```

        For [`StartStopStep`](#celery.bootsteps.StartStopStep "celery.bootsteps.StartStopStep") the services created
        will also be added to the objects `steps` attribute.

    claim\_steps()[[source]](../_modules/celery/bootsteps.html#Blueprint.claim_steps)

    close(*parent*)[[source]](../_modules/celery/bootsteps.html#Blueprint.close)

    connect\_with(*other*)[[source]](../_modules/celery/bootsteps.html#Blueprint.connect_with)

    default\_steps = {}

    human\_state()[[source]](../_modules/celery/bootsteps.html#Blueprint.human_state)

    info(*parent*)[[source]](../_modules/celery/bootsteps.html#Blueprint.info)

    join(*timeout=None*)[[source]](../_modules/celery/bootsteps.html#Blueprint.join)

    load\_step(*step*)[[source]](../_modules/celery/bootsteps.html#Blueprint.load_step)

    name = None

    restart(*parent*, *method='stop'*, *description='restarting'*, *propagate=False*)[[source]](../_modules/celery/bootsteps.html#Blueprint.restart)

    send\_all(*parent*, *method*, *description=None*, *reverse=True*, *propagate=True*, *args=()*)[[source]](../_modules/celery/bootsteps.html#Blueprint.send_all)

    start(*parent*)[[source]](../_modules/celery/bootsteps.html#Blueprint.start)

    started = 0

    state = None

    state\_to\_name = {0: 'initializing', 1: 'running', 2: 'closing', 3: 'terminating'}

    stop(*parent*, *close=True*, *terminate=False*)[[source]](../_modules/celery/bootsteps.html#Blueprint.stop)

class celery.bootsteps.ConsumerStep(*parent*, *\*\*kwargs*)[[source]](../_modules/celery/bootsteps.html#ConsumerStep)
:   Bootstep that starts a message consumer.

    consumers = None

    get\_consumers(*channel*)[[source]](../_modules/celery/bootsteps.html#ConsumerStep.get_consumers)

    name = 'celery.bootsteps.ConsumerStep'

    requires = ('celery.worker.consumer:Connection',)

    shutdown(*c*)[[source]](../_modules/celery/bootsteps.html#ConsumerStep.shutdown)

    start(*c*)[[source]](../_modules/celery/bootsteps.html#ConsumerStep.start)

    stop(*c*)[[source]](../_modules/celery/bootsteps.html#ConsumerStep.stop)

class celery.bootsteps.StartStopStep(*parent*, *\*\*kwargs*)[[source]](../_modules/celery/bootsteps.html#StartStopStep)
:   Bootstep that must be started and stopped in order.

    close(*parent*)[[source]](../_modules/celery/bootsteps.html#StartStopStep.close)

    include(*parent*)[[source]](../_modules/celery/bootsteps.html#StartStopStep.include)

    name = 'celery.bootsteps.StartStopStep'

    obj = None

    start(*parent*)[[source]](../_modules/celery/bootsteps.html#StartStopStep.start)

    stop(*parent*)[[source]](../_modules/celery/bootsteps.html#StartStopStep.stop)

    terminate(*parent*)[[source]](../_modules/celery/bootsteps.html#StartStopStep.terminate)

class celery.bootsteps.Step(*parent*, *\*\*kwargs*)[[source]](../_modules/celery/bootsteps.html#Step)
:   A Bootstep.

    The `__init__()` method is called when the step
    is bound to a parent object, and can as such be used
    to initialize attributes in the parent object at
    parent instantiation-time.

    property alias

    conditional = False

    create(*parent*)[[source]](../_modules/celery/bootsteps.html#Step.create)
    :   Create the step.

    enabled = True

    include(*parent*)[[source]](../_modules/celery/bootsteps.html#Step.include)

    include\_if(*parent*)[[source]](../_modules/celery/bootsteps.html#Step.include_if)
    :   Return true if bootstep should be included.

        You can define this as an optional predicate that decides whether
        this step should be created.

    info(*obj*)[[source]](../_modules/celery/bootsteps.html#Step.info)

    instantiate(*name*, *\*args*, *\*\*kwargs*)[[source]](../_modules/celery/bootsteps.html#Step.instantiate)

    label = None

    last = False

    name = 'celery.bootsteps.Step'

    requires = ()