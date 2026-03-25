<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/base/BasePromptTemplate/partial_variables -->

Attributev1.2.21 (latest)●Since v0.1

# partial\_variables

A dictionary of the partial variables the prompt template carries.

Partial variables populate the template so that you don't need to pass them in every
time you call the prompt.


```
partial_variables: Mapping[str, Any] = Field(default_factory=dict)
```


