<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/output_parsers/react_json_single_input -->

Modulev1.2.13 (latest)●Since v1.0

# react\_json\_single\_input

## Attributes

[attribute

FORMAT\_INSTRUCTIONS: str](/python/langchain-classic/agents/chat/prompt/FORMAT_INSTRUCTIONS)[attribute

FINAL\_ANSWER\_ACTION: str](/python/langchain-classic/agents/output_parsers/react_json_single_input/FINAL_ANSWER_ACTION)

## Classes

[class

AgentOutputParser

Base class for parsing agent output into agent action/finish.](/python/langchain-classic/agents/agent/AgentOutputParser)[class

ReActJsonSingleInputOutputParser

Parses ReAct-style LLM calls that have a single tool input in json format.

Expects output to be in one of two formats.

If the output signals that an action should be taken,
should be in the below format. This will result in an AgentAction
being returned.

```
Thought: agent thought here
Action:
```

{
"action": "search",
"action\_input": "what is the temperature in SF"
}

If the output signals that a final answer should be given,
should be in the below format. This will result in an AgentFinish
being returned.

```
Thought: agent thought here
Final Answer: The temperature is 100 degrees
```](/python/langchain-classic/agents/output_parsers/react_json_single_input/ReActJsonSingleInputOutputParser)


