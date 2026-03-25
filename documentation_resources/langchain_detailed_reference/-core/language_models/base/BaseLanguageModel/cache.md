<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/base/BaseLanguageModel/cache -->

Attributev1.2.21 (latest)●Since v0.1

# cache

Whether to cache the response.

- If `True`, will use the global cache.
- If `False`, will not use a cache
- If `None`, will use the global cache if it's set, otherwise no cache.
- If instance of `BaseCache`, will use the provided cache.

Caching is not currently supported for streaming methods of models.


```
cache: BaseCache | bool | None = Field(default=None, exclude=True)
```


