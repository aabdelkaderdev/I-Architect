<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.filesystem.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.filesystem.html).

# `celery.backends.filesystem`

File-system result store backend.

class celery.backends.filesystem.FilesystemBackend(*url=None*, *open=<built-in function open>*, *unlink=<built-in function unlink>*, *sep='/'*, *encoding='UTF-8'*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend)
:   File-system result backend.

    Parameters:
    :   - **url** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – URL to the directory we should use
        - **open** (*Callable*) – open function to use when opening files
        - **unlink** (*Callable*) – unlink function to use when deleting files
        - **sep** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – directory separator (to join the directory with the key)
        - **encoding** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – encoding used on the file-system

    cleanup()[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend.cleanup)
    :   Delete expired meta-data.

    delete(*key*)[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend.delete)

    get(*key*)[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend.get)

    mget(*keys*)[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend.mget)

    set(*key*, *value*)[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend.set)