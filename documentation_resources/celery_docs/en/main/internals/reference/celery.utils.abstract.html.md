<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.abstract.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.abstract.html).

# `celery.utils.abstract`

Abstract classes.

class celery.utils.abstract.CallableSignature[[source]](../../_modules/celery/utils/abstract.html#CallableSignature)
:   Celery Signature interface.

    abstract property app

    abstract property args

    abstract property chord\_size

    abstractmethod clone(*args=None*, *kwargs=None*)[[source]](../../_modules/celery/utils/abstract.html#CallableSignature.clone)

    abstractmethod freeze(*id=None*, *group\_id=None*, *chord=None*, *root\_id=None*, *group\_index=None*)[[source]](../../_modules/celery/utils/abstract.html#CallableSignature.freeze)

    abstract property id

    abstract property immutable

    abstract property kwargs

    abstractmethod link(*callback*)[[source]](../../_modules/celery/utils/abstract.html#CallableSignature.link)

    abstractmethod link\_error(*errback*)[[source]](../../_modules/celery/utils/abstract.html#CallableSignature.link_error)

    abstract property name

    abstract property options

    abstractmethod set(*immutable=None*, *\*\*options*)[[source]](../../_modules/celery/utils/abstract.html#CallableSignature.set)

    abstract property subtask\_type

    abstract property task

    abstract property type

class celery.utils.abstract.CallableTask[[source]](../../_modules/celery/utils/abstract.html#CallableTask)
:   Task interface.

    abstractmethod apply(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/abstract.html#CallableTask.apply)

    abstractmethod apply\_async(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/abstract.html#CallableTask.apply_async)

    abstractmethod delay(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/abstract.html#CallableTask.delay)