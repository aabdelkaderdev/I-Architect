<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.contrib.rdb.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.rdb.html).

# `celery.contrib.rdb`

Remote Debugger.

## Introduction

This is a remote debugger for Celery tasks running in multiprocessing
pool workers. Inspired by a lost post on dzone.com.

### Usage

```
from celery.contrib import rdb
from celery import task

@task()
def add(x, y):
    result = x + y
    rdb.set_trace()
    return result
```

## Environment Variables

CELERY\_RDB\_HOST

### `CELERY_RDB_HOST`

> Hostname to bind to. Default is ‘127.0.0.1’ (only accessible from
> localhost).

CELERY\_RDB\_PORT

### `CELERY_RDB_PORT`

> Base port to bind to. Default is 6899.
> The debugger will try to find an available port starting from the
> base port. The selected port will be logged by the worker.

celery.contrib.rdb.set\_trace(*frame=None*)[[source]](../_modules/celery/contrib/rdb.html#set_trace)
:   Set break-point at current location, or a specified frame.

celery.contrib.rdb.debugger()[[source]](../_modules/celery/contrib/rdb.html#debugger)
:   Return the current debugger instance, or create if none.

class celery.contrib.rdb.Rdb(*host='127.0.0.1'*, *port=6899*, *port\_search\_limit=100*, *port\_skew=0*, *out=<\_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>*)[[source]](../_modules/celery/contrib/rdb.html#Rdb)
:   Remote debugger.