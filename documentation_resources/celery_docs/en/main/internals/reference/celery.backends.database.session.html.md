<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.database.session.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.database.session.html).

# `celery.backends.database.session`

SQLAlchemy session.

class celery.backends.database.session.SessionManager[[source]](../../_modules/celery/backends/database/session.html#SessionManager)
:   Manage SQLAlchemy sessions.

    create\_session(*dburi*, *short\_lived\_sessions=False*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/database/session.html#SessionManager.create_session)

    get\_engine(*dburi*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/database/session.html#SessionManager.get_engine)

    invalidate(*dburi*)[[source]](../../_modules/celery/backends/database/session.html#SessionManager.invalidate)
    :   Dispose cached engine/session state for a database URI.

    prepare\_models(*engine*)[[source]](../../_modules/celery/backends/database/session.html#SessionManager.prepare_models)

    session\_factory(*dburi*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/database/session.html#SessionManager.session_factory)