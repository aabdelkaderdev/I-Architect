<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/llms/BaseLLM/save -->

Methodv1.2.21 (latest)●Since v0.1

# save

Save the LLM.


```
save(
    self,
    file_path: Path | str,
) -> None
```

**Example:**

```
llm.save(file_path="path/llm.yaml")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `file_path`\* | `Path | str` | Path to file to save the LLM to. |


