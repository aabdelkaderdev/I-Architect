<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/agents/trajectory_eval_prompt/EVAL_CHAT_PROMPT -->

Attributev1.2.13 (latest)●Since v1.0

# EVAL\_CHAT\_PROMPT


```
EVAL_CHAT_PROMPT = ChatPromptTemplate.from_messages(
  messages=[SystemMessage(content='You are a helpful assistant that evaluates language models.'), HumanMessage(content=EXAMPLE_INPUT), AIMessage(content=EXAMPLE_OUTPUT), HumanMessagePromptTemplate.from_template(EVAL_TEMPLATE)]
)
```


