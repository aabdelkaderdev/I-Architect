<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/cloro -->

[cloro](https://cloro.dev) provides tools for monitoring AI platforms and search engines with structured data extraction.

## [​](#setup) Setup

Install the `langchain-cloro` package:

Copy

```
pip install -U langchain-cloro
```

Get your API key from the [cloro dashboard](https://dashboard.cloro.dev) and set it as an environment variable:

Copy

```
import os
os.environ["CLORO_API_KEY"] = "your-api-key"
```

## [​](#google-search-scraper) Google Search scraper

Extract structured data from Google Search results, including organic results, People Also Ask questions, related searches, and optional AI Overview.

Copy

```
from langchain_cloro import CloroGoogleSearch

tool = CloroGoogleSearch()
result = tool.invoke({"query": "best laptops for programming"})
```

### [​](#include-ai-overview) Include AI Overview

Copy

```
result = tool.invoke({
    "query": "best laptops for programming",
    "include_aioverview": True,
    "aioverview_markdown": True
})
```

### [​](#custom-parameters) Custom parameters

Copy

```
result = tool.invoke({
    "query": "python tutorials",
    "country": "GB",  # UK results
    "device": "mobile",  # or "desktop"
    "pages": 3  # Number of pages (1-20)
})
```

## [​](#chatgpt-scraper) ChatGPT scraper

Extract structured data from ChatGPT with shopping cards, entity extraction, and advanced features for monitoring products, prices, and brand mentions.

Copy

```
from langchain_cloro import CloroChatGPT

tool = CloroChatGPT()
result = tool.invoke({"prompt": "What are the best sneakers under $100?"})
```

### [​](#include-raw-response-and-search-queries) Include raw response and search queries

Copy

```
result = tool.invoke({
    "prompt": "best running shoes 2024",
    "include_raw_response": True,
    "include_search_queries": True,
    "country": "US"
})
```

## [​](#gemini-scraper) Gemini scraper

Extract structured data from Google’s Gemini AI with source citations and confidence levels.

Copy

```
from langchain_cloro import CloroGemini

tool = CloroGemini()
result = tool.invoke({"prompt": "Explain quantum entanglement"})
```

### [​](#include-markdown-response) Include markdown response

Copy

```
result = tool.invoke({
    "prompt": "What is machine learning?",
    "include_markdown": True,
    "country": "US"
})
```

## [​](#perplexity-scraper) Perplexity scraper

Extract comprehensive structured data from Perplexity AI with real-time web sources, shopping products, media content, and travel information.

Copy

```
from langchain_cloro import CloroPerplexity

tool = CloroPerplexity()
result = tool.invoke({"prompt": "Best hotels in San Francisco"})
```

## [​](#grok-scraper) Grok scraper

Extract comprehensive structured data from Grok with real-time web sources and enhanced source metadata including preview text, creator details, and images.

Copy

```
from langchain_cloro import CloroGrok

tool = CloroGrok()
result = tool.invoke({"prompt": "Latest news about AI"})
```

## [​](#copilot-scraper) Copilot scraper

Extract structured data from Microsoft Copilot with source citations.

Copy

```
from langchain_cloro import CloroCopilot

tool = CloroCopilot()
result = tool.invoke({"prompt": "What is the capital of France?"})
```

## [​](#use-with-agents) Use with agents

All cloro tools can be used with LangChain agents:

Copy

```
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_cloro import CloroGoogleSearch, CloroChatGPT

# Initialize tools
search_tool = CloroGoogleSearch()
chatgpt_tool = CloroChatGPT()
tools = [search_tool, chatgpt_tool]

# Create agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run agent
result = agent_executor.invoke({"input": "Search for information about AI trends and summarize what you find"})
```

## [​](#response-format) Response format

All cloro tools return JSON-formatted responses with structured data:

Copy

```
import json

result = tool.invoke({"query": "python programming"})
data = json.loads(result)

# Access structured results
if "result" in data:
    if "organicResults" in data["result"]:
        for item in data["result"]["organicResults"]:
            print(f"{item['title']}: {item['link']}")
```

## [​](#api-reference) API reference

- **`CloroGoogleSearch`**: Google Search with AI Overview support
- **`CloroChatGPT`**: ChatGPT monitoring with shopping cards
- **`CloroGemini`**: Google Gemini AI with citations
- **`CloroPerplexity`**: Perplexity AI with sources and media
- **`CloroGrok`**: Grok with enhanced metadata
- **`CloroCopilot`**: Microsoft Copilot monitoring

For more details, visit the [cloro documentation](https://docs.cloro.dev).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/cloro.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.