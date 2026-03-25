<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/entity/ConversationEntityMemory/load_memory_variables -->

Methodv1.2.13 (latest)●Since v1.0

# load\_memory\_variables

Load memory variables.

Returns chat history and all generated entities with summaries if available,
and updates or clears the recent entity cache.

New entity name can be found when calling this method, before the entity
summaries are generated, so the entity cache values may be empty if no entity
descriptions are generated yet.


```
load_memory_variables(
    self,
    inputs: dict[str, Any],
) -> dict[str, Any]
```


