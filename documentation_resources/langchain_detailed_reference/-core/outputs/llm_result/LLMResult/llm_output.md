<!-- Source: https://reference.langchain.com/python/langchain-core/outputs/llm_result/LLMResult/llm_output -->

Attributev1.2.21 (latest)●Since v0.1

# llm\_output

For arbitrary model provider-specific output.

This dictionary is a free-form dictionary that can contain any information that the
provider wants to return. It is not standardized and keys may vary by provider and
over time.

Users should generally avoid relying on this field and instead rely on accessing
relevant information from standardized fields present in AIMessage.


```
llm_output: dict | None = None
```


