<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.collections.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.collections.html).

# `celery.utils.collections`

Custom maps, sets, sequences, and other data structures.

class celery.utils.collections.AttributeDict[[source]](../../_modules/celery/utils/collections.html#AttributeDict)
:   Dict subclass with attribute access.

class celery.utils.collections.AttributeDictMixin[[source]](../../_modules/celery/utils/collections.html#AttributeDictMixin)
:   Mixin for Mapping interface that adds attribute access.

    I.e., d.key -> d[key]).

class celery.utils.collections.BufferMap(*maxsize: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*, *iterable: [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)") = None*, *bufmaxsize: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 1000*)[[source]](../../_modules/celery/utils/collections.html#BufferMap)
:   Map of buffers.

    Buffer
    :   alias of [`Messagebuffer`](#celery.utils.collections.Messagebuffer "celery.utils.collections.Messagebuffer")

    exception Empty
    :   Exception raised by Queue.get(block=0)/get\_nowait().

    bufmaxsize = None

    extend(*key: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *it: [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#BufferMap.extend)

    maxsize = None

    put(*key: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *item: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#BufferMap.put)

    take(*key: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*default: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#BufferMap.take)

    total = 0

class celery.utils.collections.ChainMap(*\*maps: [Mapping](https://docs.python.org/dev/library/collections.abc.html#collections.abc.Mapping "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../../_modules/celery/utils/collections.html#ChainMap)
:   Key lookup on a sequence of maps.

    add\_defaults(*d: [Mapping](https://docs.python.org/dev/library/collections.abc.html#collections.abc.Mapping "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#ChainMap.add_defaults)

    bind\_to(*callback*)[[source]](../../_modules/celery/utils/collections.html#ChainMap.bind_to)

    changes = None

    clear() → None.  Remove all items from D.[[source]](../../_modules/celery/utils/collections.html#ChainMap.clear)

    copy() → [ChainMap](#celery.utils.collections.ChainMap "celery.utils.collections.ChainMap")[[source]](../../_modules/celery/utils/collections.html#ChainMap.copy)

    defaults = None

    classmethod fromkeys(*iterable: [type](celery.backends.rpc.html#id5 "celery.backends.rpc.RPCBackend.Exchange.type")*, *\*args: [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")*) → [ChainMap](#celery.utils.collections.ChainMap "celery.utils.collections.ChainMap")[[source]](../../_modules/celery/utils/collections.html#ChainMap.fromkeys)
    :   Create a ChainMap with a single dict created from the iterable.

    get(*k*[, *d*]) → D[k] if k in D, else d.  d defaults to None.[[source]](../../_modules/celery/utils/collections.html#ChainMap.get)

    items() → a set-like object providing a view on D's items

    iteritems() → [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")

    iterkeys() → [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")

    itervalues() → [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")

    key\_t = None

    keys() → a set-like object providing a view on D's keys

    maps = None

    pop(*k*[, *d*]) → v, remove specified key and return the corresponding value.[[source]](../../_modules/celery/utils/collections.html#ChainMap.pop)
    :   If key is not found, d is returned if given, otherwise KeyError is raised.

    setdefault(*k*[, *d*]) → D.get(k,d), also set D[k]=d if k not in D[[source]](../../_modules/celery/utils/collections.html#ChainMap.setdefault)

    update([*E*, ]*\*\*F*) → None.  Update D from mapping/iterable E and F.[[source]](../../_modules/celery/utils/collections.html#ChainMap.update)
    :   If E present and has a .keys() method, does: for k in E: D[k] = E[k]
        If E present and lacks .keys() method, does: for (k, v) in E: D[k] = v
        In either case, this is followed by: for k, v in F.items(): D[k] = v

    values() → an object providing a view on D's values

class celery.utils.collections.ConfigurationView(*changes: [Mapping](https://docs.python.org/dev/library/collections.abc.html#collections.abc.Mapping "(in Python v3.15)")*, *defaults: [Mapping](https://docs.python.org/dev/library/collections.abc.html#collections.abc.Mapping "(in Python v3.15)") = None*, *keys: [List](https://docs.python.org/dev/library/typing.html#typing.List "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")] = None*, *prefix: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = None*)[[source]](../../_modules/celery/utils/collections.html#ConfigurationView)
:   A view over an applications configuration dictionaries.

    Custom (but older) version of [`collections.ChainMap`](https://docs.python.org/dev/library/collections.html#collections.ChainMap "(in Python v3.15)").

    If the key does not exist in `changes`, the `defaults`
    dictionaries are consulted.

    Parameters:
    :   - **changes** (*Mapping*) – Map of configuration changes.
        - **defaults** (*List**[**Mapping**]*) – List of dictionaries containing
          the default configuration.

    clear() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#ConfigurationView.clear)
    :   Remove all changes, but keep defaults.

    first(*\*keys: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#ConfigurationView.first)

    get(*k*[, *d*]) → D[k] if k in D, else d.  d defaults to None.[[source]](../../_modules/celery/utils/collections.html#ConfigurationView.get)

    swap\_with(*other: [ConfigurationView](#celery.utils.collections.ConfigurationView "celery.utils.collections.ConfigurationView")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#ConfigurationView.swap_with)

class celery.utils.collections.DictAttribute(*obj: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../../_modules/celery/utils/collections.html#DictAttribute)
:   Dict interface to attributes.

    obj[k] -> obj.k
    obj[k] = val -> obj.k = val

    get(*key: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *default: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)") = None*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#DictAttribute.get)

    items() → [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")

    iteritems() → [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")

    iterkeys() → [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")

    itervalues() → [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")

    keys() → [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")

    obj = None

    setdefault(*key: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *default: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)") = None*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#DictAttribute.setdefault)

    values() → [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")

class celery.utils.collections.Evictable[[source]](../../_modules/celery/utils/collections.html#Evictable)
:   Mixin for classes supporting the `evict` method.

    exception Empty
    :   Exception raised by Queue.get(block=0)/get\_nowait().

    evict() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#Evictable.evict)
    :   Force evict until maxsize is enforced.

class celery.utils.collections.LimitedSet(*maxlen: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 0*, *expires: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") = 0*, *data: [Mapping](https://docs.python.org/dev/library/collections.abc.html#collections.abc.Mapping "(in Python v3.15)") = None*, *minlen: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 0*)[[source]](../../_modules/celery/utils/collections.html#LimitedSet)
:   Kind-of Set (or priority queue) with limitations.

    Good for when you need to test for membership (a in set),
    but the set should not grow unbounded.

    `maxlen` is enforced at all times, so if the limit is reached
    we’ll also remove non-expired items.

    You can also configure `minlen`: this is the minimal residual size
    of the set.

    All arguments are optional, and no limits are enabled by default.

    Parameters:
    :   - **maxlen** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – Optional max number of items.
          Adding more items than `maxlen` will result in immediate
          removal of items sorted by oldest insertion time.
        - **expires** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – TTL for all items.
          Expired items are purged as keys are inserted.
        - **minlen** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) –

          Minimal residual size of this set.
          .. versionadded:: 4.0

          Value must be less than `maxlen` if both are configured.

          Older expired items will be deleted, only after the set
          exceeds `minlen` number of items.
        - **data** (*Sequence*) – Initial data to initialize set with.
          Can be an iterable of `(key, value)` pairs,
          a dict (`{key: insertion_time}`), or another instance
          of [`LimitedSet`](#celery.utils.collections.LimitedSet "celery.utils.collections.LimitedSet").

    Example

    ```
    >>> s = LimitedSet(maxlen=50000, expires=3600, minlen=4000)
    >>> for i in range(60000):
    ...     s.add(i)
    ...     s.add(str(i))
    ...
    >>> 57000 in s  # last 50k inserted values are kept
    True
    >>> '10' in s  # '10' did expire and was purged from set.
    False
    >>> len(s)  # maxlen is reached
    50000
    >>> s.purge(now=time.monotonic() + 7200)  # clock + 2 hours
    >>> len(s)  # now only minlen items are cached
    4000
    >>>> 57000 in s  # even this item is gone now
    False
    ```

    add(*item: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *now: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") = None*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#LimitedSet.add)
    :   Add a new item, or reset the expiry time of an existing item.

    as\_dict() → [Dict](https://docs.python.org/dev/library/typing.html#typing.Dict "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#LimitedSet.as_dict)
    :   Whole set as serializable dictionary.

        Example

        ```
        >>> s = LimitedSet(maxlen=200)
        >>> r = LimitedSet(maxlen=200)
        >>> for i in range(500):
        ...     s.add(i)
        ...
        >>> r.update(s.as_dict())
        >>> r == s
        True
        ```

    clear() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#LimitedSet.clear)
    :   Clear all data, start from scratch again.

    discard(*item: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#LimitedSet.discard)

    max\_heap\_percent\_overload = 15

    pop(*default: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)") = None*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#LimitedSet.pop)
    :   Remove and return the oldest item, or `None` when empty.

    pop\_value(*item: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")

    purge(*now: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") = None*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#LimitedSet.purge)
    :   Check oldest items and remove them if needed.

        Parameters:
        :   **now** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time of purging – by default right now.
            This can be useful for unit testing.

    update(*other: [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#LimitedSet.update)
    :   Update this set from other LimitedSet, dict or iterable.

class celery.utils.collections.Messagebuffer(*maxsize: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*, *iterable: [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)") = None*, *deque: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)") = <class 'collections.deque'>*)[[source]](../../_modules/celery/utils/collections.html#Messagebuffer)
:   A buffer of pending messages.

    exception Empty
    :   Exception raised by Queue.get(block=0)/get\_nowait().

    extend(*it: [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#Messagebuffer.extend)

    put(*item: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#Messagebuffer.put)

    take(*\*default: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#Messagebuffer.take)

class celery.utils.collections.OrderedDict[[source]](../../_modules/celery/utils/collections.html#OrderedDict)
:   Dict where insertion order matters.

celery.utils.collections.force\_mapping(*m: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Mapping](https://docs.python.org/dev/library/collections.abc.html#collections.abc.Mapping "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#force_mapping)
:   Wrap object into supporting the mapping interface if necessary.

celery.utils.collections.lpmerge(*L: [Mapping](https://docs.python.org/dev/library/collections.abc.html#collections.abc.Mapping "(in Python v3.15)")*, *R: [Mapping](https://docs.python.org/dev/library/collections.abc.html#collections.abc.Mapping "(in Python v3.15)")*) → [Mapping](https://docs.python.org/dev/library/collections.abc.html#collections.abc.Mapping "(in Python v3.15)")[[source]](../../_modules/celery/utils/collections.html#lpmerge)
:   In place left precedent dictionary merge.

    Keeps values from L, if the value in R is `None`.