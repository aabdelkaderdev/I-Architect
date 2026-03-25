<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/query_constructor/prompt/DEFAULT_SUFFIX -->

Attributev1.2.13 (latest)●Since v1.0

# DEFAULT\_SUFFIX


```
DEFAULT_SUFFIX = '<
  < Example {i}. >
>\nData Source:\n```json\n{{{{\n    "content": "{content}",\n    "attributes": {attributes}\n}}}}\n```\n\nUser Query:\n{{query}}\n\nStructured Request:\n'
```


