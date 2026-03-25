<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/entity/ConversationEntityMemory/save_context -->

Methodv1.2.13 (latest)●Since v1.0

# save\_context

Save context from this conversation history to the entity store.

Generates a summary for each entity in the entity cache by prompting
the model, and saves these summaries to the entity store.


```
save_context(
  self,
  inputs: dict[str, Any],
  outputs: dict[str, str]
) -> None
```


