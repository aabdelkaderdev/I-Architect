<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/string/mustache_template_vars -->

Functionv1.2.21 (latest)●Since v0.1

# mustache\_template\_vars

Get the top-level variables from a mustache template.

For nested variables like `{{person.name}}`, only the top-level key (`person`) is
returned.


```
mustache_template_vars(
    template: str,
) -> set[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `template`\* | `str` | The template string. |


