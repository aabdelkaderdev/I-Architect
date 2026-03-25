<!-- Source: https://reference.langchain.com/python/langchain-core/agents/AgentAction/log -->

Attributev1.2.21 (latest)●Since v0.1

# log

Additional information to log about the action.

This log can be used in a few ways. First, it can be used to audit what exactly the
LLM predicted to lead to this `(tool, tool_input)`.

Second, it can be used in future iterations to show the LLMs prior thoughts. This is
useful when `(tool, tool_input)` does not contain full information about the LLM
prediction (for example, any `thought` before the tool/tool\_input).


```
log: str
```


