<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.gcs.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.gcs.html).

# `celery.backends.gcs`

Google Cloud Storage result store backend for Celery.

class celery.backends.gcs.GCSBackend(*\*\*kwargs*)[[source]](../../_modules/celery/backends/gcs.html#GCSBackend)
:   Google Cloud Storage task result backend.

    Uses Firestore for chord ref count.

    property firestore\_client
    :   Returns a firestore client.

    implements\_incr = True

    incr(*key: [bytes](https://docs.python.org/dev/library/stdtypes.html#bytes "(in Python v3.15)")*) → [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")[[source]](../../_modules/celery/backends/gcs.html#GCSBackend.incr)

    on\_chord\_part\_return(*request*, *state*, *result*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/gcs.html#GCSBackend.on_chord_part_return)
    :   Chord part return callback.

        Called for each task in the chord.
        Increments the counter stored in Firestore.
        If the counter reaches the number of tasks in the chord, the callback
        is called.
        If the callback raises an exception, the chord is marked as errored.
        If the callback returns a value, the chord is marked as successful.

    supports\_native\_join = True
    :   If true the backend must implement `get_many()`.