<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/bedrock_agentcore_browser -->

[Amazon Bedrock AgentCore Browser](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-tool.html) enables agents to interact with web pages through a managed Chrome browser. Agents can navigate websites, extract content, fill forms, click elements, and take screenshots in a secure, managed environment.

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Serializable | [JS support](https://js.langchain.com/docs/integrations/tools/) | Version |
| --- | --- | --- | --- | --- |
| [BrowserToolkit](https://github.com/langchain-ai/langchain-aws/tree/main/libs/aws/langchain_aws/tools) | [langchain-aws](https://pypi.org/project/langchain-aws/) | ✅ | ❌ |  |

### [​](#tool-features) Tool features

| [Returns artifact](/oss/python/langchain/tools) | Native async | Supports browser interaction | Pricing |
| --- | --- | --- | --- |
| ✅ | ✅ | ✅ | Pay-per-use (AWS) |

### [​](#available-tools) Available tools

The toolkit provides multiple tools for browser automation:

| Tool | Description |
| --- | --- |
| `navigate_browser` | Navigate to a URL |
| `click_element` | Click on an element using CSS selector |
| `type_text` | Type text into an input field |
| `extract_text` | Extract all text content from the page |
| `extract_hyperlinks` | Extract all hyperlinks from the page |
| `get_elements` | Get elements matching a CSS selector |
| `current_webpage` | Get the current page URL and title |
| `navigate_back` | Go back to the previous page |
| `take_screenshot` | Take a screenshot of the page |
| `scroll_page` | Scroll the page in a direction |
| `wait_for_element` | Wait for an element to appear |

## [​](#setup) Setup

The integration lives in the `langchain-aws` package. It also requires `playwright` and `beautifulsoup4` for browser automation and HTML parsing.

pip

uv

Copy

```
pip install -U langchain-aws bedrock-agentcore playwright beautifulsoup4
playwright install chromium
```

### [​](#credentials) Credentials

You need AWS credentials configured with permissions for Bedrock AgentCore Browser. See the [Amazon Bedrock AgentCore documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) for required IAM permissions.
It’s also helpful (but not needed) to set up LangSmith for best-in-class observability:

Copy

```
import os

os.environ["LANGSMITH_API_KEY"] = "your-api-key"
os.environ["LANGSMITH_TRACING"] = "true"
```

## [​](#instantiation) Instantiation

The toolkit is created using a factory function:

Copy

```
from langchain_aws.tools import create_browser_toolkit

# Create toolkit and get tools
toolkit, browser_tools = create_browser_toolkit(region="us-west-2")
```

## [​](#invocation) Invocation

### [​](#direct-tool-usage) Direct tool usage

Get specific tools and invoke them:

Copy

```
# Get tools by name
tools_by_name = toolkit.get_tools_by_name()

# Navigate to a URL (requires config with thread_id)
config = {"configurable": {"thread_id": "session-123"}}

result = tools_by_name["navigate_browser"].invoke(
    {"url": "https://example.com"},
    config=config
)
print(result)

# Extract text from the page
text = tools_by_name["extract_text"].invoke({}, config=config)
print(text)
```

### [​](#use-within-an-agent) Use within an agent

Copy

```
import asyncio
from langchain.agents import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_aws.tools import create_browser_toolkit

async def main():
    # Create toolkit
    toolkit, browser_tools = create_browser_toolkit(region="us-west-2")

    # Initialize chat model
    llm = init_chat_model(
        "us.anthropic.claude-sonnet-4-20250514-v1:0",
        model_provider="bedrock_converse",
    )

    # Create agent with browser tools
    agent = create_react_agent(
        model=llm,
        tools=browser_tools,
    )

    # Create config with thread_id for session isolation
    config = {"configurable": {"thread_id": "research-session"}}

    # Run the agent
    result = await agent.ainvoke(
        {"messages": [{
            "role": "user",
            "content": "Navigate to https://example.com and tell me the main heading"
        }]},
        config=config
    )
    print(result["messages"][-1].content)

    # Clean up when done
    await toolkit.cleanup()

asyncio.run(main())
```

## [​](#thread-based-session-isolation) Thread-based session isolation

The toolkit maintains separate browser sessions for each `thread_id`. This enables concurrent usage without interference:

Copy

```
# Each thread gets its own browser session
config_user1 = {"configurable": {"thread_id": "user-1"}}
config_user2 = {"configurable": {"thread_id": "user-2"}}

# User 1 navigates to site A
tools_by_name["navigate_browser"].invoke(
    {"url": "https://site-a.com"},
    config=config_user1
)

# User 2 navigates to site B (different browser session)
tools_by_name["navigate_browser"].invoke(
    {"url": "https://site-b.com"},
    config=config_user2
)
```

## [​](#browser-actions) Browser actions

### [​](#navigation) Navigation

Copy

```
config = {"configurable": {"thread_id": "session-123"}}

# Navigate to URL
tools_by_name["navigate_browser"].invoke({"url": "https://example.com"}, config=config)

# Go back
tools_by_name["navigate_back"].invoke({}, config=config)

# Get current page info
current = tools_by_name["current_webpage"].invoke({}, config=config)
print(current)  # URL and title
```

### [​](#interacting-with-elements) Interacting with elements

Copy

```
# Click an element
tools_by_name["click_element"].invoke({"selector": "#submit-button"}, config=config)

# Type into an input field
tools_by_name["type_text"].invoke({
    "selector": "input[name='search']",
    "text": "search query"
}, config=config)

# Wait for element to appear
tools_by_name["wait_for_element"].invoke({
    "selector": ".results",
    "timeout": 10000,  # 10 seconds
    "state": "visible"
}, config=config)
```

### [​](#extracting-content) Extracting content

Copy

```
# Extract all text
text = tools_by_name["extract_text"].invoke({}, config=config)

# Extract all hyperlinks
links = tools_by_name["extract_hyperlinks"].invoke({}, config=config)

# Get specific elements
elements = tools_by_name["get_elements"].invoke(
    {"selector": "article h2"},
    config=config
)
```

### [​](#screenshots-and-scrolling) Screenshots and scrolling

Copy

```
# Take screenshot of visible viewport (returns base64 image)
screenshot = tools_by_name["take_screenshot"].invoke(
    {"capture_type": "viewport"},
    config=config
)

# Take screenshot of entire scrollable page
full_screenshot = tools_by_name["take_screenshot"].invoke(
    {"capture_type": "full_page"},
    config=config
)

# Scroll the page
tools_by_name["scroll_page"].invoke({
    "direction": "down",
    "amount": 500  # pixels
}, config=config)
```

## [​](#session-cleanup) Session cleanup

Always clean up browser sessions when done to release resources:

Copy

```
# Clean up all browser sessions
await toolkit.cleanup()
```

> **Note:** While `create_browser_toolkit()` is synchronous, the `cleanup()` method is asynchronous and must be awaited.

## [​](#concurrency-protection) Concurrency protection

The toolkit includes built-in concurrency protection. Each browser session is tied to a specific `thread_id`, and attempting to access the same session while it’s already in use will raise a `RuntimeError`. Use different `thread_id` values for concurrent operations.

Copy

```
# Good: Different thread IDs for concurrent operations
config_a = {"configurable": {"thread_id": "task-a"}}
config_b = {"configurable": {"thread_id": "task-b"}}

# These can run concurrently without conflicts
await asyncio.gather(
    agent.ainvoke({"messages": [...]}, config=config_a),
    agent.ainvoke({"messages": [...]}, config=config_b),
)
```

---

## [​](#api-reference) API reference

For detailed documentation of all features and configurations, see:

- [langchain-aws API reference](https://python.langchain.com/api_reference/aws/)
- [Amazon Bedrock AgentCore documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/bedrock_agentcore_browser.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.