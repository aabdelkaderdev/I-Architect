<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.bin.multi.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.bin.multi.html).

# `celery.bin.multi`

Start multiple worker instances from the command-line.

Examples

```
$ # Single worker with explicit name and events enabled.
$ celery multi start Leslie -E

$ # Pidfiles and logfiles are stored in the current directory
$ # by default.  Use --pidfile and --logfile argument to change
$ # this.  The abbreviation %n will be expanded to the current
$ # node name.
$ celery multi start Leslie -E --pidfile=/var/run/celery/%n.pid
                               --logfile=/var/log/celery/%n%I.log

$ # You need to add the same arguments when you restart,
$ # as these aren't persisted anywhere.
$ celery multi restart Leslie -E --pidfile=/var/run/celery/%n.pid
                                 --logfile=/var/log/celery/%n%I.log

$ # To stop the node, you need to specify the same pidfile.
$ celery multi stop Leslie --pidfile=/var/run/celery/%n.pid

$ # 3 workers, with 3 processes each
$ celery multi start 3 -c 3
celery worker -n celery1@myhost -c 3
celery worker -n celery2@myhost -c 3
celery worker -n celery3@myhost -c 3

$ # override name prefix when using range
$ celery multi start 3 --range-prefix=worker -c 3
celery worker -n worker1@myhost -c 3
celery worker -n worker2@myhost -c 3
celery worker -n worker3@myhost -c 3

$ # start 3 named workers
$ celery multi start image video data -c 3
celery worker -n image@myhost -c 3
celery worker -n video@myhost -c 3
celery worker -n data@myhost -c 3

$ # specify custom hostname
$ celery multi start 2 --hostname=worker.example.com -c 3
celery worker -n celery1@worker.example.com -c 3
celery worker -n celery2@worker.example.com -c 3

$ # specify fully qualified nodenames
$ celery multi start foo@worker.example.com bar@worker.example.com -c 3

$ # fully qualified nodenames but using the current hostname
$ celery multi start foo@%h bar@%h

$ # Advanced example starting 10 workers in the background:
$ #   * Three of the workers processes the images and video queue
$ #   * Two of the workers processes the data queue with loglevel DEBUG
$ #   * the rest processes the default' queue.
$ celery multi start 10 -l INFO -Q:1-3 images,video -Q:4,5 data
    -Q default -L:4,5 DEBUG

$ # You can show the commands necessary to start the workers with
$ # the 'show' command:
$ celery multi show 10 -l INFO -Q:1-3 images,video -Q:4,5 data
    -Q default -L:4,5 DEBUG

$ # Additional options are added to each celery worker's command,
$ # but you can also modify the options for ranges of, or specific workers

$ # 3 workers: Two with 3 processes, and one with 10 processes.
$ celery multi start 3 -c 3 -c:1 10
celery worker -n celery1@myhost -c 10
celery worker -n celery2@myhost -c 3
celery worker -n celery3@myhost -c 3

$ # can also specify options for named workers
$ celery multi start image video data -c 3 -c:image 10
celery worker -n image@myhost -c 10
celery worker -n video@myhost -c 3
celery worker -n data@myhost -c 3

$ # ranges and lists of workers in options is also allowed:
$ # (-c:1-3 can also be written as -c:1,2,3)
$ celery multi start 5 -c 3  -c:1-3 10
celery worker -n celery1@myhost -c 10
celery worker -n celery2@myhost -c 10
celery worker -n celery3@myhost -c 10
celery worker -n celery4@myhost -c 3
celery worker -n celery5@myhost -c 3

$ # lists also works with named workers
$ celery multi start foo bar baz xuzzy -c 3 -c:foo,bar,baz 10
celery worker -n foo@myhost -c 10
celery worker -n bar@myhost -c 10
celery worker -n baz@myhost -c 10
celery worker -n xuzzy@myhost -c 3
```

