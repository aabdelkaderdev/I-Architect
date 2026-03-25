<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.signals.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.signals.html).

# `celery.signals`

Celery Signals.

This module defines the signals (Observer pattern) sent by
both workers and clients.

Functions can be connected to these signals, and connected
functions are called whenever a signal is called.

See also

[Signals](../userguide/signals.html#signals) for more information.