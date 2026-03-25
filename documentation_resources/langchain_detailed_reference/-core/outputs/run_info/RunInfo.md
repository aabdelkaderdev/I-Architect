<!-- Source: https://reference.langchain.com/python/langchain-core/outputs/run_info/RunInfo -->

Classv1.2.21 (latest)●Since v0.1

# RunInfo

Class that contains metadata for a single execution of a chain or model.

Defined for backwards compatibility with older versions of `langchain_core`.

Users can acquire the `run_id` information from callbacks or via `run_id`
information present in the `astream_event` API (depending on the use case).


```
RunInfo()
```

## Bases

`BaseModel`

## Attributes

[attribute

run\_id: UUID

A unique identifier for the model or chain run.](/python/langchain-core/outputs/run_info/RunInfo/run_id)