class celery.bin.multi.MultiTool(*env=None*, *cmd=None*, *fh=None*, *stdout=None*, *stderr=None*, *\*\*kwargs*)[[source]](../_modules/celery/bin/multi.html#MultiTool)
:   The `celery multi` program.

    Cluster(*nodes*, *cmd=None*)[[source]](../_modules/celery/bin/multi.html#MultiTool.Cluster)

    property DOWN

    property FAILED

    class MultiParser(*cmd='celery worker'*, *append=''*, *prefix=''*, *suffix=''*, *range\_prefix='celery'*)
    :   class Node(*name*, *cmd=None*, *append=None*, *options=None*, *extra\_args=None*)
        :   Represents a node in a cluster.

            alive()

            property argv\_with\_executable

            property executable

            classmethod from\_kwargs(*name*, *\*\*kwargs*)

            getopt(*\*alt*)

            handle\_process\_exit(*retcode*, *on\_signalled=None*, *on\_failure=None*)

            property logfile

            property pid

            property pidfile

            prepare\_argv(*argv*, *path*)

            send(*sig*, *on\_error=None*)

            start(*env=None*, *\*\*kwargs*)

        parse(*p*)

    property OK

    OptionParser
    :   alias of `NamespacedOptionParser`

    call\_command(*command*, *argv*)[[source]](../_modules/celery/bin/multi.html#MultiTool.call_command)

    cluster\_from\_argv(*argv*, *cmd=None*)[[source]](../_modules/celery/bin/multi.html#MultiTool.cluster_from_argv)

    execute\_from\_commandline(*argv*, *cmd=None*)[[source]](../_modules/celery/bin/multi.html#MultiTool.execute_from_commandline)

    expand(*template*, *\*argv*)[[source]](../_modules/celery/bin/multi.html#MultiTool.expand)

    get(*wanted*, *\*argv*)[[source]](../_modules/celery/bin/multi.html#MultiTool.get)

    help(*\*argv*)[[source]](../_modules/celery/bin/multi.html#MultiTool.help)

    kill(*cluster*)[[source]](../_modules/celery/bin/multi.html#MultiTool.kill)

    names(*cluster*)[[source]](../_modules/celery/bin/multi.html#MultiTool.names)

    on\_child\_failure(*node*, *retcode*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_child_failure)

    on\_child\_signalled(*node*, *signum*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_child_signalled)

    on\_child\_spawn(*node*, *argstr*, *env*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_child_spawn)

    on\_node\_down(*node*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_node_down)

    on\_node\_restart(*node*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_node_restart)

    on\_node\_shutdown\_ok(*node*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_node_shutdown_ok)

    on\_node\_signal(*node*, *sig*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_node_signal)

    on\_node\_signal\_dead(*node*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_node_signal_dead)

    on\_node\_start(*node*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_node_start)

    on\_node\_status(*node*, *retval*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_node_status)

    on\_send\_signal(*node*, *sig*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_send_signal)

    on\_still\_waiting\_end()[[source]](../_modules/celery/bin/multi.html#MultiTool.on_still_waiting_end)

    on\_still\_waiting\_for(*nodes*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_still_waiting_for)

    on\_still\_waiting\_progress(*nodes*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_still_waiting_progress)

    on\_stopping\_preamble(*nodes*)[[source]](../_modules/celery/bin/multi.html#MultiTool.on_stopping_preamble)

    reserved\_options = [('--nosplash', 'nosplash'), ('--quiet', 'quiet'), ('-q', 'quiet'), ('--verbose', 'verbose'), ('--no-color', 'no\_color')]

    restart(*cluster*, *sig*, *\*\*kwargs*)[[source]](../_modules/celery/bin/multi.html#MultiTool.restart)

    show(*cluster*)[[source]](../_modules/celery/bin/multi.html#MultiTool.show)

    start(*cluster*)[[source]](../_modules/celery/bin/multi.html#MultiTool.start)

    stop(*cluster*, *sig*, *\*\*kwargs*)[[source]](../_modules/celery/bin/multi.html#MultiTool.stop)

    stop\_verify(*cluster*, *sig*, *\*\*kwargs*)

    stopwait(*cluster*, *sig*, *\*\*kwargs*)[[source]](../_modules/celery/bin/multi.html#MultiTool.stopwait)

    validate\_arguments(*argv*)[[source]](../_modules/celery/bin/multi.html#MultiTool.validate_arguments)