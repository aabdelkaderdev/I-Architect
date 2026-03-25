<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/structured_chat/prompt/FORMAT_INSTRUCTIONS -->

Attributev1.2.13 (latest)●Since v1.0

# FORMAT\_INSTRUCTIONS


```
FORMAT_INSTRUCTIONS = 'Use a json blob to specify a tool by providing an action key (
  tool name) and an action_input key (tool input).\n\nValid "action" values: "Final Answer" or {tool_names}\n\nProvide only ONE action per $JSON_BLOB, as shown:\n\n```\n{{{{\n  "action": $TOOL_NAME,\n  "action_input": $INPUT\n}}}}\n```\n\nFollow this format:\n\nQuestion: input question to answer\nThought: consider previous and subsequent steps\nAction:\n```\n$JSON_BLOB\n```\nObservation: action result\n... (repeat Thought/Action/Observation N times
)\nThought: I know what to respond\nAction:\n```\n{{{{\n  "action": "Final Answer",\n  "action_input": "Final response to human"\n}}}}\n```'
```


