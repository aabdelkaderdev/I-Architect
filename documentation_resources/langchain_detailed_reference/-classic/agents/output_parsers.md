<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/output_parsers -->

Modulev1.2.13 (latest)●Since v1.0

# output\_parsers

Parsing utils to go from string to AgentAction or Agent Finish.

AgentAction means that an action should be taken.
This contains the name of the tool to use, the input to pass to that tool,
and a `log` variable (which contains a log of the agent's thinking).

AgentFinish means that a response should be given.
This contains a `return_values` dictionary. This usually contains a
single `output` key, but can be extended to contain more.
This also contains a `log` variable (which contains a log of the agent's thinking).

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
```](/python/langchain-classic/agents/output_parsers/json/JSONAgentOutputParser)[class

OpenAIFunctionsAgentOutputParser

Parses a message into agent action/finish.

Is meant to be used with OpenAI models, as it relies on the specific
function\_call parameter from OpenAI to convey what tools to use.

If a function\_call parameter is passed, then that is used to get
the tool and tool input.

If one is not passed, then the AIMessage is assumed to be the final output.](/python/langchain-classic/agents/output_parsers/openai_functions/OpenAIFunctionsAgentOutputParser)[class

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
```](/python/langchain-classic/agents/output_parsers/react_json_single_input/ReActJsonSingleInputOutputParser)[class

ReActSingleInputOutputParser

Parses ReAct-style LLM calls that have a single tool input.

Expects output to be in one of two formats.

If the output signals that an action should be taken,
should be in the below format. This will result in an AgentAction
being returned.

```
Thought: agent thought here
Action: search
Action Input: what is the temperature in SF?
```

If the output signals that a final answer should be given,
should be in the below format. This will result in an AgentFinish
being returned.

```
Thought: agent thought here
Final Answer: The temperature is 100 degrees
```](/python/langchain-classic/agents/output_parsers/react_single_input/ReActSingleInputOutputParser)[class

SelfAskOutputParser

Parses self-ask style LLM calls.

Expects output to be in one of two formats.

If the output signals that an action should be taken,
should be in the below format. This will result in an AgentAction
being returned.

```
Thoughts go here...
Follow up: what is the temperature in SF?
```

If the output signals that a final answer should be given,
should be in the below format. This will result in an AgentFinish
being returned.

```
Thoughts go here...
So the final answer is: The temperature is 100 degrees
```](/python/langchain-classic/agents/output_parsers/self_ask/SelfAskOutputParser)[class

ToolsAgentOutputParser

Parses a message into agent actions/finish.

If a tool\_calls parameter is passed, then that is used to get
the tool names and tool inputs.

If one is not passed, then the AIMessage is assumed to be the final output.](/python/langchain-classic/agents/output_parsers/tools/ToolsAgentOutputParser)[class

XMLAgentOutputParser

Parses tool invocations and final answers from XML-formatted agent output.

This parser extracts structured information from XML tags to determine whether
an agent should perform a tool action or provide a final answer. It includes
built-in escaping support to safely handle tool names and inputs
containing XML special characters.](/python/langchain-classic/agents/output_parsers/xml/XMLAgentOutputParser)

## Modules

[module

react\_json\_single\_input](/python/langchain-classic/agents/output_parsers/react_json_single_input)[module

self\_ask](/python/langchain-classic/agents/output_parsers/self_ask)[module

json](/python/langchain-classic/agents/output_parsers/json)[module

openai\_tools](/python/langchain-classic/agents/output_parsers/openai_tools)[module

react\_single\_input](/python/langchain-classic/agents/output_parsers/react_single_input)[module

tools](/python/langchain-classic/agents/output_parsers/tools)[module

openai\_functions](/python/langchain-classic/agents/output_parsers/openai_functions)[module

xml](/python/langchain-classic/agents/output_parsers/xml)


