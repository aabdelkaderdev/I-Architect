<!-- Source: https://reference.langchain.com/python/langchain/middleware -->

Reference docs

This page contains **reference documentation** for Middleware. See [the docs](https://docs.langchain.com/oss/python/langchain/middleware) for conceptual guides, tutorials, and examples on using Middleware.

## Middleware classes

LangChain provides prebuilt middleware for common agent use cases:

| CLASS | DESCRIPTION |
| --- | --- |
| [`SummarizationMiddleware`](/python/langchain/agents/middleware/summarization/SummarizationMiddleware) | Automatically summarize conversation history when approaching token limits |
| [`HumanInTheLoopMiddleware`](/python/langchain/agents/middleware/human_in_the_loop/HumanInTheLoopMiddleware) | Pause execution for human approval of tool calls |
| [`ModelCallLimitMiddleware`](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitMiddleware) | Limit the number of model calls to prevent excessive costs |
| [`ToolCallLimitMiddleware`](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitMiddleware) | Control tool execution by limiting call counts |
| [`ModelFallbackMiddleware`](/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware) | Automatically fallback to alternative models when primary fails |
| [`PIIMiddleware`](/python/langchain/agents/middleware/pii/PIIMiddleware) | Detect and handle Personally Identifiable Information |
| [`TodoListMiddleware`](/python/langchain/agents/middleware/todo/TodoListMiddleware) | Equip agents with task planning and tracking capabilities |
| [`LLMToolSelectorMiddleware`](/python/langchain/agents/middleware/tool_selection/LLMToolSelectorMiddleware) | Use an LLM to select relevant tools before calling main model |
| [`ToolRetryMiddleware`](/python/langchain/agents/middleware/tool_retry/ToolRetryMiddleware) | Automatically retry failed tool calls with exponential backoff |
| [`LLMToolEmulator`](/python/langchain/agents/middleware/tool_emulator/LLMToolEmulator) | Emulate tool execution using LLM for testing purposes |
| [`ContextEditingMiddleware`](/python/langchain/agents/middleware/context_editing/ContextEditingMiddleware) | Manage conversation context by trimming or clearing tool uses |
| [`ShellToolMiddleware`](/python/langchain/agents/middleware/shell_tool/ShellToolMiddleware) | Expose a persistent shell session to agents for command execution |
| [`FilesystemFileSearchMiddleware`](/python/langchain/agents/middleware/file_search/FilesystemFileSearchMiddleware) | Provide Glob and Grep search tools over filesystem files |
| [`AgentMiddleware`](/python/langchain/agents/middleware/types/AgentMiddleware) | Base middleware class for creating custom middleware |

## Decorators

Create custom middleware using these decorators:

| DECORATOR | DESCRIPTION |
| --- | --- |
| [`@before_agent`](/python/langchain/agents/middleware/types/before_agent) | Execute logic before agent execution starts |
| [`@before_model`](/python/langchain/agents/middleware/types/before_model) | Execute logic before each model call |
| [`@after_model`](/python/langchain/agents/middleware/types/after_model) | Execute logic after each model receives a response |
| [`@after_agent`](/python/langchain/agents/middleware/types/after_agent) | Execute logic after agent execution completes |
| [`@wrap_model_call`](/python/langchain/agents/middleware/types/wrap_model_call) | Wrap and intercept model calls |
| [`@wrap_tool_call`](/python/langchain/agents/middleware/types/wrap_tool_call) | Wrap and intercept tool calls |
| [`@dynamic_prompt`](/python/langchain/agents/middleware/types/dynamic_prompt) | Generate dynamic system prompts based on request context |
| [`@hook_config`](/python/langchain/agents/middleware/types/hook_config) | Configure hook behavior (e.g., conditional routing) |

## Types and utilities

Core types for building middleware:

| TYPE | DESCRIPTION |
| --- | --- |
| [`AgentState`](/python/langchain/agents/middleware/types/AgentState) | State container for agent execution |
| [`ModelRequest`](/python/langchain/agents/middleware/types/ModelRequest) | Request details passed to model calls |
| [`ModelResponse`](/python/langchain/agents/middleware/types/ModelResponse) | Response details from model calls |
| [`ClearToolUsesEdit`](/python/langchain/agents/middleware/context_editing/ClearToolUsesEdit) | Utility for clearing tool usage history from context |
| [`InterruptOnConfig`](/python/langchain/agents/middleware/human_in_the_loop/InterruptOnConfig) | Configuration for human-in-the-loop interruptions |

[`SummarizationMiddleware`](/python/langchain/agents/middleware/summarization/SummarizationMiddleware) types:

| TYPE | DESCRIPTION |
| --- | --- |
| [`ContextSize`](/python/langchain/agents/middleware/summarization/ContextSize) | Union type |
| [`ContextFraction`](/python/langchain/agents/middleware/summarization/ContextFraction) | Summarize at fraction of total context |
| [`ContextTokens`](/python/langchain/agents/middleware/summarization/ContextTokens) | Summarize at token threshold |
| [`ContextMessages`](/python/langchain/agents/middleware/summarization/ContextMessages) | Summarize at message threshold |