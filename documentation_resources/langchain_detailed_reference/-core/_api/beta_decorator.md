<!-- Source: https://reference.langchain.com/python/langchain-core/_api/beta_decorator -->

Modulev1.2.21 (latest)●Since v0.1

# beta\_decorator

Helper functions for marking parts of the LangChain API as beta.

This module was loosely adapted from matplotlib's [`_api/deprecation.py`](https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/_api/deprecation.py)
module.

Warning

This module is for internal use only. Do not use it in your own code. We may change
the API at any time with no warning.

## Attributes

[attribute

T](/python/langchain-core/_api/beta_decorator/T)

## Functions

[function

is\_caller\_internal

Return whether the caller at `depth` of this function is internal.](/python/langchain-core/_api/internal/is_caller_internal)[function

beta

Decorator to mark a function, a class, or a property as beta.

When marking a classmethod, a staticmethod, or a property, the `@beta` decorator
should go *under* `@classmethod` and `@staticmethod` (i.e., `beta` should directly
decorate the underlying callable), but *over* `@property`.

When marking a class `C` intended to be used as a base class in a multiple
inheritance hierarchy, `C` *must* define an `__init__` method (if `C` instead
inherited its `__init__` from its own base class, then `@beta` would mess up
`__init__` inheritance when installing its own (annotation-emitting) `C.__init__`).](/python/langchain-core/_api/beta_decorator/beta)[function

suppress\_langchain\_beta\_warning

Context manager to suppress `LangChainDeprecationWarning`.](/python/langchain-core/_api/beta_decorator/suppress_langchain_beta_warning)[function

warn\_beta

Display a standardized beta annotation.](/python/langchain-core/_api/beta_decorator/warn_beta)[function

surface\_langchain\_beta\_warnings

Unmute LangChain beta warnings.](/python/langchain-core/_api/beta_decorator/surface_langchain_beta_warnings)

## Classes

[class

LangChainBetaWarning

A class for issuing beta warnings for LangChain users.](/python/langchain-core/_api/beta_decorator/LangChainBetaWarning)


