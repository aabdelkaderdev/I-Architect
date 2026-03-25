<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/conversational_chat/prompt/FORMAT_INSTRUCTIONS -->

Attributev1.2.13 (latest)●Since v1.0

# FORMAT\_INSTRUCTIONS


```
FORMAT_INSTRUCTIONS = 'RESPONSE FORMAT INSTRUCTIONS\n----------------------------\n\nWhen responding to me, please output a response in one of two formats:\n\n**Option 1:**\nUse this if you want the human to use a tool.\nMarkdown code snippet formatted in the following schema:\n\n```json\n{{{{\n    "action": string, \\\\ The action to take. Must be one of {tool_names}\n    "action_input": string \\\\ The input to the action\n}}}}\n```\n\n**Option #2:**\nUse this if you want to respond directly to the human. Markdown code snippet formatted in the following schema:\n\n```json\n{{{{\n    "action": "Final Answer",\n    "action_input": string \\\\ You should put what you want to return to use here\n}}}}\n```'
```


