<!-- Source: https://reference.langchain.com/python/langchain-core/utils/utils/LC_ID_PREFIX -->

Attributev1.2.21 (latest)●Since v1.0

# LC\_ID\_PREFIX

Internal tracing/callback system identifier.

Used for:

- Tracing. Every LangChain operation (LLM call, chain execution, tool use, etc.)
  gets a unique run\_id (UUID)
- Enables tracking parent-child relationships between operations


```
LC_ID_PREFIX = 'lc_run-'
```


