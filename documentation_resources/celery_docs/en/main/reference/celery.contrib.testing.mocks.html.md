<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.contrib.testing.mocks.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.testing.mocks.html).

# `celery.contrib.testing.mocks`

## 

Useful mocks for unit testing.

celery.contrib.testing.mocks.ContextMock(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/mocks.html#ContextMock)
:   Mock that mocks [`with`](https://docs.python.org/dev/reference/compound_stmts.html#with "(in Python v3.15)") statement contexts.

celery.contrib.testing.mocks.TaskMessage(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *id: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = None*, *args: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)") = ()*, *kwargs: [Mapping](https://docs.python.org/dev/library/typing.html#typing.Mapping "(in Python v3.15)") = None*, *callbacks: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] = None*, *errbacks: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] = None*, *chain: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] = None*, *shadow: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = None*, *utc: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = None*, *\*\*options: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/mocks.html#TaskMessage)
:   Create task message in protocol 2 format.

celery.contrib.testing.mocks.TaskMessage1(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *id: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = None*, *args: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)") = ()*, *kwargs: [Mapping](https://docs.python.org/dev/library/typing.html#typing.Mapping "(in Python v3.15)") = None*, *callbacks: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] = None*, *errbacks: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] = None*, *chain: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] = None*, *\*\*options: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/mocks.html#TaskMessage1)
:   Create task message in protocol 1 format.

celery.contrib.testing.mocks.task\_message\_from\_sig(*app: [Celery](celery.html#celery.Celery "celery.app.base.Celery")*, *sig: [Signature](celery.html#celery.Signature "celery.canvas.Signature")*, *utc: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*, *TaskMessage: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)") = <function TaskMessage>*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/mocks.html#task_message_from_sig)
:   Create task message from [`celery.Signature`](celery.html#celery.Signature "celery.Signature").

    Example

    ```
    >>> m = task_message_from_sig(app, add.s(2, 2))
    >>> amqp_client.basic_publish(m, exchange='ex', routing_key='rkey')
    ```