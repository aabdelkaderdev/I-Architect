<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/stdout -->

Modulev1.2.21 (latest)●Since v0.1

# stdout

Callback handler that prints to std out.

## Functions

[function

print\_text

Print text with highlighting and no end characters.

If a color is provided, the text will be printed in that color.

If a file is provided, the text will be written to that file.](/python/langchain-core/utils/input/print_text)

## Classes

[class

BaseCallbackHandler

Base callback handler.](/python/langchain-core/callbacks/base/BaseCallbackHandler)[class

AgentAction

Represents a request to execute an action by an agent.

The action consists of the name of the tool to execute and the input to pass
to the tool. The log is used to pass along extra information about the action.](/python/langchain-core/agents/AgentAction)[class

AgentFinish

Final return value of an `ActionAgent`.

Agents return an `AgentFinish` when they have reached a stopping condition.](/python/langchain-core/agents/AgentFinish)[class

StdOutCallbackHandler

Callback handler that prints to std out.](/python/langchain-core/callbacks/stdout/StdOutCallbackHandler)


