<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/llms/aupdate_cache -->

Functionv1.2.21 (latest)●Since v0.1

# aupdate\_cache

Update the cache and get the LLM output. Async version.


```
aupdate_cache(
  cache: BaseCache | bool | None,
  existing_prompts: dict[int, list],
  llm_string: str,
  missing_prompt_idxs: list[int],
  new_results: LLMResult,
  prompts: list[str]
) -> dict | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `cache`\* | `BaseCache | bool | None` | Cache object. |
| `existing_prompts`\* | `dict[int, list]` | Dictionary of existing prompts. |
| `llm_string`\* | `str` | LLM string. |
| `missing_prompt_idxs`\* | `list[int]` | List of missing prompt indexes. |
| `new_results`\* | `LLMResult` | LLMResult object. |
| `prompts`\* | `list[str]` | List of prompts. |


