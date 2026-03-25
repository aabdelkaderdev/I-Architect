<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/types -->

Modulev1.2.13 (latest)●Since v0.3

# types

Types for middleware and agents.

## Attributes

[attribute

JumpTo: Literal['tools', 'model', 'end']

Destination to jump to when a middleware node returns.](/python/langchain/agents/middleware/types/JumpTo)[attribute

ResponseT](/python/langchain/agents/middleware/types/ResponseT)[attribute

OmitFromInput

Annotation used to mark state attributes as omitted from input schema.](/python/langchain/agents/middleware/types/OmitFromInput)[attribute

OmitFromOutput

Annotation used to mark state attributes as omitted from output schema.](/python/langchain/agents/middleware/types/OmitFromOutput)[attribute

PrivateStateAttr

Annotation used to mark state attributes as purely internal for a given middleware.](/python/langchain/agents/middleware/types/PrivateStateAttr)[attribute

StateT](/python/langchain/agents/middleware/types/StateT)[attribute

StateT\_co](/python/langchain/agents/middleware/types/StateT_co)[attribute

StateT\_contra](/python/langchain/agents/middleware/types/StateT_contra)[attribute

CallableT](/python/langchain/agents/middleware/types/CallableT)

## Functions

[function

hook\_config

Decorator to configure hook behavior in middleware methods.

Use this decorator on `before_model` or `after_model` methods in middleware classes
to configure their behavior. Currently supports specifying which destinations they
can jump to, which establishes conditional edges in the agent graph.](/python/langchain/agents/middleware/types/hook_config)[function

before\_model

Decorator used to dynamically create a middleware with the `before_model` hook.](/python/langchain/agents/middleware/types/before_model)[function

after\_model

Decorator used to dynamically create a middleware with the `after_model` hook.](/python/langchain/agents/middleware/types/after_model)[function

before\_agent

Decorator used to dynamically create a middleware with the `before_agent` hook.](/python/langchain/agents/middleware/types/before_agent)[function

after\_agent

Decorator used to dynamically create a middleware with the `after_agent` hook.

Async version is `aafter_agent`.](/python/langchain/agents/middleware/types/after_agent)[function

dynamic\_prompt

Decorator used to dynamically generate system prompts for the model.

This is a convenience decorator that creates middleware using `wrap_model_call`
specifically for dynamic prompt generation. The decorated function should return
a string that will be set as the system prompt for the model request.](/python/langchain/agents/middleware/types/dynamic_prompt)[function

wrap\_model\_call

Create middleware with `wrap_model_call` hook from a function.

Converts a function with handler callback into middleware that can intercept model
calls, implement retry logic, handle errors, and rewrite responses.](/python/langchain/agents/middleware/types/wrap_model_call)[function

wrap\_tool\_call

Create middleware with `wrap_tool_call` hook from a function.

Async version is `awrap_tool_call`.

Converts a function with handler callback into middleware that can intercept
tool calls, implement retry logic, monitor execution, and modify responses.](/python/langchain/agents/middleware/types/wrap_tool_call)

## Classes

[class

ModelRequest

Model request information for the agent.](/python/langchain/agents/middleware/types/ModelRequest)[class

ModelResponse

Response from model execution including messages and optional structured output.

The result will usually contain a single `AIMessage`, but may include an additional
`ToolMessage` if the model used a tool for structured output.](/python/langchain/agents/middleware/types/ModelResponse)[class

ExtendedModelResponse

Model response with an optional 'Command' from 'wrap\_model\_call' middleware.

Use this to return a 'Command' alongside the model response from a
'wrap\_model\_call' handler. The command is applied as an additional state
update after the model node completes, using the graph's reducers (e.g.
'add\_messages' for the 'messages' key).

Because each 'Command' is applied through the reducer, messages in the
command are **added alongside** the model response messages rather than
replacing them. For non-reducer state fields, later commands overwrite
earlier ones (outermost middleware wins over inner).](/python/langchain/agents/middleware/types/ExtendedModelResponse)[class

OmitFromSchema

Annotation used to mark state attributes as omitted from input or output schemas.](/python/langchain/agents/middleware/types/OmitFromSchema)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/types/AgentState)[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/types/AgentMiddleware)

## Type Aliases

[typeAlias

ResponseFormat: ToolStrategy[SchemaT] | ProviderStrategy[SchemaT] | AutoStrategy[SchemaT]

Union type for all supported response format strategies.](/python/langchain/agents/middleware/types/ResponseFormat)[typeAlias

ModelCallResult: TypeAlias

`TypeAlias` for model call handler return value.

Middleware can return either:

- `ModelResponse`: Full response with messages and optional structured output
- `AIMessage`: Simplified return for simple use cases
- `ExtendedModelResponse`: Response with an optional `Command` for additional state updates
  `goto`, `resume`, and `graph` are not yet supported on these commands.
  A `NotImplementedError` will be raised if you try to use them.](/python/langchain/agents/middleware/types/ModelCallResult)


