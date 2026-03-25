<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/stuff/StuffDocumentsChain/get_default_document_variable_name -->

Methodv1.2.13 (latest)●Since v1.0

# get\_default\_document\_variable\_name

Get default document variable name, if not provided.

If only one variable is present in the llm\_chain.prompt,
we can infer that the formatted documents should be passed in
with this variable name.


```
get_default_document_variable_name(
    cls,
    values: dict,
) -> Any
```


