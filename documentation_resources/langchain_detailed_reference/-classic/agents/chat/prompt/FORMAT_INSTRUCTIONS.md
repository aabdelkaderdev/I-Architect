<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/chat/prompt/FORMAT_INSTRUCTIONS -->

Attributev1.2.13 (latest)●Since v1.0

# FORMAT\_INSTRUCTIONS


```
FORMAT_INSTRUCTIONS = 'The way you use the tools is by specifying a json blob.\nSpecifically, this json should have a `action` key (
  with the name of the tool to use) and a `action_input` key (with the input to the tool going here).\n\nThe only values that should be in the "action" field are: {tool_names}\n\nThe $JSON_BLOB should only contain a SINGLE action, do NOT return a list of multiple actions. Here is an example of a valid $JSON_BLOB:\n\n```\n{{{{\n  "action": $TOOL_NAME,\n  "action_input": $INPUT\n}}}}\n```\n\nALWAYS use the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction:\n```\n$JSON_BLOB\n```\nObservation: the result of the action\n... (this Thought/Action/Observation can repeat N times
)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question'
```


