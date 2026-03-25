<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.objects.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.objects.html).

# `celery.utils.objects`

Object related utilities, including introspection, etc.

class celery.utils.objects.Bunch(*\*\*kwargs*)[[source]](../../_modules/celery/utils/objects.html#Bunch)
:   Object that enables you to modify attributes.

class celery.utils.objects.FallbackContext(*provided*, *fallback*, *\*fb\_args*, *\*\*fb\_kwargs*)[[source]](../../_modules/celery/utils/objects.html#FallbackContext)
:   Context workaround.

    The built-in `@contextmanager` utility does not work well
    when wrapping other contexts, as the traceback is wrong when
    the wrapped context raises.

    This solves this problem and can be used instead of `@contextmanager`
    in this example:

    ```
    @contextmanager
    def connection_or_default_connection(connection=None):
        if connection:
            # user already has a connection, shouldn't close
            # after use
            yield connection
        else:
            # must've new connection, and also close the connection
            # after the block returns
            with create_new_connection() as connection:
                yield connection
    ```

    This wrapper can be used instead for the above like this:

    ```
    def connection_or_default_connection(connection=None):
        return FallbackContext(connection, create_new_connection)
    ```

class celery.utils.objects.getitem\_property(*keypath*, *doc=None*)[[source]](../../_modules/celery/utils/objects.html#getitem_property)
:   Attribute -> dict key descriptor.

    The target object must support `__getitem__`,
    and optionally `__setitem__`.

    Example

    ```
    >>> from collections import defaultdict
    ```

    ```
    >>> class Me(dict):
    ...     deep = defaultdict(dict)
    ...
    ...     foo = _getitem_property('foo')
    ...     deep_thing = _getitem_property('deep.thing')
    ```

    ```
    >>> me = Me()
    >>> me.foo
    None
    ```

    ```
    >>> me.foo = 10
    >>> me.foo
    10
    >>> me['foo']
    10
    ```

    ```
    >>> me.deep_thing = 42
    >>> me.deep_thing
    42
    >>> me.deep
    defaultdict(<type 'dict'>, {'thing': 42})
    ```

celery.utils.objects.mro\_lookup(*cls*, *attr*, *stop=None*, *monkey\_patched=None*)[[source]](../../_modules/celery/utils/objects.html#mro_lookup)
:   Return the first node by MRO order that defines an attribute.

    Parameters:
    :   - **cls** (*Any*) – Child class to traverse.
        - **attr** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of attribute to find.
        - **stop** (*Set**[**Any**]*) – A set of types that if reached will stop
          the search.
        - **monkey\_patched** (*Sequence*) – Use one of the stop classes
          if the attributes module origin isn’t in this list.
          Used to detect monkey patched attributes.

    Returns:
    :   The attribute value, or `None` if not found.

    Return type:
    :   Any