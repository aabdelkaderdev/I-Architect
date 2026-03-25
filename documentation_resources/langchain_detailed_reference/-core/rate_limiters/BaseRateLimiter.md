<!-- Source: https://reference.langchain.com/python/langchain-core/rate_limiters/BaseRateLimiter -->

Classv1.2.21 (latest)●Since v0.2

# BaseRateLimiter

Base class for rate limiters.

Usage of the base limiter is through the acquire and aacquire methods depending
on whether running in a sync or async context.

Implementations are free to add a timeout parameter to their initialize method
to allow users to specify a timeout for acquiring the necessary tokens when
using a blocking call.

Current limitations:

- Rate limiting information is not surfaced in tracing or callbacks. This means
  that the total time it takes to invoke a chat model will encompass both
  the time spent waiting for tokens and the time spent making the request.


```
BaseRateLimiter()
```

## Bases

`abc.ABC`

## Methods

[method

acquire

Attempt to acquire the necessary tokens for the rate limiter.

This method blocks until the required tokens are available if `blocking`
is set to `True`.

If `blocking` is set to `False`, the method will immediately return the result
of the attempt to acquire the tokens.](/python/langchain-core/rate_limiters/BaseRateLimiter/acquire)[method

aacquire

Attempt to acquire the necessary tokens for the rate limiter.

This method blocks until the required tokens are available if `blocking`
is set to `True`.

If `blocking` is set to `False`, the method will immediately return the result
of the attempt to acquire the tokens.](/python/langchain-core/rate_limiters/BaseRateLimiter/aacquire)


