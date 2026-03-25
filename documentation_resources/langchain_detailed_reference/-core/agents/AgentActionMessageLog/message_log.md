<!-- Source: https://reference.langchain.com/python/langchain-core/agents/AgentActionMessageLog/message_log -->

Attributev1.2.21 (latest)●Since v0.1

# message\_log

Similar to log, this can be used to pass along extra information about what exact
messages were predicted by the LLM before parsing out the `(tool, tool_input)`.

This is again useful if `(tool, tool_input)` cannot be used to fully recreate the
LLM prediction, and you need that LLM prediction (for future agent iteration).

Compared to `log`, this is useful when the underlying LLM is a chat model (and
therefore returns messages rather than a string).


```
message_log: Sequence[BaseMessage]
```


