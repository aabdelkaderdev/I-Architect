<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/conversational/prompt/FORMAT_INSTRUCTIONS -->

Attributev1.2.13 (latest)●Since v1.0

# FORMAT\_INSTRUCTIONS


```
FORMAT_INSTRUCTIONS = 'To use a tool, please use the following format:\n\n```\nThought: Do I need to use a tool? Yes\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n```\n\nWhen you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:\n\n```\nThought: Do I need to use a tool? No\n{ai_prefix}: [your response here]\n```'
```


