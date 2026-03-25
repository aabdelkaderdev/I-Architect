<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.app.autoretry.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.autoretry.html).

# `celery.app.autoretry`

Tasks auto-retry functionality.

celery.app.autoretry.add\_autoretry\_behaviour(*task*, *\*\*options*)[[source]](../_modules/celery/app/autoretry.html#add_autoretry_behaviour)
:   Wrap task’s run method with auto-retry functionality.