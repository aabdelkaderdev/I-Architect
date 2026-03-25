<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate/from_template -->

Methodv1.2.21 (latest)●Since v0.1

# from\_template

Create a class from a string template.


```
from_template(
  cls,
  template: str,
  template_format: PromptTemplateFormat = 'f-string',
  partial_variables: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> Self
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `template`\* | `str` | a template. |
| `template_format` | `PromptTemplateFormat` | Default:`'f-string'`  format of the template. |
| `partial_variables` | `dict[str, Any] | None` | Default:`None`  A dictionary of variables that can be used to partially fill in the template.  For example, if the template is `"{variable1} {variable2}"`, and `partial_variables` is `{"variable1": "foo"}`, then the final prompt will be `"foo {variable2}"`. |
| `**kwargs` | `Any` | Default:`{}`  Keyword arguments to pass to the constructor. |


