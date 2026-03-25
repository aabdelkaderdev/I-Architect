<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.app.annotations.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.app.annotations.html).

# `celery.app.annotations`

Task Annotations.

Annotations is a nice term for monkey-patching task classes
in the configuration.

This prepares and performs the annotations in the
[`task_annotations`](../../userguide/configuration.html#std-setting-task_annotations) setting.

class celery.app.annotations.MapAnnotation[[source]](../../_modules/celery/app/annotations.html#MapAnnotation)
:   Annotation map: task\_name => attributes.

    annotate(*task*)[[source]](../../_modules/celery/app/annotations.html#MapAnnotation.annotate)

    annotate\_any()[[source]](../../_modules/celery/app/annotations.html#MapAnnotation.annotate_any)

celery.app.annotations.prepare(*annotations*)[[source]](../../_modules/celery/app/annotations.html#prepare)
:   Expand the [`task_annotations`](../../userguide/configuration.html#std-setting-task_annotations) setting.

celery.app.annotations.resolve\_all(*anno*, *task*)[[source]](../../_modules/celery/app/annotations.html#resolve_all)
:   Resolve all pending annotations.