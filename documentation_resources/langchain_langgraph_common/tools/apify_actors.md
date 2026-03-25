<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/apify_actors -->

> [Apify Actors](https://docs.apify.com/platform/actors) are cloud programs designed for a wide range of web scraping, crawling, and data extraction tasks. These actors facilitate automated data gathering from the web, enabling users to extract, process, and store information efficiently. Actors can be used to perform tasks like scraping e-commerce sites for product details, monitoring price changes, or gathering search engine results. They integrate seamlessly with [Apify Datasets](https://docs.apify.com/platform/storage/dataset), allowing the structured data collected by actors to be stored, managed, and exported in formats like JSON, CSV, or Excel for further analysis or use.

## [​](#overview) Overview

This notebook walks you through using [Apify Actors](https://docs.apify.com/platform/actors) with LangChain to automate web scraping and data extraction. The `langchain-apify` package integrates Apify’s cloud-based tools with LangChain agents, enabling efficient data collection and processing for AI applications.

### [​](#integration-details) Integration details

| Class | Package | Serializable | [JS support](https://js.langchain.com/docs/integrations/tools/apify_actors) | Version |
| --- | --- | --- | --- | --- |
| [ApifyActorsTool](https://github.com/apify/langchain-apify) | [langchain-apify](https://pypi.org/project/langchain-apify/) | ✅ | ✅ |  |

### [​](#tool-features) Tool features

| Returns artifact | Native async | Return data | Pricing |
| --- | --- | --- | --- |
| ❌ | ✅ | Actor output (varies by Actor) | Pay-per-use, [free tier available](https://apify.com/pricing) |

## [​](#setup) Setup

This integration lives in the [langchain-apify](https://pypi.org/project/langchain-apify/) package. The package can be installed using pip.

Copy

```
pip install langchain-apify
```

### [​](#prerequisites) Prerequisites

- **Apify account**: Register your free [Apify account](https://console.apify.com/sign-up).
- **Apify API token**: Learn how to get your API token in the [Apify documentation](https://docs.apify.com/platform/integrations/api).

Copy

```
import os

os.environ["APIFY_TOKEN"] = "your-apify-token"
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
```

### [​](#pricing) Pricing

Apify uses pay-per-use pricing with a free tier available.
Pricing varies by Actor—some Actors are free (you only pay for platform usage), while others charge per result or event.

## [​](#instantiation) Instantiation

Here we instantiate the `ApifyActorsTool` to be able to call [RAG Web Browser](https://apify.com/apify/rag-web-browser) Apify Actor. This Actor provides web browsing functionality for AI and LLM applications, similar to the web browsing feature in ChatGPT. Any Actor from the [Apify Store](https://apify.com/store) can be used in this way.

Copy

```
from langchain_apify import ApifyActorsTool

tool = ApifyActorsTool("apify/rag-web-browser")
```

## [​](#invocation) Invocation

The `ApifyActorsTool` takes a single argument, which is `run_input` - a dictionary that is passed as a run input to the Actor. Run input schema documentation can be found in the input section of the Actor details page. See [RAG Web Browser input schema](https://apify.com/apify/rag-web-browser/input-schema).

Copy

```
tool.invoke({"run_input": {"query": "what is apify?", "maxResults": 2}})
```

## [​](#chaining) Chaining

We can provide the created tool to an [agent](https://python.langchain.com/docs/tutorials/agents/). When asked to search for information, the agent will call the Apify Actor, which will search the web, and then retrieve the search results.

Copy

```
pip install langgraph langchain-openai
```

Copy

```
from langchain.messages import ToolMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

model = ChatOpenAI(model="gpt-5-mini")
tools = [tool]
graph = create_agent(model, tools=tools)
```

Copy

```
inputs = {"messages": [("user", "search for what is Apify")]}
for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    # skip tool messages
    if isinstance(message, ToolMessage):
        continue
    message.pretty_print()
```

Copy

```
================================ Human Message =================================

search for what is Apify
================================== Ai Message ==================================
Tool Calls:
  apify_actor_apify_rag-web-browser (call_27mjHLzDzwa5ZaHWCMH510lm)
 Call ID: call_27mjHLzDzwa5ZaHWCMH510lm
  Args:
    run_input: {"run_input":{"query":"Apify","maxResults":3,"outputFormats":["markdown"]}}
================================== Ai Message ==================================

Apify is a comprehensive platform for web scraping, browser automation, and data extraction. It offers a wide array of tools and services that cater to developers and businesses looking to extract data from websites efficiently and effectively. Here's an overview of Apify:

1. **Ecosystem and Tools**:
   - Apify provides an ecosystem where developers can build, deploy, and publish data extraction and web automation tools called Actors.
   - The platform supports various use cases such as extracting data from social media platforms, conducting automated browser-based tasks, and more.

2. **Offerings**:
   - Apify offers over 10,000 ready-made scraping tools and code templates.
   - Users can also build custom solutions or hire Apify's professional services for more tailored data extraction needs.

3. **Technology and Integration**:
   - The platform supports integration with popular tools and services like Zapier, GitHub, Google Sheets, Pinecone, and more.
   - Apify supports open-source tools and technologies such as JavaScript, Python, Puppeteer, Playwright, Selenium, and its own Crawlee library for web crawling and browser automation.

4. **Community and Learning**:
   - Apify hosts a community on Discord where developers can get help and share expertise.
   - It offers educational resources through the Web Scraping Academy to help users become proficient in data scraping and automation.

5. **Enterprise Solutions**:
   - Apify provides enterprise-grade web data extraction solutions with high reliability, 99.95% uptime, and compliance with SOC2, GDPR, and CCPA standards.

For more information, you can visit [Apify's official website](https://apify.com/) or their [GitHub page](https://github.com/apify) which contains their code repositories and further details about their projects.
```

## [​](#additional-actor-examples) Additional Actor examples

The Apify Store contains thousands of prebuilt Actors. Here are examples of other popular Actors:

### [​](#instagram-scraper) Instagram Scraper

Copy

```
from langchain_apify import ApifyActorsTool

instagram_tool = ApifyActorsTool("apify/instagram-scraper")

# Scrape Instagram posts
result = instagram_tool.invoke({
    "run_input": {
        "directUrls": ["https://www.instagram.com/humansofny/"],
        "resultsLimit": 10
    }
})
```

### [​](#google-search-results-scraper) Google Search Results Scraper

Copy

```
google_search_tool = ApifyActorsTool("apify/google-search-scraper")

# Scrape Google Search results
result = google_search_tool.invoke({
    "run_input": {
        "queries": "langchain python tutorial",
        "maxPagesPerQuery": 1
    }
})
```

Browse the [Apify Store](https://apify.com/store) to discover more Actors for your use case.

## [​](#when-to-use-apify) When to use Apify

Apify is ideal when you need:

- **Access to thousands of prebuilt Actors** for various platforms (social media, e-commerce, search engines, etc.)
- **Custom web scraping and automation workflows** beyond simple search
- **Infrastructure-free scraping** (a serverless platform handles scaling and maintenance)
- **Flexible Actor ecosystem** – run any Actor from the Apify Store

---

## [​](#api-reference) API reference

For more information on how to use this integration, see the [git repository](https://github.com/apify/langchain-apify) or the [Apify integration documentation](https://docs.apify.com/platform/integrations/langgraph).

---

## [​](#using-apify-mcp-server) Using Apify MCP Server

Unsure which Actor to use or what parameters it requires?
The [Apify MCP (Model Context Protocol) server](https://mcp.apify.com) can help you discover available Actors, explore their input schemas, and understand parameter requirements through the Model Context Protocol.
To use the Apify MCP server with LangChain:

Copy

```
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient({
    "apify": {
        "transport": "http",
        "url": "https://mcp.apify.com",
        "headers": {
            "Authorization": f"Bearer {os.environ['APIFY_TOKEN']}",
        },
    }
})

tools = await client.get_tools()
agent = create_agent("gpt-5-mini", tools)
```

For more information, see the [LangChain MCP documentation](/oss/python/langchain/mcp) and [Apify MCP server](https://mcp.apify.com).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/apify_actors.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.