<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/string/validate_jinja2 -->

Functionv1.2.21 (latest)●Since v0.1

# validate\_jinja2

Validate that the input variables are valid for the template.

Issues a warning if missing or extra variables are found.


```
validate_jinja2(
    template: str,
    input_variables: list[str],
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `template`\* | `str` | The template string. |
| `input_variables`\* | `list[str]` | The input variables. |


