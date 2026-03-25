<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/question_answering/refine_prompts/CHAT_REFINE_PROMPT -->

Attributev1.2.13 (latest)●Since v1.0

# CHAT\_REFINE\_PROMPT


```
CHAT_REFINE_PROMPT = ChatPromptTemplate.from_messages(
  [('human', '{question}'), ('ai', '{existing_answer}'), ('human', refine_template)]
)
```


