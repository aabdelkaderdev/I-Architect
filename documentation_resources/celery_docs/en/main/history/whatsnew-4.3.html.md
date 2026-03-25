<!-- Source: https://docs.celeryq.dev/en/main/history/whatsnew-4.3.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/history/whatsnew-4.3.html).

# What’s new in Celery 4.3 (rhubarb)

Author:
:   Omer Katz (`omer.drow at gmail.com`)

Celery is a simple, flexible, and reliable distributed system to
process vast amounts of messages, while providing operations with
the tools required to maintain such a system.

It’s a task queue with focus on real-time processing, while also
supporting task scheduling.

Celery has a large and diverse community of users and contributors,
you should come join us on IRC
or our mailing-list.

To read more about Celery you should go read the [introduction](../getting-started/introduction.html#intro).

While this version is backward compatible with previous versions
it’s important that you read the following section.

This version is officially supported on CPython 2.7, 3.4, 3.5, 3.6 & 3.7
and is also supported on PyPy2 & PyPy3.

## 

The 4.3.0 release continues to improve our efforts to provide you with
the best task execution platform for Python.

This release has been codenamed [Rhubarb](https://www.youtube.com/watch?v=_AWIqXzvX-U)
which is one of my favorite tracks from Selected Ambient Works II.

This release focuses on new features like new result backends
and a revamped security serializer along with bug fixes mainly for Celery Beat,
Canvas, a number of critical fixes for hanging workers and
fixes for several severe memory leaks.

Celery 4.3 is the first release to support Python 3.7.

We hope that 4.3 will be the last release to support Python 2.7 as we now
begin to work on Celery 5, the next generation of our task execution platform.

However, if Celery 5 will be delayed for any reason we may release
another 4.x minor version which will still support Python 2.7.

If another 4.x version will be released it will most likely drop support for
Python 3.4 as it will reach it’s EOL in March 2019.

We have also focused on reducing contribution friction.

Thanks to **Josue Balandrano Coronel**, one of our core contributors, we now have an
updated [Contributing](../contributing.html#contributing) document.
If you intend to contribute, please review it at your earliest convenience.

I have also added new issue templates, which we will continue to improve,
so that the issues you open will have more relevant information which
will allow us to help you to resolve them more easily.

*— Omer Katz*

### 

Alexander Ioannidis <[a.ioannidis.pan@gmail.com](mailto:a.ioannidis.pan%40gmail.com)>
Amir Hossein Saeid Mehr <[amir.saiedmehr@gmail.com](mailto:amir.saiedmehr%40gmail.com)>
Andrea Rabbaglietti <[rabbagliettiandrea@gmail.com](mailto:rabbagliettiandrea%40gmail.com)>
Andrey Skabelin <[andrey.skabelin@gmail.com](mailto:andrey.skabelin%40gmail.com)>
Anthony Ruhier <[anthony.ruhier@gmail.com](mailto:anthony.ruhier%40gmail.com)>
Antonin Delpeuch <[antonin@delpeuch.eu](mailto:antonin%40delpeuch.eu)>
Artem Vasilyev <[artem.v.vasilyev@gmail.com](mailto:artem.v.vasilyev%40gmail.com)>
Asif Saif Uddin (Auvi) <[auvipy@gmail.com](mailto:auvipy%40gmail.com)>
aviadatsnyk <[aviad@snyk.io](mailto:aviad%40snyk.io)>
Axel Haustant <[noirbizarre@users.noreply.github.com](mailto:noirbizarre%40users.noreply.github.com)>
Bojan Jovanovic <[bojan.jovanovic.gtech@gmail.com](mailto:bojan.jovanovic.gtech%40gmail.com)>
Brett Jackson <[brett@brettjackson.org](mailto:brett%40brettjackson.org)>
Brett Randall <[javabrett@gmail.com](mailto:javabrett%40gmail.com)>
Brian Schrader <[brian@brianschrader.com](mailto:brian%40brianschrader.com)>
Bruno Alla <[browniebroke@users.noreply.github.com](mailto:browniebroke%40users.noreply.github.com)>
Buddy <[34044521+CoffeeExpress@users.noreply.github.com](mailto:34044521+CoffeeExpress%40users.noreply.github.com)>
Charles Chan <[charleswhchan@users.noreply.github.com](mailto:charleswhchan%40users.noreply.github.com)>
Christopher Dignam <[chris@dignam.xyz](mailto:chris%40dignam.xyz)>
Ciaran Courtney <[6096029+ciarancourtney@users.noreply.github.com](mailto:6096029+ciarancourtney%40users.noreply.github.com)>
Clemens Wolff <[clemens@justamouse.com](mailto:clemens%40justamouse.com)>
Colin Watson <[cjwatson@ubuntu.com](mailto:cjwatson%40ubuntu.com)>
Daniel Hahler <[github@thequod.de](mailto:github%40thequod.de)>
Dash Winterson <[dashdanw@gmail.com](mailto:dashdanw%40gmail.com)>
Derek Harland <[donkopotamus@users.noreply.github.com](mailto:donkopotamus%40users.noreply.github.com)>
Dilip Vamsi Moturi <[16288600+dilipvamsi@users.noreply.github.com](mailto:16288600+dilipvamsi%40users.noreply.github.com)>
Dmytro Litvinov <[litvinov.dmytro.it@gmail.com](mailto:litvinov.dmytro.it%40gmail.com)>
Douglas Rohde <[douglas.rohde2@gmail.com](mailto:douglas.rohde2%40gmail.com)>
Ed Morley <[501702+edmorley@users.noreply.github.com](mailto:501702+edmorley%40users.noreply.github.com)>
Fabian Becker <[halfdan@xnorfz.de](mailto:halfdan%40xnorfz.de)>
Federico Bond <[federicobond@gmail.com](mailto:federicobond%40gmail.com)>
Fengyuan Chen <[cfy1990@gmail.com](mailto:cfy1990%40gmail.com)>
Florian CHARDIN <[othalla.lf@gmail.com](mailto:othalla.lf%40gmail.com)>
George Psarakis <[giwrgos.psarakis@gmail.com](mailto:giwrgos.psarakis%40gmail.com)>
Guilherme Caminha <[gpkc@cin.ufpe.br](mailto:gpkc%40cin.ufpe.br)>
ideascf <[ideascf@163.com](mailto:ideascf%40163.com)>
Itay <[itay.bittan@gmail.com](mailto:itay.bittan%40gmail.com)>
Jamie Alessio <[jamie@stoic.net](mailto:jamie%40stoic.net)>
Jason Held <[jasonsheld@gmail.com](mailto:jasonsheld%40gmail.com)>
Jeremy Cohen <[jcohen02@users.noreply.github.com](mailto:jcohen02%40users.noreply.github.com)>
John Arnold <[johnar@microsoft.com](mailto:johnar%40microsoft.com)>
Jon Banafato <[jonathan.banafato@gmail.com](mailto:jonathan.banafato%40gmail.com)>
Jon Dufresne <[jon.dufresne@gmail.com](mailto:jon.dufresne%40gmail.com)>
Joshua Engelman <[j.aaron.engelman@gmail.com](mailto:j.aaron.engelman%40gmail.com)>
Joshua Schmid <[jschmid@suse.com](mailto:jschmid%40suse.com)>
Josue Balandrano Coronel <[xirdneh@gmail.com](mailto:xirdneh%40gmail.com)>
K Davis <[anybodys@users.noreply.github.com](mailto:anybodys%40users.noreply.github.com)>
kidoz <[ckidoz@gmail.com](mailto:ckidoz%40gmail.com)>
Kiyohiro Yamaguchi <[kiyoya@gmail.com](mailto:kiyoya%40gmail.com)>
Korijn van Golen <[korijn@gmail.com](mailto:korijn%40gmail.com)>
Lars Kruse <[devel@sumpfralle.de](mailto:devel%40sumpfralle.de)>
Lars Rinn <[lm.rinn@outlook.com](mailto:lm.rinn%40outlook.com)>
Lewis M. Kabui <[lewis.maina@andela.com](mailto:lewis.maina%40andela.com)>
madprogrammer <[serg@anufrienko.net](mailto:serg%40anufrienko.net)>
Manuel Vázquez Acosta <[mvaled@users.noreply.github.com](mailto:mvaled%40users.noreply.github.com)>
Marcus McHale <[marcus.mchale@nuigalway.ie](mailto:marcus.mchale%40nuigalway.ie)>
Mariatta <[Mariatta@users.noreply.github.com](mailto:Mariatta%40users.noreply.github.com)>
Mario Kostelac <[mario@intercom.io](mailto:mario%40intercom.io)>
Matt Wiens <[mwiens91@gmail.com](mailto:mwiens91%40gmail.com)>
Maximilien Cuony <[the-glu@users.noreply.github.com](mailto:the-glu%40users.noreply.github.com)>
Maximilien de Bayser <[maxdebayser@gmail.com](mailto:maxdebayser%40gmail.com)>
Meysam <[MeysamAzad81@yahoo.com](mailto:MeysamAzad81%40yahoo.com)>
Milind Shakya <[milin@users.noreply.github.com](mailto:milin%40users.noreply.github.com)>
na387 <[na387@users.noreply.github.com](mailto:na387%40users.noreply.github.com)>
Nicholas Pilon <[npilon@gmail.com](mailto:npilon%40gmail.com)>
Nick Parsons <[nparsons08@gmail.com](mailto:nparsons08%40gmail.com)>
Nik Molnar <[nik.molnar@consbio.org](mailto:nik.molnar%40consbio.org)>
Noah Hall <[noah.t.hall@gmail.com](mailto:noah.t.hall%40gmail.com)>
Noam <[noamkush@users.noreply.github.com](mailto:noamkush%40users.noreply.github.com)>
Omer Katz <[omer.drow@gmail.com](mailto:omer.drow%40gmail.com)>
Paweł Adamczak <[pawel.ad@gmail.com](mailto:pawel.ad%40gmail.com)>
peng weikang <[pengwk2@gmail.com](mailto:pengwk2%40gmail.com)>
Prathamesh Salunkhe <[spratham55@gmail.com](mailto:spratham55%40gmail.com)>
Przemysław Suliga <[1270737+suligap@users.noreply.github.com](mailto:1270737+suligap%40users.noreply.github.com)>
Raf Geens <[rafgeens@gmail.com](mailto:rafgeens%40gmail.com)>
(◕ᴥ◕) <[ratson@users.noreply.github.com](mailto:ratson%40users.noreply.github.com)>
Robert Kopaczewski <[rk@23doors.com](mailto:rk%4023doors.com)>
Samuel Huang <[samhuang91@gmail.com](mailto:samhuang91%40gmail.com)>
Sebastian Wojciechowski <[42519683+sebwoj@users.noreply.github.com](mailto:42519683+sebwoj%40users.noreply.github.com)>
Seunghun Lee <[waydi1@gmail.com](mailto:waydi1%40gmail.com)>
Shanavas M <[shanavas.m2@gmail.com](mailto:shanavas.m2%40gmail.com)>
Simon Charette <[charettes@users.noreply.github.com](mailto:charettes%40users.noreply.github.com)>
Simon Schmidt <[schmidt.simon@gmail.com](mailto:schmidt.simon%40gmail.com)>
srafehi <[shadyrafehi@gmail.com](mailto:shadyrafehi%40gmail.com)>
Steven Sklar <[sklarsa@gmail.com](mailto:sklarsa%40gmail.com)>
Tom Booth <[thomasbo@microsoft.com](mailto:thomasbo%40microsoft.com)>
Tom Clancy <[ClancyTJD@users.noreply.github.com](mailto:ClancyTJD%40users.noreply.github.com)>
Toni Ruža <[gmr.gaf@gmail.com](mailto:gmr.gaf%40gmail.com)>
tothegump <[tothegump@gmail.com](mailto:tothegump%40gmail.com)>
Victor Mireyev <[victor@opennodecloud.com](mailto:victor%40opennodecloud.com)>
Vikas Prasad <[vikasprasad.prasad@gmail.com](mailto:vikasprasad.prasad%40gmail.com)>
walterqian <[walter@color.com](mailto:walter%40color.com)>
Willem <[himself@willemthiart.com](mailto:himself%40willemthiart.com)>
Xiaodong <[xd\_deng@hotmail.com](mailto:xd_deng%40hotmail.com)>
yywing <[386542536@qq.com](mailto:386542536%40qq.com)>

Note

This wall was automatically generated from git history,
so sadly it doesn’t not include the people who help with more important
things like answering mailing-list questions.

## 

Please read the important notes below as there are several breaking changes.

## 

### 

The supported Python Versions are:

- CPython 2.7
- CPython 3.4
- CPython 3.5
- CPython 3.6
- CPython 3.7
- PyPy2.7 6.0 (`pypy2`)
- PyPy3.5 6.0 (`pypy3`)

### 

Starting from this release, the minimum required version is Kombu 4.4.

#### New Compression Algorithms

Kombu 4.3 includes a few new optional compression methods:

- LZMA (available from stdlib if using Python 3 or from a backported package)
- Brotli (available if you install either the brotli or the brotlipy package)
- ZStandard (available if you install the zstandard package)

Unfortunately our current protocol generates huge payloads for complex canvases.

Until we migrate to our 3rd revision of the Celery protocol in Celery 5
which will resolve this issue, please use one of the new compression methods
as a workaround.

See [Compression](../userguide/calling.html#calling-compression) for details.

### 

Starting from this release, the minimum required version is Billiard 3.6.

### 

We now require eventlet>=0.24.1.

If you are using the eventlet workers pool please install Celery using:

```
$ pip install -U celery[eventlet]
```

### 

We’ve been using the deprecated msgpack-python package for a while.
This is now fixed as we depend on the msgpack instead.

If you are currently using the MessagePack serializer please uninstall the
previous package and reinstall the new one using:

```
$ pip uninstall msgpack-python -y
$ pip install -U celery[msgpack]
```

### 

We now support the [DNS seedlist connection format](https://docs.mongodb.com/manual/reference/connection-string/#dns-seedlist-connection-format) for the MongoDB result backend.

This requires the dnspython package.

If you are using the MongoDB result backend please install Celery using:

```
$ pip install -U celery[mongodb]
```

### 

Due to multiple bugs in earlier versions of py-redis that were causing
issues for Celery, we were forced to bump the minimum required version to 3.2.0.

### 

Due to multiple bugs in earlier versions of py-redis that were causing
issues for Celery, we were forced to bump the minimum required version to 3.2.0.

### 

The official Riak client does not support Python 3.7 as of yet.

In case you are using the Riak result backend, either attempt to install the
client from master or avoid upgrading to Python 3.7 until this matter is resolved.

In case you are using the Riak result backend with Python 3.7, we now emit
a warning.

Please track [basho/riak-python-client#534](https://github.com/basho/riak-python-client/issues/534)
for updates.

### 

Starting from this release, we officially no longer support RabbitMQ 2.x.

The last release of 2.x was in 2012 and we had to make adjustments to
correctly support high availability on RabbitMQ 3.x.

If for some reason, you are still using RabbitMQ 2.x we encourage you to upgrade
as soon as possible since security patches are no longer applied on RabbitMQ 2.x.

### 

Starting from this release, the minimum required Django version is 1.11.

### 

The auth serializer received a complete overhaul.
It was previously horribly broken.

We now depend on cryptography instead of pyOpenSSL for this serializer.

See [Message Signing](../userguide/security.html#message-signing) for details.

## 

### 

#### Redis Broker Support for SSL URIs

The Redis broker now has support for SSL connections.

You can use [`broker_use_ssl`](../userguide/configuration.html#std-setting-broker_use_ssl) as you normally did and use a
rediss:// URI.

You can also pass the SSL configuration parameters to the URI:

> rediss://localhost:3456?ssl\_keyfile=keyfile.key&ssl\_certfile=certificate.crt&ssl\_ca\_certs=ca.pem&ssl\_cert\_reqs=CERT\_REQUIRED

#### Configurable Events Exchange Name

Previously, the events exchange name was hardcoded.

You can use [`event_exchange`](../userguide/configuration.html#std-setting-event_exchange) to determine it.
The default value remains the same.

#### Configurable Pidbox Exchange Name

Previously, the Pidbox exchange name was hardcoded.

You can use [`control_exchange`](../userguide/configuration.html#std-setting-control_exchange) to determine it.
The default value remains the same.

### 

#### Redis Result Backend Support for SSL URIs

The Redis result backend now has support for SSL connections.

You can use [`redis_backend_use_ssl`](../userguide/configuration.html#std-setting-redis_backend_use_ssl) to configure it and use a
rediss:// URI.

You can also pass the SSL configuration parameters to the URI:

> rediss://localhost:3456?ssl\_keyfile=keyfile.key&ssl\_certfile=certificate.crt&ssl\_ca\_certs=ca.pem&ssl\_cert\_reqs=CERT\_REQUIRED

#### Store Extended Task Metadata in Result

When [`result_extended`](../userguide/configuration.html#std-setting-result_extended) is True the backend will store the following
metadata:

- Task Name
- Arguments
- Keyword arguments
- The worker the task was executed on
- Number of retries
- The queue’s name or routing key

In addition, `celery.app.task.update_state()` now accepts keyword arguments
which allows you to store custom data with the result.

#### Encode Results Using A Different Serializer

The [`result_accept_content`](../userguide/configuration.html#std-setting-result_accept_content) setting allows to configure different
accepted content for the result backend.

A special serializer (auth) is used for signed messaging,
however the result\_serializer remains in json, because we don’t want encrypted
content in our result backend.

To accept unsigned content from the result backend,
we introduced this new configuration option to specify the
accepted content from the backend.

#### New Result Backends

This release introduces four new result backends:

> - S3 result backend
> - ArangoDB result backend
> - Azure Block Blob Storage result backend
> - CosmosDB result backend

#### S3 Result Backend

Amazon Simple Storage Service (Amazon S3) is an object storage service by AWS.

The results are stored using the following path template:

<[`s3_bucket`](../userguide/configuration.html#std-setting-s3_bucket)>/<[`s3_base_path`](../userguide/configuration.html#std-setting-s3_base_path)>/<key>

See [S3 backend settings](../userguide/configuration.html#conf-s3-result-backend) for more information.

#### ArangoDB Result Backend

ArangoDB is a native multi-model database with search capabilities.
The backend stores the result in the following document format:

{

\_key: {key},

task: {task}

}

See [ArangoDB backend settings](../userguide/configuration.html#conf-arangodb-result-backend) for more information.

#### Azure Block Blob Storage Result Backend

Azure Block Blob Storage is an object storage service by Microsoft.

The backend stores the result in the following path template:

<[`azureblockblob_container_name`](../userguide/configuration.html#std-setting-azureblockblob_container_name)>/<key>

See [Azure Block Blob backend settings](../userguide/configuration.html#conf-azureblockblob-result-backend) for more information.

#### CosmosDB Result Backend

Azure Cosmos DB is Microsoft’s globally distributed,
multi-model database service.

The backend stores the result in the following document format:

{

id: {key},

value: {task}

}

See [CosmosDB backend settings (experimental)](../userguide/configuration.html#conf-cosmosdbsql-result-backend) for more information.

### 

#### Cythonized Tasks

Cythonized tasks are now supported.
You can generate C code from Cython that specifies a task using the @task
decorator and everything should work exactly the same.

#### Acknowledging Tasks on Failures or Timeouts

When [`task_acks_late`](../userguide/configuration.html#std-setting-task_acks_late) is set to True tasks are acknowledged on failures or
timeouts.
This makes it hard to use dead letter queues and exchanges.

Celery 4.3 introduces the new [`task_acks_on_failure_or_timeout`](../userguide/configuration.html#std-setting-task_acks_on_failure_or_timeout) which
allows you to avoid acknowledging tasks if they failed or timed out even if
[`task_acks_late`](../userguide/configuration.html#std-setting-task_acks_late) is set to True.

[`task_acks_on_failure_or_timeout`](../userguide/configuration.html#std-setting-task_acks_on_failure_or_timeout) is set to True by default.

#### Schedules Now Support Microseconds

When scheduling tasks using **celery beat** microseconds
are no longer ignored.

#### Default Task Priority

You can now set the default priority of a task using
the [`task_default_priority`](../userguide/configuration.html#std-setting-task_default_priority) setting.
The setting’s value will be used if no priority is provided for a specific
task.

#### Tasks Optionally Inherit Parent’s Priority

Setting the [`task_inherit_parent_priority`](../userguide/configuration.html#std-setting-task_inherit_parent_priority) configuration option to
True will make Celery tasks inherit the priority of the previous task
linked to it.

Examples:

```
c = celery.chain(
  add.s(2), # priority=None
  add.s(3).set(priority=5), # priority=5
  add.s(4), # priority=5
  add.s(5).set(priority=3), # priority=3
  add.s(6), # priority=3
)
```

```
@app.task(bind=True)
def child_task(self):
  pass

@app.task(bind=True)
def parent_task(self):
  child_task.delay()

# child_task will also have priority=5
parent_task.apply_async(args=[], priority=5)
```

### 

#### Chords can be Executed in Eager Mode

When [`task_always_eager`](../userguide/configuration.html#std-setting-task_always_eager) is set to True, chords are executed eagerly
as well.

#### Configurable Chord Join Timeout

Previously, `celery.result.GroupResult.join()` had a fixed timeout of 3
seconds.

The [`result_chord_join_timeout`](../userguide/configuration.html#std-setting-result_chord_join_timeout) setting now allows you to change it.

The default remains 3 seconds.