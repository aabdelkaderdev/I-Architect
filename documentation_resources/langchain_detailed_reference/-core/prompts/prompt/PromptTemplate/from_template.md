<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/prompt/PromptTemplate/from_template -->

Methodv1.2.21 (latest)●Since v0.1

# from\_template

Load a prompt template from a template.

Security

Prefer using `template_format='f-string'` instead of
`template_format='jinja2'`, or make sure to NEVER accept jinja2 templates
from untrusted sources as they may lead to arbitrary Python code execution.

As of LangChain 0.0.329, Jinja2 templates will be rendered using Jinja2's
SandboxedEnvironment by default. This sand-boxing should be treated as a
best-effort approach rather than a guarantee of security, as it is an
opt-out rather than opt-in approach.

Despite the sandboxing, we recommend to never use jinja2 templates from
untrusted sources.


```
from_template(
  cls,
  template: str,
  *,
  template_format: PromptTemplateFormat = 'f-string',
  partial_variables: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> PromptTemplate
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `template`\* | `str` | The template to load. |
| `template_format` | `PromptTemplateFormat` | Default:`'f-string'`  The format of the template.  Use `jinja2` for jinja2, `mustache` for mustache, and `f-string` for f-strings. |
| `partial_variables` | `dict[str, Any] | None` | Default:`None`  A dictionary of variables that can be used to partially fill in the template.  For example, if the template is `'{variable1} {variable2}'`, and `partial_variables` is `{"variable1": "foo"}`, then the final prompt will be `'foo {variable2}'`. |
| `**kwargs` | `Any` | Default:`{}`  Any other arguments to pass to the prompt template. |


