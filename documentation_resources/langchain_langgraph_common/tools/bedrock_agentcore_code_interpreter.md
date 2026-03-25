<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/bedrock_agentcore_code_interpreter -->

[Amazon Bedrock AgentCore Code Interpreter](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-tool.html) enables agents to execute code in secure, managed sandbox environments. Agents can run Python, JavaScript, and TypeScript code for calculations, data analysis, file manipulation, and visualizations.

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Serializable | [JS support](https://js.langchain.com/docs/integrations/tools/) | Version |
| --- | --- | --- | --- | --- |
| [CodeInterpreterToolkit](https://github.com/langchain-ai/langchain-aws/tree/main/libs/aws/langchain_aws/tools) | [langchain-aws](https://pypi.org/project/langchain-aws/) | ✅ | ❌ |  |

### [​](#tool-features) Tool features

| [Returns artifact](/oss/python/langchain/tools) | Native async | Return data | Pricing |
| --- | --- | --- | --- |
| ✅ | ✅ | Text, Files, Images | Pay-per-use (AWS) |

### [​](#available-tools) Available tools

The toolkit provides multiple tools for code execution and file management:

| Tool | Description |
| --- | --- |
| `execute_code` | Run Python/JavaScript/TypeScript code with persistent state |
| `execute_command` | Run shell commands in the environment |
| `read_files` | Read content of files in the environment |
| `write_files` | Create or update files |
| `list_files` | List files in directories |
| `delete_files` | Remove files from the environment |
| `upload_file` | Upload files with semantic descriptions |
| `install_packages` | Install Python packages |
| `start_command_execution` | Start a long-running command asynchronously |
| `get_task` | Check status of an async task by task\_id |
| `stop_task` | Stop a running async task by task\_id |

## [​](#setup) Setup

The integration lives in the `langchain-aws` package, which wraps the `bedrock-agentcore` SDK.

pip

uv

Copy

```
pip install -U langchain-aws bedrock-agentcore
```

### [​](#credentials) Credentials

You need AWS credentials configured with permissions for Bedrock AgentCore Code Interpreter. See the [Amazon Bedrock AgentCore documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) for required IAM permissions.
It’s also helpful (but not needed) to set up LangSmith for best-in-class observability:

Copy

```
import os

os.environ["LANGSMITH_API_KEY"] = "your-api-key"
os.environ["LANGSMITH_TRACING"] = "true"
```

## [​](#instantiation) Instantiation

The toolkit is created using an **async** factory function:

Copy

```
from langchain_aws.tools import create_code_interpreter_toolkit

# Create toolkit and get tools (async)
toolkit, code_tools = await create_code_interpreter_toolkit(region="us-west-2")
```

## [​](#invocation) Invocation

### [​](#direct-tool-usage) Direct tool usage

Get specific tools and invoke them:

Copy

```
# Get tools by name
tools_by_name = toolkit.get_tools_by_name()

# Execute Python code
result = tools_by_name["execute_code"].invoke({
    "code": """
import numpy as np
data = [1, 2, 3, 4, 5]
print(f"Mean: {np.mean(data)}")
print(f"Sum: {np.sum(data)}")
""",
    "language": "python"
})
print(result)
```

### [​](#use-within-an-agent) Use within an agent

Copy

```
import asyncio
from langchain.agents import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_aws.tools import create_code_interpreter_toolkit

async def main():
    # Create toolkit
    toolkit, code_tools = await create_code_interpreter_toolkit(region="us-west-2")

    # Initialize chat model
    llm = init_chat_model(
        "us.anthropic.claude-sonnet-4-20250514-v1:0",
        model_provider="bedrock_converse",
    )

    # Create agent with code interpreter tools
    agent = create_react_agent(
        model=llm,
        tools=code_tools,
    )

    # Create config with thread_id for session isolation
    config = {"configurable": {"thread_id": "session-123"}}

    # Run the agent
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Calculate the factorial of 10"}]},
        config=config
    )
    print(result["messages"][-1].content)

    # Clean up when done
    await toolkit.cleanup()

asyncio.run(main())
```

## [​](#thread-based-session-isolation) Thread-based session isolation

The toolkit supports multiple concurrent sessions via `thread_id`. Each thread maintains its own code interpreter session with isolated state:

Copy

```
# Different threads have isolated sessions
config_user1 = {"configurable": {"thread_id": "user-1"}}
config_user2 = {"configurable": {"thread_id": "user-2"}}

# Variables defined in user-1's session won't exist in user-2's session
await agent.ainvoke(
    {"messages": [{"role": "user", "content": "Set x = 100"}]},
    config=config_user1
)

await agent.ainvoke(
    {"messages": [{"role": "user", "content": "What is x?"}]},  # x is undefined here
    config=config_user2
)
```

## [​](#working-with-files) Working with files

### [​](#write-and-read-files) Write and read files

Copy

```
tools_by_name = toolkit.get_tools_by_name()

# Write a file
tools_by_name["write_files"].invoke({
    "files": [{"path": "data.csv", "text": "name,value\nAlice,100\nBob,200"}]
})

# Read it back
content = tools_by_name["read_files"].invoke({"paths": ["data.csv"]})
print(content)

# List files in current directory
files = tools_by_name["list_files"].invoke({"directory_path": "."})
print(files)
```

### [​](#upload-files-with-descriptions) Upload files with descriptions

Copy

```
tools_by_name["upload_file"].invoke({
    "path": "sales.csv",
    "content": "date,revenue,product\n2024-01-01,1000,Widget\n2024-01-02,1500,Gadget",
    "description": "Sales data with columns: date, revenue, product_id"
})
```

## [​](#installing-packages) Installing packages

Copy

```
tools_by_name["install_packages"].invoke({
    "packages": ["pandas>=2.0", "matplotlib", "scikit-learn"],
    "upgrade": False
})
```

## [​](#async-task-management) Async task management

For long-running commands, you can start them asynchronously and check their status:

Copy

```
tools_by_name = toolkit.get_tools_by_name()
config = {"configurable": {"thread_id": "session-123"}}

# Start a long-running command asynchronously
result = tools_by_name["start_command_execution"].invoke(
    {"command": "python long_running_script.py"},
    config=config
)
# Returns a task_id

# Check task status
status = tools_by_name["get_task"].invoke(
    {"task_id": "task-abc123"},
    config=config
)
print(status)

# Stop a running task if needed
tools_by_name["stop_task"].invoke(
    {"task_id": "task-abc123"},
    config=config
)
```

## [​](#session-cleanup) Session cleanup

Always clean up sessions when done to release resources:

Copy

```
# Clean up all sessions
await toolkit.cleanup()

# Or clean up a specific thread's session
await toolkit.cleanup(thread_id="session-123")
```

---

## [​](#api-reference) API reference

For detailed documentation of all features and configurations, see:

- [langchain-aws API reference](https://python.langchain.com/api_reference/aws/)
- [Amazon Bedrock AgentCore documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/bedrock_agentcore_code_interpreter.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.