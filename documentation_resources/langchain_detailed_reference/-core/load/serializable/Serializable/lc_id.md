<!-- Source: https://reference.langchain.com/python/langchain-core/load/serializable/Serializable/lc_id -->

Methodv1.2.21 (latest)●Since v0.1

# lc\_id

Return a unique identifier for this class for serialization purposes.

The unique identifier is a list of strings that describes the path
to the object.

For example, for the class `langchain.llms.openai.OpenAI`, the id is
`["langchain", "llms", "openai", "OpenAI"]`.


```
lc_id(
    cls,
) -> list[str]
```


