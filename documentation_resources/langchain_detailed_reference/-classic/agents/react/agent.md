<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/react/agent -->

Modulev1.2.13 (latest)●Since v1.0

# agent

## Functions

[function

format\_log\_to\_str

Construct the scratchpad that lets the agent continue its thought process.](/python/langchain-classic/agents/format_scratchpad/log/format_log_to_str)[function

create\_react\_agent

Create an agent that uses ReAct prompting.

Based on paper "ReAct: Synergizing Reasoning and Acting in Language Models"
(<https://arxiv.org/abs/2210.03629>)

Warning

This implementation is based on the foundational ReAct paper but is older and
not well-suited for production applications.

For a more robust and feature-rich implementation, we recommend using the
`create_agent` function from the `langchain` library.

See the
[reference doc](https://reference.langchain.com/python/langchain/agents/)
for more information.](/python/langchain-classic/agents/react/agent/create_react_agent)

## Classes

[class

AgentOutputParser

Base class for parsing agent output into agent action/finish.](/python/langchain-classic/agents/agent/AgentOutputParser)[class

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
```](/python/langchain-classic/agents/output_parsers/react_single_input/ReActSingleInputOutputParser)


