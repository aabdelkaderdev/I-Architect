<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/json_chat/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

## Attributes

[attribute

TEMPLATE\_TOOL\_RESPONSE: str](/python/langchain-classic/agents/json_chat/prompt/TEMPLATE_TOOL_RESPONSE)

## Functions

[function

format\_log\_to\_messages

Construct the scratchpad that lets the agent continue its thought process.](/python/langchain-classic/agents/format_scratchpad/log_to_messages/format_log_to_messages)[function

create\_json\_chat\_agent

Create an agent that uses JSON to format its logic, build for Chat Models.](/python/langchain-classic/agents/json_chat/base/create_json_chat_agent)

## Classes

[class

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


