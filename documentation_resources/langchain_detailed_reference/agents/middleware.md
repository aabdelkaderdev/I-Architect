<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware -->

Modulev1.2.13 (latest)●Since v0.3

# middleware

## Functions

## Classes

## Type Aliases

## Modules



[function

after\_agent

Decorator used to dynamically create a middleware with the `after_agent` hook.

Async version is `aafter_agent`.](/python/langchain/agents/middleware/after_agent)

[function

after\_model

Decorator used to dynamically create a middleware with the `after_model` hook.](/python/langchain/agents/middleware/after_model)

[function

before\_agent

Decorator used to dynamically create a middleware with the `before_agent` hook.](/python/langchain/agents/middleware/before_agent)

[function

before\_model

Decorator used to dynamically create a middleware with the `before_model` hook.](/python/langchain/agents/middleware/before_model)

[function

dynamic\_prompt

Decorator used to dynamically generate system prompts for the model.

This is a convenience decorator that creates middleware using `wrap_model_call`
specifically for dynamic prompt generation. The decorated function should return
a string that will be set as the system prompt for the model request.](/python/langchain/agents/middleware/dynamic_prompt)

[function

hook\_config

Decorator to configure hook behavior in middleware methods.

Use this decorator on `before_model` or `after_model` methods in middleware classes
to configure their behavior. Currently supports specifying which destinations they
can jump to, which establishes conditional edges in the agent graph.](/python/langchain/agents/middleware/hook_config)

[function

wrap\_model\_call

Create middleware with `wrap_model_call` hook from a function.

Converts a function with handler callback into middleware that can intercept model
calls, implement retry logic, handle errors, and rewrite responses.](/python/langchain/agents/middleware/wrap_model_call)

[function

wrap\_tool\_call

Create middleware with `wrap_tool_call` hook from a function.

Async version is `awrap_tool_call`.

Converts a function with handler callback into middleware that can intercept
tool calls, implement retry logic, monitor execution, and modify responses.](/python/langchain/agents/middleware/wrap_tool_call)

[class

ClearToolUsesEdit

Configuration for clearing tool outputs when token limits are exceeded.](/python/langchain/agents/middleware/ClearToolUsesEdit)

[class

ContextEditingMiddleware

Automatically prune tool results to manage context size.

The middleware applies a sequence of edits when the total input token count exceeds
configured thresholds.

Currently the `ClearToolUsesEdit` strategy is supported, aligning with Anthropic's
`clear_tool_uses_20250919` behavior [(read more)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool).](/python/langchain/agents/middleware/ContextEditingMiddleware)

[class

FilesystemFileSearchMiddleware

Provides Glob and Grep search over filesystem files.

This middleware adds two tools that search through local filesystem:

- Glob: Fast file pattern matching by file path
- Grep: Fast content search using ripgrep or Python fallback](/python/langchain/agents/middleware/FilesystemFileSearchMiddleware)

[class

HumanInTheLoopMiddleware

Human in the loop middleware.](/python/langchain/agents/middleware/HumanInTheLoopMiddleware)

[class

InterruptOnConfig

Configuration for an action requiring human in the loop.

This is the configuration format used in the `HumanInTheLoopMiddleware.__init__`
method.](/python/langchain/agents/middleware/InterruptOnConfig)

[class

ModelCallLimitMiddleware

Tracks model call counts and enforces limits.

This middleware monitors the number of model calls made during agent execution
and can terminate the agent when specified limits are reached. It supports
both thread-level and run-level call counting with configurable exit behaviors.

Thread-level: The middleware tracks the number of model calls and persists
call count across multiple runs (invocations) of the agent.

Run-level: The middleware tracks the number of model calls made during a single
run (invocation) of the agent.](/python/langchain/agents/middleware/ModelCallLimitMiddleware)

[class

ModelFallbackMiddleware

Automatic fallback to alternative models on errors.

Retries failed model calls with alternative models in sequence until
success or all models exhausted. Primary model specified in `create_agent`.](/python/langchain/agents/middleware/ModelFallbackMiddleware)

[class

ModelRetryMiddleware

Middleware that automatically retries failed model calls with configurable backoff.

Supports retrying on specific exceptions and exponential backoff.](/python/langchain/agents/middleware/ModelRetryMiddleware)

[class

PIIDetectionError

Raised when configured to block on detected sensitive values.](/python/langchain/agents/middleware/PIIDetectionError)

