<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/string/jinja2_formatter -->

Functionv1.2.21 (latest)●Since v0.1

# jinja2\_formatter

Format a template using jinja2.

Security

As of LangChain 0.0.329, this method uses Jinja2's `SandboxedEnvironment` by
default. However, this sandboxing should be treated as a best-effort approach
rather than a guarantee of security.

Do not accept jinja2 templates from untrusted sources as they may lead
to arbitrary Python code execution.

[More information.](https://jinja.palletsprojects.com/en/3.1.x/sandbox/)


```
jinja2_formatter(
    template: str,
    ,
    **kwargs: Any = {},
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `template`\* | `str` | The template string. |
| `**kwargs` | `Any` | Default:`{}`  The variables to format the template with. |


