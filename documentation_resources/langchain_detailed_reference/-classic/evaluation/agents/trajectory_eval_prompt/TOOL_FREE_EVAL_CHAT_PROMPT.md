<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/agents/trajectory_eval_prompt/TOOL_FREE_EVAL_CHAT_PROMPT -->

Attributev1.2.13 (latest)●Since v1.0

# TOOL\_FREE\_EVAL\_CHAT\_PROMPT


```
TOOL_FREE_EVAL_CHAT_PROMPT = ChatPromptTemplate.from_messages(
  messages=[SystemMessage(content='You are a helpful assistant that evaluates language models.'), HumanMessage(content=EXAMPLE_INPUT), AIMessage(content=EXAMPLE_OUTPUT), HumanMessagePromptTemplate.from_template(TOOL_FREE_EVAL_TEMPLATE)]
)
```


