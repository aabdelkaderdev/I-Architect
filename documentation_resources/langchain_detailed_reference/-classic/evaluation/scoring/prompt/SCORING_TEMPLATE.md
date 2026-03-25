<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/scoring/prompt/SCORING_TEMPLATE -->

Attributev1.2.13 (latest)●Since v1.0

# SCORING\_TEMPLATE


```
SCORING_TEMPLATE = ChatPromptTemplate.from_messages(
  [('system', SYSTEM_MESSAGE), ('human', '[Instruction]\nPlease act as an impartial judge and evaluate the quality of the response provided by an AI assistant to the user question displayed below. {criteria}Begin your evaluation by providing a short explanation. Be as objective as possible. After providing your explanation, you must rate the response on a scale of 1 to 10 by strictly following this format: "[[rating]]", for example: "Rating: [[5]]".\n\n[Question]\n{input}\n\n[The Start of Assistant\'s Answer]\n{prediction}\n[The End of Assistant\'s Answer]')]
)
```


