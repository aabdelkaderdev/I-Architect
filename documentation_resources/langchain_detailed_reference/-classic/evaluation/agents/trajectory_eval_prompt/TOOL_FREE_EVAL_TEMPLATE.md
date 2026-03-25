<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/agents/trajectory_eval_prompt/TOOL_FREE_EVAL_TEMPLATE -->

Attributev1.2.13 (latest)●Since v1.0

# TOOL\_FREE\_EVAL\_TEMPLATE


```
TOOL_FREE_EVAL_TEMPLATE = "An AI language model has been given access to a set of tools to help answer a user's question.\n\nThe question the human asked the AI model was:\n[QUESTION]\n{question}\n[END_QUESTION]{reference}\n\nThe AI language model decided to use the following set of tools to answer the question:\n[AGENT_TRAJECTORY]\n{agent_trajectory}\n[END_AGENT_TRAJECTORY]\n\nThe AI language model's final answer to the question was:\n[RESPONSE]\n{answer}\n[END_RESPONSE]\n\nLet's to do a detailed evaluation of the AI language model's answer step by step.\n\nWe consider the following criteria before giving a score from 1 to 5:\n\ni. Is the final answer helpful?\nii. Does the AI language use a logical sequence of tools to answer the question?\niii. Does the AI language model use the tools in a helpful way?\niv. Does the AI language model use too many steps to answer the question?\nv. Are the appropriate tools used to answer the question?"
```


