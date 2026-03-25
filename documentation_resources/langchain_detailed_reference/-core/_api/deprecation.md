<!-- Source: https://reference.langchain.com/python/langchain-core/_api/deprecation -->

Modulev1.2.21 (latest)●Since v0.1

# deprecation

Helper functions for deprecating parts of the LangChain API.

This module was adapted from matplotlib's [`_api/deprecation.py`](https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/_api/deprecation.py)
module.

Warning

This module is for internal use only. Do not use it in your own code. We may change
the API at any time with no warning.

## Attributes

[attribute

T](/python/langchain-core/_api/deprecation/T)

## Functions

[function

is\_caller\_internal

Return whether the caller at `depth` of this function is internal.](/python/langchain-core/_api/internal/is_caller_internal)[function

deprecated

Decorator to mark a function, a class, or a property as deprecated.

When deprecating a classmethod, a staticmethod, or a property, the `@deprecated`
decorator should go *under* `@classmethod` and `@staticmethod` (i.e., `deprecated`
should directly decorate the underlying callable), but *over* `@property`.

When deprecating a class `C` intended to be used as a base class in a multiple
inheritance hierarchy, `C` *must* define an `__init__` method (if `C` instead
inherited its `__init__` from its own base class, then `@deprecated` would mess up
`__init__` inheritance when installing its own (deprecation-emitting) `C.__init__`).

Parameters are the same as for `warn_deprecated`, except that *obj\_type* defaults to
'class' if decorating a class, 'attribute' if decorating a property, and 'function'
otherwise.](/python/langchain-core/_api/deprecation/deprecated)[function

suppress\_langchain\_deprecation\_warning

Context manager to suppress `LangChainDeprecationWarning`.](/python/langchain-core/_api/deprecation/suppress_langchain_deprecation_warning)[function

warn\_deprecated

Display a standardized deprecation.](/python/langchain-core/_api/deprecation/warn_deprecated)[function

surface\_langchain\_deprecation\_warnings

Unmute LangChain deprecation warnings.](/python/langchain-core/_api/deprecation/surface_langchain_deprecation_warnings)[function

rename\_parameter

Decorator indicating that parameter *old* of *func* is renamed to *new*.

The actual implementation of *func* should use *new*, not *old*. If *old* is passed
to *func*, a `DeprecationWarning` is emitted, and its value is used, even if *new*
is also passed by keyword.](/python/langchain-core/_api/deprecation/rename_parameter)

## Classes

[class

LangChainDeprecationWarning

A class for issuing deprecation warnings for LangChain users.](/python/langchain-core/_api/deprecation/LangChainDeprecationWarning)[class

LangChainPendingDeprecationWarning

A class for issuing deprecation warnings for LangChain users.](/python/langchain-core/_api/deprecation/LangChainPendingDeprecationWarning)


