<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/nimble_search -->

> [Nimble’s Search API](https://docs.nimbleway.com/nimble-sdk/search-api) provides real-time web search by browsing the live web with headless browsers rather than querying prebuilt indexes. The tool handles JavaScript rendering, dynamic content, and complex navigation flows, making it suitable for agent workflows that need access to current web data including content behind pagination, filters, and client-side rendering.

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Serializable | JS support | Package latest |
| --- | --- | --- | --- | --- |
| [NimbleSearchTool](https://github.com/Nimbleway/langchain-nimble) | [langchain-nimble](https://pypi.org/project/langchain-nimble/) | ❌ | ❌ |  |

### [​](#tool-features) Tool features

| Returns artifact | Native async | Return data | Pricing |
| --- | --- | --- | --- |
| ❌ | ✅ | title, URL, content (markdown/plain\_text/HTML), metadata | [Free trial available](https://www.nimbleway.com/) |

**Key Features:**

- **Fast mode & Deep mode**: **Deep mode** (default) for full content extraction with JavaScript rendering, or **Fast mode** for quick SERP-only results
- **AI-generated summaries**: Optional concise answers alongside raw search results
- **Domain and date filtering**: Filter by specific domains or date ranges for precise results
- **Topic-based routing**: Optimized routing for general, news, or location-based queries
- **Flexible output formats**: plain\_text, markdown (default), or simplified\_html
- **Production-ready**: Native async support, automatic retries, connection pooling

## [​](#setup) Setup

The integration lives in the `langchain-nimble` package.

pip

uv

Copy

```
pip install -U langchain-nimble
```

### [​](#credentials) Credentials

You’ll need a Nimble API key to use this tool. Sign up at [Nimble](https://www.nimbleway.com/) to get your API key and access their free trial.

Copy

```
import getpass
import os

if not os.environ.get("NIMBLE_API_KEY"):
    os.environ["NIMBLE_API_KEY"] = getpass.getpass("Nimble API key:\n")
```

## [​](#instantiation) Instantiation

Now we can instantiate the tool:

Copy

```
from langchain_nimble import NimbleSearchTool

# Basic usage - uses environment variable for API key
tool = NimbleSearchTool()
```

## [​](#use-within-an-agent) Use within an agent

We can use the Nimble search tool with an agent to give it dynamic web search capabilities. Here’s a complete example using LangGraph:

Copy

```
import os
import getpass

from langchain_nimble import NimbleSearchTool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API key:\n")
if not os.environ.get("NIMBLE_API_KEY"):
    os.environ["NIMBLE_API_KEY"] = getpass.getpass("Nimble API key:\n")

# Initialize Nimble Search Tool with deep search for comprehensive results
nimble_tool = NimbleSearchTool(
    k=5,
    deep_search=True,
    parsing_type="markdown"
)

# Create agent with the tool
model = init_chat_model(model="gpt-4o", model_provider="openai", temperature=0)
agent = create_agent(model, [nimble_tool])

# Ask the agent a question that requires web search
user_input = "What are the latest developments in quantum computing? Include only sources from academic institutions and reputable tech publications."

for step in agent.stream(
    {"messages": user_input},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
```

Copy

```
================================ Human Message =================================

What are the latest developments in quantum computing? Include only sources from academic institutions and reputable tech publications.

================================== Ai Message ==================================
Tool Calls:
  nimble_search (call_abc123)
 Call ID: call_abc123
  Args:
    query: quantum computing latest developments 2025
    deep_search: True
    include_domains: ['mit.edu', 'stanford.edu', 'nature.com', 'science.org', 'ieee.org']
    k: 5

================================= Tool Message =================================
Name: nimble_search

[{"title": "Breakthrough in Quantum Error Correction | MIT News", "url": "https://news.mit.edu/quantum-error-correction", "content": "# Quantum Error Correction Breakthrough\n\nResearchers at MIT have achieved a significant milestone in quantum error correction...\n\n## Key Findings\n- New error correction codes reduce computational overhead\n- Scalability improvements for larger quantum systems...", "rank": 1}, {"title": "Quantum Computing Advances | Nature", "url": "https://www.nature.com/articles/quantum-2024"...

================================== Ai Message ==================================

Based on recent academic and technical sources, here are the latest developments in quantum computing:

**Error Correction:**
- MIT researchers have achieved breakthroughs in quantum error correction
- New codes significantly reduce computational overhead

**Hardware Advances:**
- Improved qubit coherence times and stability
- Progress toward fault-tolerant quantum computing...
[Agent continues with comprehensive summary]
```

## [​](#advanced-configuration) Advanced configuration

The tool supports extensive configuration for different use cases:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `num_results` | int | 10 | Maximum number of results to return (1-20) |
| `deep_search` | bool | True | **Deep mode** (default) for full content extraction, or **Fast mode** (False) for SERP-only results |
| `topic` | str | ”general” | Optimize search for specific content types: “general”, “news”, or “location” |
| `include_answer` | bool | False | Generate AI-powered summary answer alongside search results |
| `include_domains` | list[str] | None | Whitelist specific domains (e.g., [“wikipedia.org”, “.edu”]) |
| `exclude_domains` | list[str] | None | Blacklist specific domains to filter out |
| `start_date` | str | None | Filter results after date (YYYY-MM-DD or YYYY) |
| `end_date` | str | None | Filter results before date (YYYY-MM-DD or YYYY) |
| `parsing_type` | str | ”markdown” | Output format: “plain\_text”, “markdown”, or “simplified\_html” |
| `locale` | str | ”en” | Search locale (e.g., “en-US”) |
| `country` | str | ”US” | Country code for localized results (e.g., “US”) |
| `api_key` | str | env var | Nimble API key (defaults to NIMBLE\_API\_KEY environment variable) |

## [​](#best-practices) Best Practices

### [​](#fast-mode-vs-deep-mode) Fast mode vs Deep mode

- **Deep mode** (`deep_search=True`, default):
  - Full content extraction from web pages
  - Best for detailed analysis, RAG applications, and comprehensive research
  - Handles JavaScript rendering and dynamic content
- **Fast mode** (`deep_search=False`):
  - Quick SERP-only results with titles and snippets
  - Optimized for high-volume queries where speed is critical
  - Lower cost per query

### [​](#when-to-use-include_answer) When to use include\_answer

- Enable `include_answer=True` when you want a concise, AI-generated summary in addition to the raw search results
- Useful for quick insights without processing all the raw content yourself

### [​](#filtering-tips) Filtering tips

- **Domain filtering**: Use `include_domains` for academic research or when you need trusted sources. Use `exclude_domains` to filter out unwanted content types
- **Date filtering**: Combine `start_date` and `end_date` for time-sensitive queries or recent news
- **Topic routing**: Use `topic` parameter to optimize search for general web content, news articles, or location-based information

### [​](#performance-optimization) Performance optimization

- **Choose the right mode**: Use **Fast mode** (`deep_search=False`) for high-volume queries where speed matters; **Deep mode** (default) for comprehensive content extraction
- Use async operations (`ainvoke`) when running multiple searches concurrently
- Tune `num_results` to the minimum number of results needed to reduce response time
- Leverage domain filtering to focus on quality sources and reduce noise

## [​](#api-reference) API reference

For detailed documentation of all `NimbleSearchRetriever` features and configurations, visit the [Nimble API documentation](https://docs.nimbleway.com/nimble-sdk/search-api).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/nimble_search.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.