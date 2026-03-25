<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/output_parsers/json -->

Modulev1.2.13 (latest)●Since v1.0

# json

## Attributes

[attribute

logger](/python/langchain-classic/agents/output_parsers/json/logger)

## Classes

[class

AgentOutputParser

Base class for parsing agent output into agent action/finish.](/python/langchain-classic/agents/agent/AgentOutputParser)[class

JSONAgentOutputParser

Parses tool invocations and final answers in JSON format.

Expects output to be in one of two formats.

If the output signals that an action should be taken,
should be in the below format. This will result in an AgentAction
being returned.

```
{"action": "search", "action_input": "2+2"}
```

If the output signals that a final answer should be given,
should be in the below format. This will result in an AgentFinish
being returned.

```
{"action": "Final Answer", "action_input": "4"}
```](/python/langchain-classic/agents/output_parsers/json/JSONAgentOutputParser)