[class

PIIMiddleware

Detect and handle Personally Identifiable Information (PII) in conversations.

This middleware detects common PII types and applies configurable strategies
to handle them. It can detect emails, credit cards, IP addresses, MAC addresses, and
URLs in both user input and agent output.

Built-in PII types:

- `email`: Email addresses
- `credit_card`: Credit card numbers (validated with Luhn algorithm)
- `ip`: IP addresses (validated with stdlib)
- `mac_address`: MAC addresses
- `url`: URLs (both `http`/`https` and bare URLs)

Strategies:

- `block`: Raise an exception when PII is detected
- `redact`: Replace PII with `[REDACTED_TYPE]` placeholders
- `mask`: Partially mask PII (e.g., `****-****-****-1234` for credit card)
- `hash`: Replace PII with deterministic hash (e.g., `<email_hash:a1b2c3d4>`)

Strategy Selection Guide:

| Strategy | Preserves Identity? | Best For |
| --- | --- | --- |
| `block` | N/A | Avoid PII completely |
| `redact` | No | General compliance, log sanitization |
| `mask` | No | Human readability, customer service UIs |
| `hash` | Yes (pseudonymous) | Analytics, debugging |](/python/langchain/agents/middleware/PIIMiddleware)

[class

CodexSandboxExecutionPolicy

Launch the shell through the Codex CLI sandbox.

Ideal when you have the Codex CLI installed and want the additional syscall and
filesystem restrictions provided by Anthropic's Seatbelt (macOS) or Landlock/seccomp
(Linux) profiles. Commands still run on the host, but within the sandbox requested by
the CLI. If the Codex binary is unavailable or the runtime lacks the required
kernel features (e.g., Landlock inside some containers), process startup fails with a
`RuntimeError`.

Configure sandbox behavior via `config_overrides` to align with your Codex CLI
profile. This policy does not add its own resource limits; combine it with
host-level guards (cgroups, container resource limits) as needed.](/python/langchain/agents/middleware/CodexSandboxExecutionPolicy)

[class

DockerExecutionPolicy

Run the shell inside a dedicated Docker container.

Choose this policy when commands originate from untrusted users or you require
strong isolation between sessions. By default the workspace is bind-mounted only
when it refers to an existing non-temporary directory; ephemeral sessions run
without a mount to minimise host exposure. The container's network namespace is
disabled by default (`--network none`) and you can enable further hardening via
`read_only_rootfs` and `user`.

The security guarantees depend on your Docker daemon configuration. Run the agent on
a host where Docker is locked down (rootless mode, AppArmor/SELinux, etc.) and
review any additional volumes or capabilities passed through `extra_run_args`. The
default image is `python:3.12-alpine3.19`; supply a custom image if you need
preinstalled tooling.](/python/langchain/agents/middleware/DockerExecutionPolicy)

[class

HostExecutionPolicy

Run the shell directly on the host process.

This policy is best suited for trusted or single-tenant environments (CI jobs,
developer workstations, pre-sandboxed containers) where the agent must access the
host filesystem and tooling without additional isolation. Enforces optional CPU and
memory limits to prevent runaway commands but offers **no** filesystem or network
sandboxing; commands can modify anything the process user can reach.

On Linux platforms resource limits are applied with `resource.prlimit` after the
shell starts. On macOS, where `prlimit` is unavailable, limits are set in a
`preexec_fn` before `exec`. In both cases the shell runs in its own process group
so timeouts can terminate the full subtree.](/python/langchain/agents/middleware/HostExecutionPolicy)

[class

RedactionRule

Configuration for handling a single PII type.](/python/langchain/agents/middleware/RedactionRule)

[class

ShellToolMiddleware

Middleware that registers a persistent shell tool for agents.

The middleware exposes a single long-lived shell session. Use the execution policy
to match your deployment's security posture:

- `HostExecutionPolicy` – full host access; best for trusted environments where the
  agent already runs inside a container or VM that provides isolation.
- `CodexSandboxExecutionPolicy` – reuses the Codex CLI sandbox for additional
  syscall/filesystem restrictions when the CLI is available.
- `DockerExecutionPolicy` – launches a separate Docker container for each agent run,
  providing harder isolation, optional read-only root filesystems, and user
  remapping.

When no policy is provided the middleware defaults to `HostExecutionPolicy`.](/python/langchain/agents/middleware/ShellToolMiddleware)

[class

SummarizationMiddleware

Summarizes conversation history when token limits are approached.

This middleware monitors message token counts and automatically summarizes older
messages when a threshold is reached, preserving recent messages and maintaining
context continuity by ensuring AI/Tool message pairs remain together.](/python/langchain/agents/middleware/SummarizationMiddleware)

[class

TodoListMiddleware

Middleware that provides todo list management capabilities to agents.

This middleware adds a `write_todos` tool that allows agents to create and manage
structured task lists for complex multi-step operations. It's designed to help
agents track progress, organize complex tasks, and provide users with visibility
into task completion status.

The middleware automatically injects system prompts that guide the agent on when
and how to use the todo functionality effectively. It also enforces that the
`write_todos` tool is called at most once per model turn, since the tool replaces
the entire todo list and parallel calls would create ambiguity about precedence.](/python/langchain/agents/middleware/TodoListMiddleware)

