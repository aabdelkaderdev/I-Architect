<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/conversational_chat/prompt/SUFFIX -->

Attributev1.2.13 (latest)●Since v1.0

# SUFFIX


```
SUFFIX = "TOOLS\n------\nAssistant can ask the user to use tools to look up information that may be helpful in answering the users original question. The tools the human can use are:\n\n{{tools}}\n\n{format_instructions}\n\nUSER'S INPUT\n--------------------\nHere is the user's input (
  remember to respond with a markdown code snippet of a json blob with a single action,
  and NOTHING else
):\n\n{{{{input}}}}"
```


