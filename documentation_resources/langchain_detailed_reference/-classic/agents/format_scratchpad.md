<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/format_scratchpad -->

Modulev1.2.13 (latest)●Since v1.0

# format\_scratchpad

Logic for formatting intermediate steps into an agent scratchpad.

Intermediate steps refers to the list of (AgentAction, observation) tuples
that result from previous iterations of the agent.
Depending on the prompting strategy you are using, you may want to format these
differently before passing them into the LLM.

## Attributes

[attribute

format\_to\_openai\_functions: format\_to\_openai\_function\_messages](/python/langchain-classic/agents/format_scratchpad/openai_functions/format_to_openai_functions)

## Functions

[function

format\_log\_to\_str

Construct the scratchpad that lets the agent continue its thought process.](/python/langchain-classic/agents/format_scratchpad/log/format_log_to_str)[function

format\_log\_to\_messages

Construct the scratchpad that lets the agent continue its thought process.](/python/langchain-classic/agents/format_scratchpad/log_to_messages/format_log_to_messages)[function

format\_to\_openai\_function\_messages

Convert (AgentAction, tool output) tuples into FunctionMessages.](/python/langchain-classic/agents/format_scratchpad/openai_functions/format_to_openai_function_messages)[function

format\_to\_tool\_messages

Convert (AgentAction, tool output) tuples into `ToolMessage` objects.](/python/langchain-classic/agents/format_scratchpad/tools/format_to_tool_messages)[function

format\_xml

Format the intermediate steps as XML.](/python/langchain-classic/agents/format_scratchpad/xml/format_xml)

## Modules

[module

log](/python/langchain-classic/agents/format_scratchpad/log)[module

openai\_tools](/python/langchain-classic/agents/format_scratchpad/openai_tools)[module

tools](/python/langchain-classic/agents/format_scratchpad/tools)[module

openai\_functions](/python/langchain-classic/agents/format_scratchpad/openai_functions)[module

xml](/python/langchain-classic/agents/format_scratchpad/xml)[module

log\_to\_messages](/python/langchain-classic/agents/format_scratchpad/log_to_messages)


