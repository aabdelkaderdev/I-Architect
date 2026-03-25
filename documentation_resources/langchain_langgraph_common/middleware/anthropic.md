<!-- Source: https://docs.langchain.com/oss/python/integrations/middleware/anthropic -->

Middleware specifically designed for Anthropic’s Claude models. Learn more about [middleware](/oss/python/langchain/middleware/overview).

| Middleware | Description |
| --- | --- |
| [Prompt caching](#prompt-caching) | Reduce costs by caching repetitive prompt prefixes |
| [Bash tool](#bash-tool) | Execute Claude’s native bash tool with local command execution |
| [Text editor](#text-editor) | Provide Claude’s text editor tool for file editing |
| [Memory](#memory) | Provide Claude’s memory tool for persistent agent memory |
| [File search](#file-search) | Search tools for state-based file systems |

## [​](#middleware-vs-tools) Middleware vs tools

`langchain-anthropic` provides two ways to use Claude’s native tools:

- **Middleware** (this page): Production-ready implementations with built-in execution, state management, and security policies
- **Tools** (via [`bind_tools`](/oss/python/integrations/chat/anthropic#built-in-tools)): Low-level building blocks where you provide your own execution logic

### [​](#when-to-use-which) When to use which

| Use case | Recommended | Why |
| --- | --- | --- |
| Production agents with bash | Middleware | Persistent sessions, Docker isolation, output redaction |
| State-based file editing | Middleware | Built-in LangGraph state persistence |
| Filesystem file editing | Middleware | Writes to disk with path validation |
| Custom execution logic | Tools | Full control over execution |
| Quick prototype | Tools | Simpler, bring your own callback |
| Non-agent use with [`bind_tools`](https://reference.langchain.com/python/langchain-anthropic/chat_models/ChatAnthropic/bind_tools) | Tools | Middleware requires [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) |

### [​](#feature-comparison) Feature comparison

| Feature | Middleware | Tools |
| --- | --- | --- |
| Works with [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) | ✅ | ✅ |
| Works with [`bind_tools`](https://reference.langchain.com/python/langchain-anthropic/chat_models/ChatAnthropic/bind_tools) | ❌ | ✅ |
| Built-in state management | ✅ | ❌ |
| Custom execute callback | ❌ | ✅ |

Example: Middleware vs tools comparison

**Using middleware** (turnkey solution):

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import ClaudeBashToolMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import DockerExecutionPolicy

# Production-ready with Docker isolation, session management, etc.
agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    middleware=[
        ClaudeBashToolMiddleware(
            workspace_root="/workspace",
            execution_policy=DockerExecutionPolicy(image="python:3.11"),
            startup_commands=["pip install pandas"],
        ),
    ],
)
```

**Using tools** (bring your own execution):

Copy

```
import subprocess

from anthropic.types.beta import BetaToolBash20250124Param
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from langchain.tools import tool

tool_spec = BetaToolBash20250124Param(
    name="bash",
    type="bash_20250124",
    strict=True,
)

@tool(extras={"provider_tool_definition": tool_spec})
def bash(*, command: str, restart: bool = False, **kw):
    """Execute a bash command."""
    if restart:
        return "Bash session restarted"
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {e}"

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[bash],
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "List files in this directory"}]}
)
print(result["messages"][-1].content)
```

---

## [​](#prompt-caching) Prompt caching

Reduce costs and latency by caching static or repetitive prompt content (like system prompts, tool definitions, and conversation history) on Anthropic’s servers. This middleware implements a **conversational caching strategy** that places cache breakpoints after the most recent message, allowing the entire conversation history (including the latest user message) to be cached and reused in subsequent API calls.
Prompt caching is useful for the following:

- Applications with long, static system prompts that don’t change between requests
- Agents with many tool definitions that remain constant across invocations
- Conversations where early message history is reused across multiple turns
- High-volume deployments where reducing API costs and latency is critical

Learn more about [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#cache-limitations) strategies and limitations.

**API reference:** [`AnthropicPromptCachingMiddleware`](https://reference.langchain.com/python/langchain-anthropic/middleware/prompt_caching/AnthropicPromptCachingMiddleware)

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import AnthropicPromptCachingMiddleware
from langchain.agents import create_agent

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    system_prompt="<Your long system prompt here>",
    middleware=[AnthropicPromptCachingMiddleware(ttl="5m")],
)
```

Configuration options

[​](#param-type)

type

string

default:"ephemeral"

Cache type. Only `'ephemeral'` is currently supported.

[​](#param-ttl)

ttl

string

default:"5m"

Time to live for cached content. Valid values: `'5m'` or `'1h'`

[​](#param-min-messages-to-cache)

min\_messages\_to\_cache

number

default:"0"

Minimum number of messages before caching starts

[​](#param-unsupported-model-behavior)

unsupported\_model\_behavior

string

default:"warn"

Behavior when using non-Anthropic models. Options: `'ignore'`, `'warn'`, or `'raise'`

Full example

The middleware caches content up to and including the latest message in each request. On subsequent requests within the TTL window (5 minutes or 1 hour), previously seen content is retrieved from cache rather than reprocessed, significantly reducing costs and latency.**How it works:**

1. First request: System prompt, tools, and the user message *“Hi, my name is Bob”* are sent to the API and cached
2. Second request: The cached content (system prompt, tools, and first message) is retrieved from cache. Only the new message *“What’s my name?”* needs to be processed, plus the model’s response from the first request
3. This pattern continues for each turn, with each request reusing the cached conversation history

Prompt caching reduces API costs by caching tokens, but does **not** provide conversation memory. To persist conversation history across invocations, use a [checkpointer](https://langchain-ai.github.io/langgraph/concepts/persistence/#checkpointer-libraries) like `MemorySaver`.

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import AnthropicPromptCachingMiddleware
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

LONG_PROMPT = """
Please be a helpful assistant.

<Lots more context ...>
"""

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    system_prompt=LONG_PROMPT,
    middleware=[AnthropicPromptCachingMiddleware(ttl="5m")],
    checkpointer=MemorySaver(),  # Persists conversation history
)

# Use a thread_id to maintain conversation state
config: RunnableConfig = {"configurable": {"thread_id": "user-123"}}

# First invocation: Creates cache with system prompt, tools, and "Hi, my name is Bob"
agent.invoke({"messages": [HumanMessage("Hi, my name is Bob")]}, config=config)

# Second invocation: Reuses cached system prompt, tools, and previous messages
# The checkpointer maintains conversation history, so the agent remembers "Bob"
result = agent.invoke({"messages": [HumanMessage("What's my name?")]}, config=config)
print(result["messages"][-1].content)
```

Copy

```
Your name is Bob! You told me that when you introduced yourself at the start of our conversation.
```

## [​](#bash-tool) Bash tool

Execute Claude’s native `bash_20250124` tool with local command execution.
The bash tool middleware is useful for the following:

- Using Claude’s built-in bash tool with local execution
- Leveraging Claude’s optimized bash tool interface
- Agents that need persistent shell sessions with Anthropic models

This middleware wraps `ShellToolMiddleware` and exposes it as Claude’s native bash tool.

**API reference:** [`ClaudeBashToolMiddleware`](https://reference.langchain.com/python/langchain-anthropic/middleware/bash/ClaudeBashToolMiddleware)

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import ClaudeBashToolMiddleware
from langchain.agents import create_agent

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[
        ClaudeBashToolMiddleware(
            workspace_root="/workspace",
        ),
    ],
)
```

Configuration options

`ClaudeBashToolMiddleware` accepts all parameters from [`ShellToolMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/shell_tool/ShellToolMiddleware), including:

[​](#param-workspace-root)

workspace\_root

str | Path | None

Base directory for the shell session

[​](#param-startup-commands)

startup\_commands

tuple[str, ...] | list[str] | str | None

Commands to run when the session starts

[​](#param-execution-policy)

execution\_policy

BaseExecutionPolicy | None

Execution policy (`HostExecutionPolicy`, `DockerExecutionPolicy`, or `CodexSandboxExecutionPolicy`)

[​](#param-redaction-rules)

redaction\_rules

tuple[RedactionRule, ...] | list[RedactionRule] | None

Rules for sanitizing command output

See [Shell tool](/oss/python/langchain/middleware/built-in#shell-tool) for full configuration details.

Full example

Copy

```
import tempfile

from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import ClaudeBashToolMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import DockerExecutionPolicy

# Create a temporary workspace directory for this demo.
# In production, use a persistent directory path.
workspace = tempfile.mkdtemp(prefix="agent-workspace-")

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[
        ClaudeBashToolMiddleware(
            workspace_root=workspace,
            startup_commands=["echo 'Session initialized'"],
            execution_policy=DockerExecutionPolicy(
                image="python:3.11-slim",
            ),
        ),
    ],
)

# Claude can now use its native bash tool
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What version of Python is installed?"}]}
)
print(result["messages"][-1].content)
```

Copy

```
Python 3.11.14 is installed.
```

## [​](#text-editor) Text editor

Provide Claude’s text editor tool (`text_editor_20250728`) for file creation and editing.
The text editor middleware is useful for the following:

- File-based agent workflows
- Code editing and refactoring tasks
- Multi-file project work
- Agents that need persistent file storage

Available in two variants: **State-based** (files in LangGraph state) and **Filesystem-based** (files on disk).

**API references:**

- [`StateClaudeTextEditorMiddleware`](https://reference.langchain.com/python/langchain-anthropic/middleware/anthropic_tools/StateClaudeTextEditorMiddleware)
- [`FilesystemClaudeTextEditorMiddleware`](https://reference.langchain.com/python/langchain-anthropic/middleware/anthropic_tools/FilesystemClaudeTextEditorMiddleware)

State-based text editor

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import StateClaudeTextEditorMiddleware
from langchain.agents import create_agent

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[StateClaudeTextEditorMiddleware()],
)
```

Filesystem-based text editor

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import FilesystemClaudeTextEditorMiddleware
from langchain.agents import create_agent

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[
        FilesystemClaudeTextEditorMiddleware(
            root_path="/workspace",
        ),
    ],
)
```

Claude’s text editor tool supports the following commands:

- `view` - View file contents or list directory
- `create` - Create a new file
- `str_replace` - Replace string in file
- `insert` - Insert text at line number
- `delete` - Delete a file
- `rename` - Rename/move a file

Configuration options

**[`StateClaudeTextEditorMiddleware`](https://reference.langchain.com/python/langchain-anthropic/middleware/anthropic_tools/StateClaudeTextEditorMiddleware) (state-based)**

[​](#param-allowed-path-prefixes)

allowed\_path\_prefixes

Sequence[str] | None

Optional list of allowed path prefixes. If specified, only paths starting with these prefixes are allowed.

**[`FilesystemClaudeTextEditorMiddleware`](https://reference.langchain.com/python/langchain-anthropic/middleware/anthropic_tools/FilesystemClaudeTextEditorMiddleware) (filesystem-based)**

[​](#param-root-path)

root\_path

str

required

Root directory for file operations

[​](#param-allowed-prefixes)

allowed\_prefixes

list[str] | None

Optional list of allowed virtual path prefixes (default: `["/"]`)

[​](#param-max-file-size-mb)

max\_file\_size\_mb

int

default:"10"

Maximum file size in MB

Full example: State-based text editor

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import StateClaudeTextEditorMiddleware
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[
        StateClaudeTextEditorMiddleware(
            allowed_path_prefixes=["/project"],
        ),
    ],
    checkpointer=MemorySaver(),
)

# Use a thread_id to persist state across invocations
config: RunnableConfig = {"configurable": {"thread_id": "my-session"}}

# Claude can now create and edit files (stored in LangGraph state)
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Create a file at /project/hello.py with a simple hello world program"}]},
    config=config,
)
print(result["messages"][-1].content)
```

Copy

```
I've created a simple "Hello, World!" program at `/project/hello.py`. The program uses Python's `print()` function to display "Hello, World!" to the console when executed.
```

Full example: Filesystem-based text editor

Copy

```
import tempfile

from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import FilesystemClaudeTextEditorMiddleware
from langchain.agents import create_agent

# Create a temporary workspace directory for this demo.
# In production, use a persistent directory path.
workspace = tempfile.mkdtemp(prefix="editor-workspace-")

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[
        FilesystemClaudeTextEditorMiddleware(
            root_path=workspace,
            allowed_prefixes=["/src"],
            max_file_size_mb=10,
        ),
    ],
)

# Claude can now create and edit files (stored on disk)
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Create a file at /src/hello.py with a simple hello world program"}]}
)
print(result["messages"][-1].content)
```

Copy

```
I've created a simple "Hello, World!" program at `/src/hello.py`. The program uses Python's `print()` function to display "Hello, World!" to the console when executed.
```

## [​](#memory) Memory

Provide Claude’s memory tool (`memory_20250818`) for persistent agent memory across conversation turns.
The memory middleware is useful for the following:

- Long-running agent conversations
- Maintaining context across interruptions
- Task progress tracking
- Persistent agent state management

Claude’s memory tool uses a `/memories` directory and automatically injects a system prompt encouraging the agent to check and update memory.

**API reference:** [`StateClaudeMemoryMiddleware`](https://reference.langchain.com/python/langchain-anthropic/middleware/anthropic_tools/StateClaudeMemoryMiddleware), [`FilesystemClaudeMemoryMiddleware`](https://reference.langchain.com/python/langchain-anthropic/middleware/anthropic_tools/FilesystemClaudeMemoryMiddleware)

State-based memory

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import StateClaudeMemoryMiddleware
from langchain.agents import create_agent

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[StateClaudeMemoryMiddleware()],
)
```

Filesystem-based memory

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import FilesystemClaudeMemoryMiddleware
from langchain.agents import create_agent

agent_fs = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[
        FilesystemClaudeMemoryMiddleware(
            root_path="/workspace",
        ),
    ],
)
```

Configuration options

**[`StateClaudeMemoryMiddleware`](https://reference.langchain.com/python/langchain-anthropic/middleware/anthropic_tools/StateClaudeMemoryMiddleware) (state-based)**

[​](#param-allowed-path-prefixes-1)

allowed\_path\_prefixes

Sequence[str] | None

Optional list of allowed path prefixes. Defaults to `["/memories"]`.

[​](#param-system-prompt)

system\_prompt

str

System prompt to inject. Defaults to Anthropic’s recommended memory prompt that encourages the agent to check and update memory.

**[`FilesystemClaudeMemoryMiddleware`](https://reference.langchain.com/python/langchain-anthropic/middleware/anthropic_tools/FilesystemClaudeMemoryMiddleware) (filesystem-based)**

[​](#param-root-path-1)

root\_path

str

required

Root directory for file operations

[​](#param-allowed-prefixes-1)

allowed\_prefixes

list[str] | None

Optional list of allowed virtual path prefixes. Defaults to `["/memories"]`.

[​](#param-max-file-size-mb-1)

max\_file\_size\_mb

int

default:"10"

Maximum file size in MB

[​](#param-system-prompt-1)

system\_prompt

str

System prompt to inject

Full example: State-based memory

The agent will automatically:

1. Check `/memories` directory at start
2. Record progress and thoughts during execution
3. Update memory files as work progresses

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import StateClaudeMemoryMiddleware
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[StateClaudeMemoryMiddleware()],
    checkpointer=MemorySaver(),
)

# Use a thread_id to persist state across invocations
config: RunnableConfig = {"configurable": {"thread_id": "my-session"}}

# Claude can now use memory to track progress (stored in LangGraph state)
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Remember that my favorite color is blue, then confirm what you stored."}]},
    config=config,
)
print(result["messages"][-1].content)
```

Copy

```
Perfect! I've stored your favorite color as **blue** in my memory system. The information is saved in my user preferences file where I can access it in future conversations.
```

Full example: Filesystem-based memory

The agent will automatically:

1. Check `/memories` directory at start
2. Record progress and thoughts during execution
3. Update memory files as work progresses

Copy

```
import tempfile

from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import FilesystemClaudeMemoryMiddleware
from langchain.agents import create_agent

# Create a temporary workspace directory for this demo.
# In production, use a persistent directory path.
workspace = tempfile.mkdtemp(prefix="memory-workspace-")

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[
        FilesystemClaudeMemoryMiddleware(
            root_path=workspace,
        ),
    ],
)

# Claude can now use memory to track progress (stored on disk)
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Remember that my favorite color is blue, then confirm what you stored."}]}
)
print(result["messages"][-1].content)
```

Copy

```
Perfect! I've stored your favorite color as **blue** in my memory system. The information is saved in my user preferences file where I can access it in future conversations.
```

## [​](#file-search) File search

Provide Glob and Grep search tools for files stored in LangGraph state. File search middleware is useful for the following:

- Searching through state-based virtual file systems
- Works with text editor and memory tools
- Finding files by patterns
- Content search with regex

**API reference:** [`StateFileSearchMiddleware`](https://reference.langchain.com/python/langchain-anthropic/middleware/file_search/StateFileSearchMiddleware)

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import (
    StateClaudeTextEditorMiddleware,
    StateFileSearchMiddleware,
)
from langchain.agents import create_agent

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[
        StateClaudeTextEditorMiddleware(),
        StateFileSearchMiddleware(),  # Search text editor files
    ],
)
```

Configuration options

[​](#param-state-key)

state\_key

str

default:"text\_editor\_files"

State key containing files to search. Use `"text_editor_files"` for text editor files or `"memory_files"` for memory files.

Full example: Search text editor files

The middleware adds Glob and Grep search tools that work with state-based files.

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import (
    StateClaudeTextEditorMiddleware,
    StateFileSearchMiddleware,
)
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[
        StateClaudeTextEditorMiddleware(),
        StateFileSearchMiddleware(state_key="text_editor_files"),
    ],
    checkpointer=MemorySaver(),
)

# Use a thread_id to persist state across invocations
config: RunnableConfig = {"configurable": {"thread_id": "my-session"}}

# First invocation: Create some files using the text editor tool
result = agent.invoke(
    {"messages": [HumanMessage("Create a Python project with main.py, utils/helpers.py, and tests/test_main.py")]},
    config=config,
)

# The agent creates files, which are stored in state
print("Files created:", list(result["text_editor_files"].keys()))

# Second invocation: Search the files we just created
# State is automatically persisted via the checkpointer
result = agent.invoke(
    {"messages": [HumanMessage("Find all Python files in the project")]},
    config=config,
)
print(result["messages"][-1].content)
```

Copy

```
Files created: ['/project/main.py', '/project/utils/helpers.py', '/project/utils/__init__.py', '/project/tests/test_main.py', '/project/tests/__init__.py', '/project/README.md']
```

Copy

```
I found 5 Python files in the project:

1. `/project/main.py` - Main application file
2. `/project/utils/__init__.py` - Utils package initialization
3. `/project/utils/helpers.py` - Helper utilities
4. `/project/tests/__init__.py` - Tests package initialization
5. `/project/tests/test_main.py` - Main test file

Would you like me to view the contents of any of these files?
```

Full example: Search memory files

Copy

```
from langchain_anthropic import ChatAnthropic
from langchain_anthropic.middleware import (
    StateClaudeMemoryMiddleware,
    StateFileSearchMiddleware,
)
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[],
    middleware=[
        StateClaudeMemoryMiddleware(),
        StateFileSearchMiddleware(state_key="memory_files"),
    ],
    checkpointer=MemorySaver(),
)

# Use a thread_id to persist state across invocations
config: RunnableConfig = {"configurable": {"thread_id": "my-session"}}

# First invocation: Record some memories
result = agent.invoke(
    {"messages": [HumanMessage("Remember that the project deadline is March 15th and code review deadline is March 10th")]},
    config=config,
)

# The agent creates memory files, which are stored in state
print("Memory files created:", list(result["memory_files"].keys()))

# Second invocation: Search the memories we just recorded
# State is automatically persisted via the checkpointer
result = agent.invoke(
    {"messages": [HumanMessage("Search my memories for project deadlines")]},
    config=config,
)
print(result["messages"][-1].content)
```

Copy

```
Memory files created: ['/memories/project_info.md']
```

Copy

```
I found your project deadlines in my memory! Here's what I have recorded:

## Important Deadlines
- **Code Review Deadline:** March 10th
- **Project Deadline:** March 15th

## Notes
- Code review must be completed 5 days before final project deadline
- Need to ensure all code is ready for review by March 10th

Is there anything specific about these deadlines you'd like to know or update?
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/middleware/anthropic.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.