<!-- Source: https://docs.celeryq.dev/en/main/getting-started/introduction.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/getting-started/introduction.html).

# Introduction to Celery

## 

Task queues are used as a mechanism to distribute work across threads or
machines.

A task queue’s input is a unit of work called a task. Dedicated worker
processes constantly monitor task queues for new work to perform.

Celery communicates via messages, usually using a broker
to mediate between clients and workers. To initiate a task the client adds a
message to the queue, the broker then delivers that message to a worker.

A Celery system can consist of multiple workers and brokers, giving way
to high availability and horizontal scaling.

Celery is written in Python, but the protocol can be implemented in any
language. In addition to Python there’s [node-celery](https://github.com/mher/node-celery) for Node.js,
a [PHP client](https://github.com/gjedeer/celery-php), [gocelery](https://github.com/gocelery/gocelery), [gopher-celery](https://github.com/marselester/gopher-celery) for Go, and [rusty-celery](https://github.com/rusty-celery/rusty-celery) for Rust.

Language interoperability can also be achieved
exposing an HTTP endpoint and having a task that requests it (webhooks).

## 

*Celery* requires a message transport to send and receive messages.
The RabbitMQ and Redis broker transports are feature complete,
but there’s also support for a myriad of other experimental solutions, including
using SQLite for local development.

*Celery* can run on a single machine, on multiple machines, or even
across data centers.

## 

If this is the first time you’re trying to use Celery, or if you haven’t
kept up with development in the 3.1 version and are coming from previous versions,
then you should read our getting started tutorials:

- [First Steps with Celery](first-steps-with-celery.html#first-steps)
- [Next Steps](next-steps.html#next-steps)

##

##

## 

Celery is easy to integrate with web frameworks, some of them even have
integration packages:

> |  |  |
> | --- | --- |
> | [Pyramid](http://docs.pylonsproject.org/en/latest/docs/pyramid.html) | <https://pypi.org/project/pyramid_celery/> |
> | [Pylons](http://pylonshq.com/) | <https://pypi.org/project/celery-pylons/> |
> | [Flask](http://flask.pocoo.org/) | not needed |
> | [web2py](http://web2py.com/) | <https://pypi.org/project/web2py-celery/> |
> | [Tornado](http://www.tornadoweb.org/) | <https://pypi.org/project/tornado-celery/> |
> | [Tryton](http://www.tryton.org/) | <https://pypi.org/project/celery_tryton/> |

For [Django](https://djangoproject.com/) see [First steps with Django](../django/first-steps-with-django.html#django-first-steps).

The integration packages aren’t strictly necessary, but they can make
development easier, and sometimes they add important hooks like closing
database connections at *fork(2)*.

##

## 

You can install Celery either via the Python Package Index (PyPI)
or from source.

To install using **pip**:

```
$ pip install -U Celery
```

### Bundles

Celery also defines a group of bundles that can be used
to install Celery and the dependencies for a given feature.

You can specify these in your requirements or on the **pip**
command-line by using brackets. Multiple bundles can be specified by
separating them by commas.

```
$ pip install "celery[librabbitmq]"

$ pip install "celery[librabbitmq,redis,auth,msgpack]"
```

The following bundles are available:

#### Serializers

`celery[auth]`:
:   for using the `auth` security serializer.

`celery[msgpack]`:
:   for using the msgpack serializer.

`celery[yaml]`:
:   for using the yaml serializer.

#### Concurrency

`celery[eventlet]`:
:   for using the <https://pypi.org/project/eventlet/> pool.

`celery[gevent]`:
:   for using the <https://pypi.org/project/gevent/> pool.

#### Transports and Backends

`celery[librabbitmq]`:
:   for using the librabbitmq C library.

`celery[redis]`:
:   for using Redis as a message transport or as a result backend.

`celery[sqs]`:
:   for using Amazon SQS as a message transport (*experimental*).

`celery[tblib]`:
:   for using the [`task_remote_tracebacks`](../userguide/configuration.html#std-setting-task_remote_tracebacks) feature.

`celery[memcache]`:
:   for using Memcached as a result backend (using <https://pypi.org/project/pylibmc/>)

`celery[pymemcache]`:
:   for using Memcached as a result backend (pure-Python implementation).

`celery[cassandra]`:
:   for using Apache Cassandra/Astra DB as a result backend with DataStax driver.

`celery[couchbase]`:
:   for using Couchbase as a result backend.

`celery[arangodb]`:
:   for using ArangoDB as a result backend.

`celery[elasticsearch]`:
:   for using Elasticsearch as a result backend.

`celery[riak]`:
:   for using Riak as a result backend.

`celery[dynamodb]`:
:   for using AWS DynamoDB as a result backend.

`celery[zookeeper]`:
:   for using Zookeeper as a message transport.

`celery[sqlalchemy]`:
:   for using SQLAlchemy as a result backend (*supported*).

`celery[pyro]`:
:   for using the Pyro4 message transport (*experimental*).

`celery[slmq]`:
:   for using the SoftLayer Message Queue transport (*experimental*).

`celery[consul]`:
:   for using the Consul.io Key/Value store as a message transport or result backend (*experimental*).

`celery[django]`:
:   specifies the lowest version possible for Django support.

    You should probably not use this in your requirements, it’s here
    for informational purposes only.

`celery[gcs]`:
:   for using the Google Cloud Storage as a result backend (*experimental*).

`celery[gcpubsub]`:
:   for using the Google Cloud Pub/Sub as a message transport (*experimental*)..

### Downloading and installing from source

Download the latest version of Celery from PyPI:

<https://pypi.org/project/celery/>

You can install it by doing the following,:

```
$ tar xvfz celery-0.0.0.tar.gz
$ cd celery-0.0.0
$ python setup.py build
# python setup.py install
```

The last command must be executed as a privileged user if
you aren’t currently using a virtualenv.

### Using the development version

#### With pip

The Celery development version also requires the development
versions of <https://pypi.org/project/kombu/>, <https://pypi.org/project/amqp/>, <https://pypi.org/project/billiard/>, and <https://pypi.org/project/vine/>.

You can install the latest snapshot of these using the following
pip commands:

```
$ pip install https://github.com/celery/celery/zipball/main#egg=celery
$ pip install https://github.com/celery/billiard/zipball/main#egg=billiard
$ pip install https://github.com/celery/py-amqp/zipball/main#egg=amqp
$ pip install https://github.com/celery/kombu/zipball/main#egg=kombu
$ pip install https://github.com/celery/vine/zipball/main#egg=vine
```

#### With git

Please see the [Contributing](../contributing.html#contributing) section.