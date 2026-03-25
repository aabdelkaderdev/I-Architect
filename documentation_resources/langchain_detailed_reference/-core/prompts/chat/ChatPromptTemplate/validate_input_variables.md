<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate/validate_input_variables -->

Methodv1.2.21 (latest)●Since v0.1

# validate\_input\_variables

Validate input variables.

If `input_variables` is not set, it will be set to the union of all input
variables in the messages.


```
validate_input_variables(
    cls,
    values: dict,
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `values`\* | `dict` | values to validate. |


