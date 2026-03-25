<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/comparison/prompt/COMPARISON_TEMPLATE -->

Attributev1.2.13 (latest)●Since v1.0

# COMPARISON\_TEMPLATE


```
COMPARISON_TEMPLATE = ChatPromptTemplate.from_messages(
  [('system', SYSTEM_MESSAGE), ('human', "{criteria}[User Question]\n{input}\n\n[The Start of Assistant A's Answer]\n{prediction}\n[The End of Assistant A's Answer]\n\n[The Start of Assistant B's Answer]\n{prediction_b}\n[The End of Assistant B's Answer]")]
)
```


