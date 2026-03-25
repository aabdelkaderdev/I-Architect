<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.app.defaults.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.defaults.html).

# `celery.app.defaults`

Configuration introspection and defaults.

class celery.app.defaults.Option(*default=None*, *\*args*, *\*\*kwargs*)[[source]](../_modules/celery/app/defaults.html#Option)
:   Describes a Celery configuration option.

    alt = None

    deprecate\_by = None

    old = {}

    remove\_by = None

    to\_python(*value*)[[source]](../_modules/celery/app/defaults.html#Option.to_python)

    typemap = {'any': <function Option.<lambda>>, 'bool': <function strtobool>, 'dict': <class 'dict'>, 'float': <class 'float'>, 'int': <class 'int'>, 'string': <class 'str'>, 'tuple': <class 'tuple'>}

celery.app.defaults.find(*name*, *namespace='celery'*)[[source]](../_modules/celery/app/defaults.html#find)
:   Find setting by name.

celery.app.defaults.flatten(*d*, *root=''*, *keyfilter=<function \_flatten\_keys>*)[[source]](../_modules/celery/app/defaults.html#flatten)
:   Flatten settings.