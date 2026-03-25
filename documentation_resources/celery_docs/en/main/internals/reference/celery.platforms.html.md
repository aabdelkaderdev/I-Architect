<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.platforms.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.platforms.html).

# `celery.platforms`

Platforms.

Utilities dealing with platform specifics: signals, daemonization,
users, groups, and so on.

class celery.platforms.DaemonContext(*pidfile=None*, *workdir=None*, *umask=None*, *fake=False*, *after\_chdir=None*, *after\_forkers=True*, *\*\*kwargs*)[[source]](../../_modules/celery/platforms.html#DaemonContext)
:   Context manager daemonizing the process.

    close(*\*args*)[[source]](../../_modules/celery/platforms.html#DaemonContext.close)

    open()[[source]](../../_modules/celery/platforms.html#DaemonContext.open)

    redirect\_to\_null(*fd*)[[source]](../../_modules/celery/platforms.html#DaemonContext.redirect_to_null)

exception celery.platforms.LockFailed[[source]](../../_modules/celery/platforms.html#LockFailed)
:   Raised if a PID lock can’t be acquired.

class celery.platforms.Pidfile(*path*)[[source]](../../_modules/celery/platforms.html#Pidfile)
:   Pidfile.

    This is the type returned by [`create_pidlock()`](#celery.platforms.create_pidlock "celery.platforms.create_pidlock").

    See also

    Best practice is to not use this directly but rather use
    the [`create_pidlock()`](#celery.platforms.create_pidlock "celery.platforms.create_pidlock") function instead:
    more convenient and also removes stale pidfiles (when
    the process holding the lock is no longer running).

    acquire()[[source]](../../_modules/celery/platforms.html#Pidfile.acquire)
    :   Acquire lock.

    is\_locked()[[source]](../../_modules/celery/platforms.html#Pidfile.is_locked)
    :   Return true if the pid lock exists.

    path = None
    :   Path to the pid lock file.

    read\_pid()[[source]](../../_modules/celery/platforms.html#Pidfile.read_pid)
    :   Read and return the current pid.

    release(*\*args*)[[source]](../../_modules/celery/platforms.html#Pidfile.release)
    :   Release lock.

    remove()[[source]](../../_modules/celery/platforms.html#Pidfile.remove)
    :   Remove the lock.

    remove\_if\_stale()[[source]](../../_modules/celery/platforms.html#Pidfile.remove_if_stale)
    :   Remove the lock if the process isn’t running.

        I.e. process does not respond to signal.

    write\_pid()[[source]](../../_modules/celery/platforms.html#Pidfile.write_pid)

celery.platforms.close\_open\_fds(*keep=None*)[[source]](../../_modules/billiard/compat.html#close_open_fds)

celery.platforms.create\_pidlock(*pidfile*)[[source]](../../_modules/celery/platforms.html#create_pidlock)
:   Create and verify pidfile.

    If the pidfile already exists the program exits with an error message,
    however if the process it refers to isn’t running anymore, the pidfile
    is deleted and the program continues.

    This function will automatically install an [`atexit`](https://docs.python.org/dev/library/atexit.html#module-atexit "(in Python v3.15)") handler
    to release the lock at exit, you can skip this by calling
    `_create_pidlock()` instead.

    Returns:
    :   used to manage the lock.

    Return type:
    :   [Pidfile](#celery.platforms.Pidfile "celery.platforms.Pidfile")

    Example

    ```
    >>> pidlock = create_pidlock('/var/run/app.pid')
    ```

celery.platforms.detached(*logfile=None*, *pidfile=None*, *uid=None*, *gid=None*, *umask=0*, *workdir=None*, *fake=False*, *\*\*opts*)[[source]](../../_modules/celery/platforms.html#detached)
:   Detach the current process in the background (daemonize).

    Parameters:
    :   - **logfile** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Optional log file.
          The ability to write to this file
          will be verified before the process is detached.
        - **pidfile** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Optional pid file.
          The pidfile won’t be created,
          as this is the responsibility of the child. But the process will
          exit if the pid lock exists and the pid written is still running.
        - **uid** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Optional user id or user name to change
          effective privileges to.
        - **gid** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Optional group id or group name to change
          effective privileges to.
        - **umask** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – Optional umask that’ll be effective in
          the child process.
        - **workdir** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Optional new working directory.
        - **fake** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Don’t actually detach, intended for debugging purposes.
        - **\*\*opts** (*Any*) – Ignored.

    Example

    ```
    >>> from celery.platforms import detached, create_pidlock
    >>> with detached(
    ...           logfile='/var/log/app.log',
    ...           pidfile='/var/run/app.pid',
    ...           uid='nobody'):
    ... # Now in detached child process with effective user set to nobody,
    ... # and we know that our logfile can be written to, and that
    ... # the pidfile isn't locked.
    ... pidlock = create_pidlock('/var/run/app.pid')
    ...
    ... # Run the program
    ... program.run(logfile='/var/log/app.log')
    ```

celery.platforms.fd\_by\_path(*paths*)[[source]](../../_modules/celery/platforms.html#fd_by_path)
:   Return a list of file descriptors.

    This method returns list of file descriptors corresponding to
    file paths passed in paths variable.

    Parameters:
    :   **paths** – List[str]: List of file paths.

    Returns:
    :   List of file descriptors.

    Return type:
    :   List[[int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")]

    Example

    ```
    >>> keep = fd_by_path(['/dev/urandom', '/my/precious/'])
    ```

celery.platforms.get\_errno\_name(*n*)[[source]](../../_modules/celery/platforms.html#get_errno_name)
:   Get errno for string (e.g., `ENOENT`).

celery.platforms.get\_fdmax(*default=None*)[[source]](../../_modules/billiard/compat.html#get_fdmax)
:   Return the maximum number of open file descriptors
    on this system.

    Keyword Arguments:
    :   **default** – Value returned if there’s no file
        descriptor limit.

celery.platforms.ignore\_errno(*\*errnos*, *\*\*kwargs*)[[source]](../../_modules/celery/platforms.html#ignore_errno)
:   Context manager to ignore specific POSIX error codes.

    Takes a list of error codes to ignore: this can be either
    the name of the code, or the code integer itself:

    ```
    >>> with ignore_errno('ENOENT'):
    ...     with open('foo', 'r') as fh:
    ...         return fh.read()

    >>> with ignore_errno(errno.ENOENT, errno.EPERM):
    ...    pass
    ```

    Parameters:
    :   **types** (*Tuple**[*[*Exception*](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)")*]*) – A tuple of exceptions to ignore
        (when the errno matches). Defaults to [`Exception`](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)").

celery.platforms.initgroups(*uid*, *gid*)[[source]](../../_modules/celery/platforms.html#initgroups)
:   Init process group permissions.

    Compat version of [`os.initgroups()`](https://docs.python.org/dev/library/os.html#os.initgroups "(in Python v3.15)") that was first
    added to Python 2.7.

celery.platforms.isatty(*fh*)[[source]](../../_modules/celery/platforms.html#isatty)
:   Return true if the process has a controlling terminal.

celery.platforms.maybe\_drop\_privileges(*uid=None*, *gid=None*)[[source]](../../_modules/celery/platforms.html#maybe_drop_privileges)
:   Change process privileges to new user/group.

    If UID and GID is specified, the real user/group is changed.

    If only UID is specified, the real user is changed, and the group is
    changed to the users primary group.

    If only GID is specified, only the group is changed.

celery.platforms.parse\_gid(*gid*)[[source]](../../_modules/celery/platforms.html#parse_gid)
:   Parse group id.

    Parameters:
    :   **gid** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – Actual gid, or the name of a group.

    Returns:
    :   The actual gid of the group.

    Return type:
    :   [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")

celery.platforms.parse\_uid(*uid*)[[source]](../../_modules/celery/platforms.html#parse_uid)
:   Parse user id.

    Parameters:
    :   **uid** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – Actual uid, or the username of a user.

    Returns:
    :   The actual uid.

    Return type:
    :   [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")

celery.platforms.pyimplementation()[[source]](../../_modules/celery/platforms.html#pyimplementation)
:   Return string identifying the current Python implementation.

celery.platforms.set\_mp\_process\_title(*progname*, *info=None*, *hostname=None*)[[source]](../../_modules/celery/platforms.html#set_mp_process_title)
:   Set the **ps** name from the current process name.

    Only works if <https://pypi.org/project/setproctitle/> is installed.

celery.platforms.set\_process\_title(*progname*, *info=None*)[[source]](../../_modules/celery/platforms.html#set_process_title)
:   Set the **ps** name for the currently running process.

    Only works if <https://pypi.org/project/setproctitle/> is installed.

celery.platforms.setgid(*gid*)[[source]](../../_modules/celery/platforms.html#setgid)
:   Version of [`os.setgid()`](https://docs.python.org/dev/library/os.html#os.setgid "(in Python v3.15)") supporting group names.

celery.platforms.setgroups(*groups*)[[source]](../../_modules/celery/platforms.html#setgroups)
:   Set active groups from a list of group ids.

celery.platforms.setuid(*uid*)[[source]](../../_modules/celery/platforms.html#setuid)
:   Version of [`os.setuid()`](https://docs.python.org/dev/library/os.html#os.setuid "(in Python v3.15)") supporting usernames.

celery.platforms.signal\_name(*signum*)[[source]](../../_modules/celery/platforms.html#signal_name)
:   Return name of signal from signal number.