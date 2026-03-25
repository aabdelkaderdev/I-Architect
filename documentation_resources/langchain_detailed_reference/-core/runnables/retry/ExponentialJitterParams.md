<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/retry/ExponentialJitterParams -->

Classv1.2.21 (latest)●Since v0.3

# ExponentialJitterParams

Parameters for `tenacity.wait_exponential_jitter`.


```
ExponentialJitterParams()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| initial | [float](https://docs.python.org/3/library/functions.html#float) |
| max | [float](https://docs.python.org/3/library/functions.html#float) |
| exp\_base | [float](https://docs.python.org/3/library/functions.html#float) |
| jitter | [float](https://docs.python.org/3/library/functions.html#float) |

## Attributes

[attribute

initial: float

Initial wait.](/python/langchain-core/runnables/retry/ExponentialJitterParams/initial)[attribute

max: float

Maximum wait.](/python/langchain-core/runnables/retry/ExponentialJitterParams/max)[attribute

exp\_base: float

Base for exponential backoff.](/python/langchain-core/runnables/retry/ExponentialJitterParams/exp_base)[attribute

jitter: float

Random additional wait sampled from random.uniform(0, jitter).](/python/langchain-core/runnables/retry/ExponentialJitterParams/jitter)


