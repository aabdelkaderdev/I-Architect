<!-- Source: https://reference.langchain.com/python/langchain-core/load/load/InitValidator -->

Attributev1.2.21 (latest)●Since v0.3

# InitValidator

Type alias for a callable that validates kwargs during deserialization.

The callable receives:

- `class_path`: A tuple of strings identifying the class being instantiated
  (e.g., `('langchain', 'schema', 'messages', 'AIMessage')`).
- `kwargs`: The kwargs dict that will be passed to the constructor.

The validator should raise an exception if the object should not be deserialized.


```
InitValidator = Callable[[tuple[str, ...], dict[str, Any]], None]
```


