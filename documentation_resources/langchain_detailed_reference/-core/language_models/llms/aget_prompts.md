<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/llms/aget_prompts -->

Functionv1.2.21 (latest)●Since v0.1

# aget\_prompts

Get prompts that are already cached. Async version.


```
aget_prompts(
  params: dict[str, Any],
  prompts: list[str],
  cache: BaseCache | bool | None = None
) -> tuple[dict[int, list], str, list[int], list[str]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `params`\* | `dict[str, Any]` | Dictionary of parameters. |
| `prompts`\* | `list[str]` | List of prompts. |
| `cache` | `BaseCache | bool | None` | Default:`None`  Cache object. |


