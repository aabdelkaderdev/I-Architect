<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/string/get_template_variables -->

Functionv1.2.21 (latest)●Since v0.1

# get\_template\_variables

Get the variables from the template.


```
get_template_variables(
    template: str,
    template_format: str,
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `template`\* | `str` | The template string. |
| `template_format`\* | `str` | The template format.  Should be one of `'f-string'`, `'mustache'` or `'jinja2'`. |


