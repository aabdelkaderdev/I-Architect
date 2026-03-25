<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/AgentExecutor/handle_parsing_errors -->

Attributev1.2.13 (latest)●Since v1.0

# handle\_parsing\_errors

How to handle errors raised by the agent's output parser.
Defaults to `False`, which raises the error.
If `true`, the error will be sent back to the LLM as an observation.
If a string, the string itself will be sent to the LLM as an observation.
If a callable function, the function will be called with the exception as an
argument, and the result of that function will be passed to the agent as an
observation.


```
handle_parsing_errors: bool | str | Callable[[OutputParserException], str] = False
```


