<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.html).

# `celery.concurrency`

Pool implementation abstract factory, and alias definitions.

celery.concurrency.get\_available\_pool\_names()[[source]](../../_modules/celery/concurrency.html#get_available_pool_names)
:   Return all available pool type names.

celery.concurrency.get\_implementation(*cls*)[[source]](../../_modules/celery/concurrency.html#get_implementation)
:   Return pool implementation by name.