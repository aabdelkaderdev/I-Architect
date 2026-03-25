<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.events.dumper.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.events.dumper.html).

# `celery.events.dumper`

Utility to dump events to screen.

This is a simple program that dumps events to the console
as they happen. Think of it like a tcpdump for Celery events.

class celery.events.dumper.Dumper(*out=<\_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>*)[[source]](../../_modules/celery/events/dumper.html#Dumper)
:   Monitor events.

    format\_task\_event(*hostname*, *timestamp*, *type*, *task*, *event*)[[source]](../../_modules/celery/events/dumper.html#Dumper.format_task_event)

    on\_event(*ev*)[[source]](../../_modules/celery/events/dumper.html#Dumper.on_event)

    say(*msg*)[[source]](../../_modules/celery/events/dumper.html#Dumper.say)

celery.events.dumper.evdump(*app=None*, *out=<\_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>*)[[source]](../../_modules/celery/events/dumper.html#evdump)
:   Start event dump.