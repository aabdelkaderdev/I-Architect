<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.app.routes.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.app.routes.html).

# `celery.app.routes`

Task Routing.

Contains utilities for working with task routers, ([`task_routes`](../../userguide/configuration.html#std-setting-task_routes)).

class celery.app.routes.MapRoute(*map*)[[source]](../../_modules/celery/app/routes.html#MapRoute)
:   Creates a router out of a [`dict`](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)").

class celery.app.routes.Router(*routes=None*, *queues=None*, *create\_missing=False*, *app=None*)[[source]](../../_modules/celery/app/routes.html#Router)
:   Route tasks based on the [`task_routes`](../../userguide/configuration.html#std-setting-task_routes) setting.

    expand\_destination(*route*)[[source]](../../_modules/celery/app/routes.html#Router.expand_destination)

    lookup\_route(*name*, *args=None*, *kwargs=None*, *options=None*, *task\_type=None*)[[source]](../../_modules/celery/app/routes.html#Router.lookup_route)

    query\_router(*router*, *task*, *args*, *kwargs*, *options*, *task\_type*)[[source]](../../_modules/celery/app/routes.html#Router.query_router)

    route(*options*, *name*, *args=()*, *kwargs=None*, *task\_type=None*)[[source]](../../_modules/celery/app/routes.html#Router.route)

celery.app.routes.expand\_router\_string(*router*)[[source]](../../_modules/celery/app/routes.html#expand_router_string)

celery.app.routes.prepare(*routes*)[[source]](../../_modules/celery/app/routes.html#prepare)
:   Expand the [`task_routes`](../../userguide/configuration.html#std-setting-task_routes) setting.