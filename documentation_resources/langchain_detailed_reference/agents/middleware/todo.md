<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/todo -->

Modulev1.2.13 (latest)●Since v1.0

# todo

Planning and task management middleware for agents.

## Attributes

[attribute

OmitFromInput

Annotation used to mark state attributes as omitted from input schema.](/python/langchain/agents/middleware/todo/OmitFromInput)[attribute

ResponseT](/python/langchain/agents/middleware/todo/ResponseT)[attribute

WRITE\_TODOS\_TOOL\_DESCRIPTION: str](/python/langchain/agents/middleware/todo/WRITE_TODOS_TOOL_DESCRIPTION)[attribute

WRITE\_TODOS\_SYSTEM\_PROMPT: str](/python/langchain/agents/middleware/todo/WRITE_TODOS_SYSTEM_PROMPT)

## Functions

[function

write\_todos

Create and manage a structured task list for your current work session.](/python/langchain/agents/middleware/todo/write_todos)

## Classes

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/todo/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/todo/AgentState)[class

ModelRequest

Model request information for the agent.](/python/langchain/agents/middleware/todo/ModelRequest)[class

ModelResponse

Response from model execution including messages and optional structured output.

The result will usually contain a single `AIMessage`, but may include an additional
`ToolMessage` if the model used a tool for structured output.](/python/langchain/agents/middleware/todo/ModelResponse)[class

Todo

A single todo item with content and status.](/python/langchain/agents/middleware/todo/Todo)[class

PlanningState

State schema for the todo middleware.](/python/langchain/agents/middleware/todo/PlanningState)[class

TodoListMiddleware

Middleware that provides todo list management capabilities to agents.

This middleware adds a `write_todos` tool that allows agents to create and manage
structured task lists for complex multi-step operations. It's designed to help
agents track progress, organize complex tasks, and provide users with visibility
into task completion status.

The middleware automatically injects system prompts that guide the agent on when
and how to use the todo functionality effectively. It also enforces that the
`write_todos` tool is called at most once per model turn, since the tool replaces
the entire todo list and parallel calls would create ambiguity about precedence.](/python/langchain/agents/middleware/todo/TodoListMiddleware)


