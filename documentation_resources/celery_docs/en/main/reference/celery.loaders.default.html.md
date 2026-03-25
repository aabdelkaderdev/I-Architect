<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.loaders.default.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.loaders.default.html).

# `celery.loaders.default`

The default loader used when no custom app has been initialized.

class celery.loaders.default.Loader(*app*, *\*\*kwargs*)[[source]](../_modules/celery/loaders/default.html#Loader)
:   The loader used by the default app.

    read\_configuration(*fail\_silently=True*)[[source]](../_modules/celery/loaders/default.html#Loader.read_configuration)
    :   Read configuration from `celeryconfig.py`.

    setup\_settings(*settingsdict*)[[source]](../_modules/celery/loaders/default.html#Loader.setup_settings)