[class

ToolCallLimitMiddleware

Track tool call counts and enforces limits during agent execution.

This middleware monitors the number of tool calls made and can terminate or
restrict execution when limits are exceeded. It supports both thread-level
(persistent across runs) and run-level (per invocation) call counting.](/python/langchain/agents/middleware/ToolCallLimitMiddleware)

[class

LLMToolEmulator

Emulates specified tools using an LLM instead of executing them.

This middleware allows selective emulation of tools for testing purposes.

By default (when `tools=None`), all tools are emulated. You can specify which
tools to emulate by passing a list of tool names or `BaseTool` instances.](/python/langchain/agents/middleware/LLMToolEmulator)

[class

ToolRetryMiddleware

Middleware that automatically retries failed tool calls with configurable backoff.

Supports retrying on specific exceptions and exponential backoff.](/python/langchain/agents/middleware/ToolRetryMiddleware)

[class

LLMToolSelectorMiddleware

Uses an LLM to select relevant tools before calling the main model.

When an agent has many tools available, this middleware filters them down
to only the most relevant ones for the user's query. This reduces token usage
and helps the main model focus on the right tools.](/python/langchain/agents/middleware/LLMToolSelectorMiddleware)

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/AgentMiddleware)

[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/AgentState)

[class

ExtendedModelResponse

Model response with an optional 'Command' from 'wrap\_model\_call' middleware.

Use this to return a 'Command' alongside the model response from a
'wrap\_model\_call' handler. The command is applied as an additional state
update after the model node completes, using the graph's reducers (e.g.
'add\_messages' for the 'messages' key).

Because each 'Command' is applied through the reducer, messages in the
command are **added alongside** the model response messages rather than
replacing them. For non-reducer state fields, later commands overwrite
earlier ones (outermost middleware wins over inner).](/python/langchain/agents/middleware/ExtendedModelResponse)

[class

ModelRequest

Model request information for the agent.](/python/langchain/agents/middleware/ModelRequest)

[class

ModelResponse

Response from model execution including messages and optional structured output.

The result will usually contain a single `AIMessage`, but may include an additional
`ToolMessage` if the model used a tool for structured output.](/python/langchain/agents/middleware/ModelResponse)

[typeAlias

ModelCallResult: TypeAlias

`TypeAlias` for model call handler return value.

Middleware can return either:

- `ModelResponse`: Full response with messages and optional structured output
- `AIMessage`: Simplified return for simple use cases
- `ExtendedModelResponse`: Response with an optional `Command` for additional state updates
  `goto`, `resume`, and `graph` are not yet supported on these commands.
  A `NotImplementedError` will be raised if you try to use them.](/python/langchain/agents/middleware/ModelCallResult)

[module

model\_fallback

Model fallback middleware for agents.](/python/langchain/agents/middleware/model_fallback)

[module

context\_editing

Context editing middleware.

Mirrors Anthropic's context editing capabilities by clearing older tool results once the
conversation grows beyond a configurable token threshold.

The implementation is intentionally model-agnostic so it can be used with any LangChain
chat model.](/python/langchain/agents/middleware/context_editing)

[module

shell\_tool

Middleware that exposes a persistent shell tool to agents.](/python/langchain/agents/middleware/shell_tool)

[module

file\_search

File search middleware for Anthropic text editor and memory tools.

This module provides Glob and Grep search tools that operate on files stored
in state or filesystem.](/python/langchain/agents/middleware/file_search)

[module

model\_retry

Model retry middleware for agents.](/python/langchain/agents/middleware/model_retry)

[module

tool\_call\_limit

Tool call limit middleware for agents.](/python/langchain/agents/middleware/tool_call_limit)

[module

todo

Planning and task management middleware for agents.](/python/langchain/agents/middleware/todo)

[module

tool\_selection

LLM-based tool selector middleware.](/python/langchain/agents/middleware/tool_selection)

[module

tool\_retry

Tool retry middleware for agents.](/python/langchain/agents/middleware/tool_retry)

[module

tool\_emulator

Tool emulator middleware for testing.](/python/langchain/agents/middleware/tool_emulator)

[module

model\_call\_limit

Call tracking middleware for agents.](/python/langchain/agents/middleware/model_call_limit)

[module

pii

PII detection and handling middleware for agents.](/python/langchain/agents/middleware/pii)

[module

types

Types for middleware and agents.](/python/langchain/agents/middleware/types)

[module

human\_in\_the\_loop

Human in the loop middleware.](/python/langchain/agents/middleware/human_in_the_loop)

[module

summarization

Summarization middleware.](/python/langchain/agents/middleware/summarization)

Entrypoint to using [middleware](https://docs.langchain.com/oss/python/langchain/middleware) plugins with [Agents](https://docs.langchain.com/oss/python/langchain/agents).