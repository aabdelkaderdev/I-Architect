<!-- Source: https://docs.celeryq.dev/en/main/history/whatsnew-5.0.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/history/whatsnew-5.0.html).

# What’s new in Celery 5.0 (singularity)

Author:
:   Omer Katz (`omer.drow at gmail.com`)

Celery is a simple, flexible, and reliable distributed programming framework
to process vast amounts of messages, while providing operations with
the tools required to maintain a distributed system with python.

It’s a task queue with focus on real-time processing, while also
supporting task scheduling.

Celery has a large and diverse community of users and contributors,
you should come join us on IRC
or our mailing-list.

To read more about Celery you should go read the [introduction](../getting-started/introduction.html#intro).

While this version is **mostly** backward compatible with previous versions
it’s important that you read the following section as this release
is a new major version.

This version is officially supported on CPython 3.6, 3.7 & 3.8
and is also supported on PyPy3.

## 

The 5.0.0 release is a new major release for Celery.

Starting from now users should expect more frequent releases of major versions
as we move fast and break things to bring you even better experience.

Releases in the 5.x series are codenamed after songs of [Jon Hopkins](https://en.wikipedia.org/wiki/Jon_Hopkins).
This release has been codenamed [Singularity](https://www.youtube.com/watch?v=lkvnpHFajt0).

This version drops support for Python 2.7.x which has reached EOL
in January 1st, 2020.
This allows us, the maintainers to focus on innovating without worrying
for backwards compatibility.

From now on we only support Python 3.6 and above.
We will maintain compatibility with Python 3.6 until it’s
EOL in December, 2021.

*— Omer Katz*

### 

As we’d like to provide some time for you to transition,
we’re designating Celery 4.x an LTS release.
Celery 4.x will be supported until the 1st of August, 2021.

We will accept and apply patches for bug fixes and security issues.
However, no new features will be merged for that version.

Celery 5.x **is not** an LTS release. We will support it until the release
of Celery 6.x.

We’re in the process of defining our Long Term Support policy.
Watch the next “What’s New” document for updates.

### 

Artem Vasilyev <[artem.v.vasilyev@gmail.com](mailto:artem.v.vasilyev%40gmail.com)>
Ash Berlin-Taylor <[ash\_github@firemirror.com](mailto:ash_github%40firemirror.com)>
Asif Saif Uddin (Auvi) <[auvipy@gmail.com](mailto:auvipy%40gmail.com)>
Asif Saif Uddin <[auvipy@gmail.com](mailto:auvipy%40gmail.com)>
Christian Clauss <[cclauss@me.com](mailto:cclauss%40me.com)>
Germain Chazot <[g.chazot@gmail.com](mailto:g.chazot%40gmail.com)>
Harry Moreno <[morenoh149@gmail.com](mailto:morenoh149%40gmail.com)>
kevinbai <[kevinbai.cn@gmail.com](mailto:kevinbai.cn%40gmail.com)>
Martin Paulus <[mpaulus@lequest.com](mailto:mpaulus%40lequest.com)>
Matus Valo <[matusvalo@gmail.com](mailto:matusvalo%40gmail.com)>
Matus Valo <[matusvalo@users.noreply.github.com](mailto:matusvalo%40users.noreply.github.com)>
maybe-sybr <[58414429+maybe-sybr@users.noreply.github.com](mailto:58414429+maybe-sybr%40users.noreply.github.com)>
Omer Katz <[omer.drow@gmail.com](mailto:omer.drow%40gmail.com)>
Patrick Cloke <[clokep@users.noreply.github.com](mailto:clokep%40users.noreply.github.com)>
qiaocc <[jasonqiao36@gmail.com](mailto:jasonqiao36%40gmail.com)>
Thomas Grainger <[tagrain@gmail.com](mailto:tagrain%40gmail.com)>
Weiliang Li <[to.be.impressive@gmail.com](mailto:to.be.impressive%40gmail.com)>

Note

This wall was automatically generated from git history,
so sadly it doesn’t not include the people who help with more important
things like answering mailing-list questions.

## 

### 

Celery 5.0 introduces a new CLI implementation which isn’t completely backwards compatible.

The global options can no longer be positioned after the sub-command.
Instead, they must be positioned as an option for the celery command like so:

```
celery --app path.to.app worker
```

If you were using our [Daemonization](../userguide/daemonizing.html#daemonizing) guide to deploy Celery in production,
you should revisit it for updates.

### 

If you haven’t already updated your configuration when you migrated to Celery 4.0,
please do so now.

We elected to extend the deprecation period until 6.0 since
we did not loudly warn about using these deprecated settings.

Please refer to the [migration guide](../userguide/configuration.html#conf-old-settings-map) for instructions.

### 

Make sure you are not affected by any of the important upgrade notes
mentioned in the [following section](#v500-important).

You should mainly verify that any of the breaking changes in the CLI
do not affect you. Please refer to [New Command Line Interface](#new-command-line-interface) for details.

### 

Celery 5.0 supports only Python 3. Therefore, you must ensure your code is
compatible with Python 3.

If you haven’t ported your code to Python 3, you must do so before upgrading.

You can use tools like [2to3](https://docs.python.org/3.8/library/2to3.html)
and [pyupgrade](https://github.com/asottile/pyupgrade) to assist you with
this effort.

After the migration is done, run your test suite with Celery 4 to ensure
nothing has been broken.

### 

At this point you can upgrade your workers and clients with the new version.

## 

### 

The supported Python Versions are:

- CPython 3.6
- CPython 3.7
- CPython 3.8
- PyPy3.6 7.2 (`pypy3`)

### 

Celery now requires Python 3.6 and above.

Python 2.7 has reached EOL in January 2020.
In order to focus our efforts we have dropped support for Python 2.7 in
this version.

In addition, Python 3.5 has reached EOL in September 2020.
Therefore, we are also dropping support for Python 3.5.

If you still require to run Celery using Python 2.7 or Python 3.5
you can still use Celery 4.x.
However we encourage you to upgrade to a supported Python version since
no further security patches will be applied for Python 2.7 and as mentioned
Python 3.5 is not supported for practical reasons.

### 

Starting from this release, the minimum required version is Kombu 5.0.0.

### 

Starting from this release, the minimum required version is Billiard 3.6.3.

### 

Due to [eventlet/eventlet#526](https://github.com/eventlet/eventlet/issues/526)
the minimum required version is eventlet 0.26.1.

### 

Starting from this release, the minimum required version is gevent 1.0.0.

### 

The Couchbase result backend now uses the V3 Couchbase SDK.

As a result, we no longer support Couchbase Server 5.x.

Also, starting from this release, the minimum required version
for the database client is couchbase 3.0.0.

To verify that your Couchbase Server is compatible with the V3 SDK,
please refer to their [documentation](https://docs.couchbase.com/python-sdk/3.0/project-docs/compatibility.html).

### 

The Riak result backend has been removed as the database is no longer maintained.

The Python client only supports Python 3.6 and below which prevents us from
supporting it and it is also unmaintained.

If you are still using Riak, refrain from upgrading to Celery 5.0 while you
migrate your application to a different database.

We apologize for the lack of notice in advance but we feel that the chance
you’ll be affected by this breaking change is minimal which is why we
did it.

### 

The AMQP result backend has been removed as it was deprecated in version 4.0.

### 

The celery.utils.encoding and the celery.task modules has been deprecated
in version 4.0 and therefore are removed in 5.0.

If you were using the celery.utils.encoding module before,
you should import kombu.utils.encoding instead.

If you were using the celery.task module before, you should import directly
from the celery module instead.

If you were using from celery.task import Task you should use
from celery import Task instead.

If you were using the celery.task decorator you should use
celery.shared\_task instead.

### 

The command line interface has been revamped using Click.
As a result a few breaking changes has been introduced:

- Postfix global options like celery worker –app path.to.app or celery worker –workdir /path/to/workdir are no longer supported.
  You should specify them as part of the global options of the main celery command.
- **celery amqp** and **celery shell** require the repl
  sub command to start a shell. You can now also invoke specific commands
  without a shell. Type celery amqp –help or celery shell –help for details.
- The API for adding user options has changed.
  Refer to the [documentation](../userguide/extending.html#extending-command-options) for details.

Click provides shell completion [out of the box](https://click.palletsprojects.com/en/7.x/bashcomplete/).
This functionality replaces our previous bash completion script and adds
completion support for the zsh and fish shells.

The bash completion script was exported to [extras/celery.bash](https://github.com/celery/celery/blob/master/extra/bash-completion/celery.bash)
for the packager’s convenience.

### 

Starting from Celery 5.0, the pytest plugin is no longer enabled by default.

Please refer to the [documentation](../userguide/testing.html#pytest-plugin) for instructions.

### 

Previously group results were not ordered by their invocation order.
Celery 4.4.7 introduced an opt-in feature to make them ordered.

It is now an opt-out behavior.

If you were previously using the Redis result backend, you might need to
opt-out of this behavior.

Please refer to the [documentation](../getting-started/backends-and-brokers/redis.html#redis-group-result-ordering)
for instructions on how to disable this feature.

## 

### 

The retry policy for the Redis result backend is now exposed through
the result backend transport options.

Please refer to the [documentation](../getting-started/backends-and-brokers/redis.html#redis-result-backend-timeout) for details.