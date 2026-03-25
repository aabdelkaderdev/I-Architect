<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.loaders.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.loaders.html).

# `celery.loaders`

Get loader by name.

Loaders define how configuration is read, what happens
when workers start, when tasks are executed and so on.

celery.loaders.get\_loader\_cls(*loader*)[[source]](../_modules/celery/loaders.html#get_loader_cls)
:   Get loader class by name/alias.