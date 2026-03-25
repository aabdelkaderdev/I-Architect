<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/comparison/prompt/COMPARISON_TEMPLATE_WITH_REFERENCE -->

Attributev1.2.13 (latest)●Since v1.0

# COMPARISON\_TEMPLATE\_WITH\_REFERENCE


```
COMPARISON_TEMPLATE_WITH_REFERENCE = ChatPromptTemplate.from_messages(
  [('system', SYSTEM_MESSAGE), ('human', "{criteria}\n\nTo help you evaluate the responses, here is a reference answer to the user's question:\n{reference}[User Question]\n{input}\n\n[The Start of Assistant A's Answer]\n{prediction}\n[The End of Assistant A's Answer]\n\n[The Start of Assistant B's Answer]\n{prediction_b}\n[The End of Assistant B's Answer]")]
)
```


