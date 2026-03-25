<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.contrib.testing.manager.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.testing.manager.html).

# `celery.contrib.testing.manager`

## 

Integration testing utilities.

class celery.contrib.testing.manager.Manager(*app*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/manager.html#Manager)
:   Test helpers for task integration tests.

class celery.contrib.testing.manager.ManagerMixin[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin)
:   Mixin that adds [`Manager`](#celery.contrib.testing.manager.Manager "celery.contrib.testing.manager.Manager") capabilities.

    assert\_accepted(*ids*, *interval=0.5*, *desc='waiting for tasks to be accepted'*, *\*\*policy*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.assert_accepted)

    assert\_received(*ids*, *interval=0.5*, *desc='waiting for tasks to be received'*, *\*\*policy*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.assert_received)

    assert\_result\_tasks\_in\_progress\_or\_completed(*async\_results*, *interval=0.5*, *desc='waiting for tasks to be started or completed'*, *\*\*policy*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.assert_result_tasks_in_progress_or_completed)

    assert\_task\_state\_from\_result(*fun*, *results*, *interval=0.5*, *\*\*policy*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.assert_task_state_from_result)

    assert\_task\_worker\_state(*fun*, *ids*, *interval=0.5*, *\*\*policy*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.assert_task_worker_state)

    ensure\_not\_for\_a\_while(*fun*, *catch*, *desc='thing'*, *max\_retries=20*, *interval\_start=0.1*, *interval\_step=0.02*, *interval\_max=1.0*, *emit\_warning=False*, *\*\*options*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.ensure_not_for_a_while)
    :   Make sure something does not happen (at least for a while).

    inspect(*timeout=3.0*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.inspect)

    is\_accepted(*ids*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.is_accepted)

    is\_received(*ids*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.is_received)

    static is\_result\_task\_in\_progress(*results*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.is_result_task_in_progress)

    join(*r*, *propagate=False*, *max\_retries=10*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.join)

    missing\_results(*r: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[AsyncResult](celery.result.html#celery.result.AsyncResult "celery.result.AsyncResult")]*) → [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")][[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.missing_results)

    query\_task\_states(*ids*, *timeout=0.5*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.query_task_states)

    query\_tasks(*ids*, *timeout=0.5*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.query_tasks)

    remark(*s: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *sep: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = '-'*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.remark)

    retry\_over\_time(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.retry_over_time)

    true\_or\_raise(*fun*, *\*args*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.true_or_raise)

    wait\_for(*fun: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")*, *catch: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")]*, *desc: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'thing'*, *args: [Tuple](https://docs.python.org/dev/library/typing.html#typing.Tuple "(in Python v3.15)") = ()*, *kwargs: [Dict](https://docs.python.org/dev/library/typing.html#typing.Dict "(in Python v3.15)") = None*, *errback: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)") = None*, *max\_retries: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 10*, *interval\_start: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") = 0.1*, *interval\_step: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") = 0.5*, *interval\_max: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") = 5.0*, *emit\_warning: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*, *\*\*options: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.wait_for)
    :   Wait for event to happen.

        The catch argument specifies the exception that means the event
        has not happened yet.

    wait\_until\_idle()[[source]](../_modules/celery/contrib/testing/manager.html#ManagerMixin.wait_until_idle)

exception celery.contrib.testing.manager.Sentinel[[source]](../_modules/celery/contrib/testing/manager.html#Sentinel)
:   Signifies the end of something.