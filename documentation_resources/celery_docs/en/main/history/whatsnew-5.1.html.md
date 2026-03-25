<!-- Source: https://docs.celeryq.dev/en/main/history/whatsnew-5.1.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/history/whatsnew-5.1.html).

# What’s new in Celery 5.1 (Sun Harmonics)

Author:
:   Josue Balandrano Coronel (`jbc at rmcomplexity.com`)

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

This version is officially supported on CPython 3.6, 3.7 & 3.8 & 3.9
and is also supported on PyPy3.

## 

The 5.1.0 release is a new minor release for Celery.

Starting from now users should expect more frequent releases of major versions
as we move fast and break things to bring you even better experience.

Releases in the 5.x series are codenamed after songs of [Jon Hopkins](https://en.wikipedia.org/wiki/Jon_Hopkins).
This release has been codenamed [Sun Harmonics](https://www.youtube.com/watch?v=pCwjSoBm_pI).

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

0xflotus <[0xflotus@gmail.com](mailto:0xflotus%40gmail.com)>
AbdealiJK <[abdealikothari@gmail.com](mailto:abdealikothari%40gmail.com)>
Anatoliy <[apeks37@yandex.ru](mailto:apeks37%40yandex.ru)>
Anna Borzenko <[aaa-nn-a@mail.ru](mailto:aaa-nn-a%40mail.ru)>
aruseni <[aruseni.magiku@gmail.com](mailto:aruseni.magiku%40gmail.com)>
Asif Saif Uddin (Auvi) <[auvipy@gmail.com](mailto:auvipy%40gmail.com)>
Asif Saif Uddin <[auvipy@gmail.com](mailto:auvipy%40gmail.com)>
Awais Qureshi <[awais.qureshi@arbisoft.com](mailto:awais.qureshi%40arbisoft.com)>
careljonkhout <[carel.jonkhout@gmail.com](mailto:carel.jonkhout%40gmail.com)>
Christian Clauss <[cclauss@me.com](mailto:cclauss%40me.com)>
danthegoodman1 <[xxdanthegoodmanxx@gmail.com](mailto:xxdanthegoodmanxx%40gmail.com)>
Dave Johansen <[davejohansen@gmail.com](mailto:davejohansen%40gmail.com)>
David Schneider <[schneidav81@gmail.com](mailto:schneidav81%40gmail.com)>
Fahmi <[fahmimodelo@gmail.com](mailto:fahmimodelo%40gmail.com)>
Felix Yan <[felixonmars@archlinux.org](mailto:felixonmars%40archlinux.org)>
Gabriel Augendre <[gabriel@augendre.info](mailto:gabriel%40augendre.info)>
galcohen <[gal.cohen@autodesk.com](mailto:gal.cohen%40autodesk.com)>
gal cohen <[gal.nevis@gmail.com](mailto:gal.nevis%40gmail.com)>
Geunsik Lim <[leemgs@gmail.com](mailto:leemgs%40gmail.com)>
Guillaume DE SUSANNE D’EPINAY <[guillaume.desusanne@ssi.gouv.fr](mailto:guillaume.desusanne%40ssi.gouv.fr)>
Hilmar Hilmarsson <[hilmarh@gmail.com](mailto:hilmarh%40gmail.com)>
Illia Volochii <[illia.volochii@gmail.com](mailto:illia.volochii%40gmail.com)>
jenhaoyang <[randy19962@gmail.com](mailto:randy19962%40gmail.com)>
Jonathan Stoppani <[jonathan@stoppani.name](mailto:jonathan%40stoppani.name)>
Josue Balandrano Coronel <[jbc@rmcomplexity.com](mailto:jbc%40rmcomplexity.com)>
kosarchuksn <[sergeykosarchuk@gmail.com](mailto:sergeykosarchuk%40gmail.com)>
Kostya Deev <[kostya.deev@bluware.com](mailto:kostya.deev%40bluware.com)>
Matt Hoffman <[mjhoffman65@gmail.com](mailto:mjhoffman65%40gmail.com)>
Matus Valo <[matusvalo@gmail.com](mailto:matusvalo%40gmail.com)>
Myeongseok Seo <[clichedmoog@gmail.com](mailto:clichedmoog%40gmail.com)>
Noam <[noamkush@gmail.com](mailto:noamkush%40gmail.com)>
Omer Katz <[omer.drow@gmail.com](mailto:omer.drow%40gmail.com)>
pavlos kallis <[pakallis@gmail.com](mailto:pakallis%40gmail.com)>
Pavol Plaskoň <[pavol.plaskon@gmail.com](mailto:pavol.plaskon%40gmail.com)>
Pengjie Song (宋鹏捷) <[spengjie@sina.com](mailto:spengjie%40sina.com)>
Sardorbek Imomaliev <[sardorbek.imomaliev@gmail.com](mailto:sardorbek.imomaliev%40gmail.com)>
Sergey Lyapustin <[s.lyapustin@gmail.com](mailto:s.lyapustin%40gmail.com)>
Sergey Tikhonov <[zimbler@gmail.com](mailto:zimbler%40gmail.com)>
Stephen J. Fuhry <[steve@tpastream.com](mailto:steve%40tpastream.com)>
Swen Kooij <[swen@sectorlabs.ro](mailto:swen%40sectorlabs.ro)>
tned73 <[edwin@tranzer.com](mailto:edwin%40tranzer.com)>
Tomas Hrnciar <[thrnciar@redhat.com](mailto:thrnciar%40redhat.com)>
tumb1er <[zimbler@gmail.com](mailto:zimbler%40gmail.com)>

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
mentioned in the [following section](whatsnew-5.0.html#v500-important).

You should verify that none of the breaking changes in the CLI
do not affect you. Please refer to [New Command Line Interface](whatsnew-5.0.html#new-command-line-interface) for details.

### 

Celery 5.x only supports Python 3. Therefore, you must ensure your code is
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
- CPython 3.9
- PyPy3.6 7.2 (`pypy3`)

### 

#### Kombu

Starting from v5.1, the minimum required version is Kombu 5.1.0.

#### Py-AMQP

Starting from Celery 5.1, py-amqp will always validate certificates received from the server
and it is no longer required to manually set `cert_reqs` to `ssl.CERT_REQUIRED`.

The previous default, `ssl.CERT_NONE` is insecure and we its usage should be discouraged.
If you’d like to revert to the previous insecure default set `cert_reqs` to `ssl.CERT_NONE`

```
import ssl

broker_use_ssl = {
  'keyfile': '/var/ssl/private/worker-key.pem',
  'certfile': '/var/ssl/amqp-server-cert.pem',
  'ca_certs': '/var/ssl/myca.pem',
  'cert_reqs': ssl.CERT_NONE
}
```

#### Billiard

Starting from v5.1, the minimum required version is Billiard 3.6.4.

### 

#### Dropped support for Python 2.7 & 3.5

Celery now requires Python 3.6 and above.

Python 2.7 has reached EOL in January 2020.
In order to focus our efforts we have dropped support for Python 2.7 in
this version.

In addition, Python 3.5 has reached EOL in September 2020.
Therefore, we are also dropping support for Python 3.5.

If you still require to run Celery using Python 2.7 or Python 3.5
you can still use Celery 4.x.
However we encourage you to upgrade to a supported Python version since
no further security patches will be applied for Python 2.7 or
Python 3.5.

#### Eventlet Workers Pool

Due to [eventlet/eventlet#526](https://github.com/eventlet/eventlet/issues/526)
the minimum required version is eventlet 0.26.1.

#### Gevent Workers Pool

Starting from v5.0, the minimum required version is gevent 1.0.0.

#### Couchbase Result Backend

The Couchbase result backend now uses the V3 Couchbase SDK.

As a result, we no longer support Couchbase Server 5.x.

Also, starting from v5.0, the minimum required version
for the database client is couchbase 3.0.0.

To verify that your Couchbase Server is compatible with the V3 SDK,
please refer to their [documentation](https://docs.couchbase.com/python-sdk/3.0/project-docs/compatibility.html).

#### Riak Result Backend

The Riak result backend has been removed as the database is no longer maintained.

The Python client only supports Python 3.6 and below which prevents us from
supporting it and it is also unmaintained.

If you are still using Riak, refrain from upgrading to Celery 5.0 while you
migrate your application to a different database.

We apologize for the lack of notice in advance but we feel that the chance
you’ll be affected by this breaking change is minimal which is why we
did it.

#### AMQP Result Backend

The AMQP result backend has been removed as it was deprecated in version 4.0.

#### Removed Deprecated Modules

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

Given the SDK changes between 0.50.0 and 7.0.0 Kombu deprecates support for
older azure-servicebus versions.

## 

### 

With Kombu v5.1.0 we now support Azure Services Bus.

Azure have completely changed the Azure ServiceBus SDK between 0.50.0 and 7.0.0.
azure-servicebus >= 7.0.0 is now required for Kombu 5.1.0

### 

Following the changes in SQLAlchemy 1.4, the declarative base is no
longer an extension.
Importing it from sqlalchemy.ext.declarative is deprecated and will
be removed in SQLAlchemy 2.0.

### 

Previously, the username was ignored from the URI.
Starting from Redis>=6.0, that shouldn’t be the case since ACL support has landed.

Please refer to the [documentation](../userguide/configuration.html#conf-redis-result-backend) for details.

### 

SQS now supports managed visibility timeout. This lets us implement a back off
policy (for instance, an exponential policy) which means that the time between
task failures will dynamically change based on the number of retries.

Documentation: [Amazon SQS Transport - kombu.transport.SQS](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.transport.SQS.html "(in Kombu v5.6)")

### 

The trace function fetches the metadata from the backend each time it
receives a task and compares its state. If the state is SUCCESS,
we log and bail instead of executing the task.
The task is acknowledged and everything proceeds normally.

Documentation: [`worker_deduplicate_successful_tasks`](../userguide/configuration.html#std-setting-worker_deduplicate_successful_tasks)

### 

Tasks with late acknowledgement keep running after restart,
although the connection is lost and they cannot be
acknowledged anymore. These tasks will now be terminated.

Documentation: [`worker_cancel_long_running_tasks_on_connection_loss`](../userguide/configuration.html#std-setting-worker_cancel_long_running_tasks_on_connection_loss)

### 

task.apply\_async now supports passing ignore\_result which will act the same
as using `@app.task(ignore_result=True)`.

### 

cached\_property is heavily used in celery but it is causing
issues in multi-threaded code since it is not thread safe.
Celery is now using a thread-safe implementation of cached\_property.

### 

Tasks can now be defined like this:

```
from celery import shared_task

@shared_task
def my_func(*, name='default', age, city='Kyiv'):
    pass
```

### 

The STS token requires a refresh after a certain period of time.
After sts\_token\_timeout is reached, a new token will be created.

Documentation: [Using Amazon SQS](../getting-started/backends-and-brokers/sqs.html)

### 

health\_check\_interval can be configured and will be passed to redis-py.

Documentation: [`redis_backend_health_check_interval`](../userguide/configuration.html#std-setting-redis_backend_health_check_interval)

### 

The pickle protocol version was updated to allow Celery to serialize larger
strings among other benefits.

See: <https://docs.python.org/3.9/library/pickle.html#data-stream-format>

### 

See documentation for more info:
[Using Redis](../getting-started/backends-and-brokers/redis.html)