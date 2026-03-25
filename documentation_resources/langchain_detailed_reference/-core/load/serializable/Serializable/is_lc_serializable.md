<!-- Source: https://reference.langchain.com/python/langchain-core/load/serializable/Serializable/is_lc_serializable -->

Methodv1.2.21 (latest)●Since v0.1

# is\_lc\_serializable

Is this class serializable?

By design, even if a class inherits from `Serializable`, it is not serializable
by default. This is to prevent accidental serialization of objects that should
not be serialized.


```
is_lc_serializable(
    cls,
) -> bool
```


