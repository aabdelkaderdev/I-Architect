<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.worker.strategy.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.strategy.html).

# `celery.worker.strategy`

Task execution strategy (optimization).

celery.worker.strategy.default(*task*, *app*, *consumer*, *info=<bound method Logger.info of <Logger celery.worker.strategy (WARNING)>>*, *error=<bound method Logger.error of <Logger celery.worker.strategy (WARNING)>>*, *task\_reserved=<function task\_reserved>*, *to\_system\_tz=<bound method \_Zone.to\_system of <celery.utils.time.\_Zone object>>*, *bytes=<class 'bytes'>*, *proto1\_to\_proto2=<function proto1\_to\_proto2>*)[[source]](../_modules/celery/worker/strategy.html#default)
:   Default task execution strategy.

    Note

    Strategies are here as an optimization, so sadly
    it’s not very easy to override.