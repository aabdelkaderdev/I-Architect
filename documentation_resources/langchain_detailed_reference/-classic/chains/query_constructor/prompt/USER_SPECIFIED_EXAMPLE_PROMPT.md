<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/query_constructor/prompt/USER_SPECIFIED_EXAMPLE_PROMPT -->

Attributev1.2.13 (latest)●Since v1.0

# USER\_SPECIFIED\_EXAMPLE\_PROMPT


```
USER_SPECIFIED_EXAMPLE_PROMPT = PromptTemplate.from_template(
  '<< Example {i}. >>\nUser Query:\n{user_query}\n\nStructured Request:\n```json\n{structured_request}\n```\n'
)
```


