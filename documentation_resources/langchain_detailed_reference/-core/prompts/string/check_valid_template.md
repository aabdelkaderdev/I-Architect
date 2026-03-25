<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/string/check_valid_template -->

Functionv1.2.21 (latest)●Since v0.1

# check\_valid\_template

Check that template string is valid.


```
check_valid_template(
  template: str,
  template_format: str,
  input_variables: list[str]
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `template`\* | `str` | The template string. |
| `template_format`\* | `str` | The template format.  Should be one of `'f-string'` or `'jinja2'`. |
| `input_variables`\* | `list[str]` | The input variables. |


