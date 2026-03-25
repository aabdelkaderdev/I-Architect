<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/exa_search -->

Exa is a search engine fully designed for use by LLMs. Search for documents on the internet using **natural language queries**, then retrieve **cleaned HTML content** from desired documents.
Unlike keyword-based search (Google), Exa’s neural search capabilities allow it to semantically understand queries and return relevant documents. For example, we could search `"fascinating article about cats"` and compare the search results from [Google](https://www.google.com/search?q=fascinating+article+about+cats) and [Exa](https://search.exa.ai/search?q=fascinating%20article%20about%20cats&autopromptString=Here%20is%20a%20fascinating%20article%20about%20cats%3A). Google gives us SEO-optimized listicles based on the keyword “fascinating”. Exa just works.
This notebook goes over how to use Exa Search with LangChain.

## [​](#setup) Setup

### [​](#installation) Installation

Install the LangChain Exa integration package:

Copy

```
pip install -qU langchain-exa

# and some deps for this notebook
pip install -qU langchain langchain-openai langchain-community
```

### [​](#credentials) Credentials

You’ll need an Exa API key to use this integration. Get $10 free credit (plus more by completing certain actions like making your first search) by [signing up here](https://dashboard.exa.ai/).

Copy

```
import getpass
import os

if not os.environ.get("EXA_API_KEY"):
    os.environ["EXA_API_KEY"] = getpass.getpass("Exa API key:\n")
```

## [​](#using-exasearchresults-tool) Using ExaSearchResults tool

ExaSearchResults is a tool that can be used with LangChain agents to perform Exa searches. It provides a more structured interface for search operations:

Copy

```
from langchain_exa import ExaSearchResults

# Initialize the ExaSearchResults tool
search_tool = ExaSearchResults(exa_api_key=os.environ["EXA_API_KEY"])

# Perform a search query
search_results = search_tool._run(
    query="When was the last time the New York Knicks won the NBA Championship?",
    num_results=5,
    text_contents_options=True,
    highlights=True,
)

print("Search Results:", search_results)
```

### [​](#advanced-features-for-exasearchresults) Advanced features for ExaSearchResults

You can use advanced search options like controlling search type, live crawling, and content filtering:

Copy

```
# Perform a search query with advanced options
search_results = search_tool._run(
    query="Latest AI research papers",
    num_results=10,  # Number of results (1-100)
    type="auto",  # Can be "neural", "keyword", or "auto"
    livecrawl="always",  # Can be "always", "fallback", or "never"
    text_contents_options={"max_characters": 2000},  # Limit text length
    summary={"query": "generate one liner"},  # Custom summary prompt
)

print("Advanced Search Results:")
print(search_results)
```

## [​](#using-exafindsimilarresults-tool) Using ExaFindSimilarResults tool

ExaFindSimilarResults allows you to find webpages similar to a given URL. This is useful for finding related content or competitive analysis:

Copy

```
from langchain_exa import ExaFindSimilarResults

# Initialize the ExaFindSimilarResults tool
find_similar_tool = ExaFindSimilarResults(exa_api_key=os.environ["EXA_API_KEY"])

# Find similar results based on a URL
similar_results = find_similar_tool._run(
    url="http://espn.com", num_results=5, text_contents_options=True, highlights=True
)

print("Similar Results:", similar_results)
```

## [​](#use-within-an-agent) Use within an Agent

We can use the ExaSearchResults and ExaFindSimilarResults tools with a LangGraph agent. This gives the agent the ability to dynamically search for information and find similar content based on the user’s queries.
First, let’s set up the language model. You’ll need to provide your OpenAI API key:

Copy

```
import getpass

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API key:\n")
```

We will need to install langgraph:

Copy

```
pip install -qU langgraph
```

Copy

```
from langchain.chat_models import init_chat_model
from langchain_exa import ExaFindSimilarResults, ExaSearchResults
from langchain.agents import create_agent

# Initialize the language model
model = init_chat_model(model="gpt-4.1", model_provider="openai", temperature=0)

# Initialize Exa Tools
exa_search = ExaSearchResults(
    exa_api_key=os.environ["EXA_API_KEY"],
    max_results=5,
)

exa_find_similar = ExaFindSimilarResults(
    exa_api_key=os.environ["EXA_API_KEY"],
    max_results=5,
)

# Create agent with both tools
agent = create_agent(model, [exa_search, exa_find_similar])

# Example 1: Basic search
user_input = "What are the latest developments in quantum computing?"

for step in agent.stream(
    {"messages": user_input},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
```

## [​](#using-exasearchretriever) Using ExaSearchRetriever

ExaSearchRetriever is a retriever that uses Exa Search to retrieve relevant documents.

**The `max_characters` parameter for **TextContentsOptions** used to be called `max_length` which is now deprecated. Make sure to use `max_characters` instead.**

### [​](#basic-usage) Basic usage

Here’s a simple example of using ExaSearchRetriever:

Copy

```
from langchain_exa import ExaSearchRetriever

# Create a new instance of the ExaSearchRetriever
exa = ExaSearchRetriever(exa_api_key=os.environ["EXA_API_KEY"])

# Search for a query and save the results
results = exa.invoke("What is the capital of France?")

# Print the results
print(results)
```

### [​](#advanced-features) Advanced features

You can use advanced features like controlling the number of results, search type, live crawling, summaries, and text content options:

Copy

```
from langchain_exa import ExaSearchRetriever

# Create a new instance with advanced options
exa = ExaSearchRetriever(
    exa_api_key=os.environ["EXA_API_KEY"],
    k=20,  # Number of results (1-100)
    type="auto",  # Can be "neural", "keyword", or "auto"
    livecrawl="always",  # Can be "always", "fallback", or "never"
    text_contents_options={"max_characters": 3000},  # Limit text length
    # Custom prompt for an LLM generated summary of page content
    summary={"query": "generate one line summary in simple words."},
)

# Search with advanced options
results = exa.invoke("Latest developments in quantum computing")
print(f"Found {len(results)} results")
for result in results[:3]:  # Print first 3 results
    print(f"Title: {result.metadata.get('title', 'N/A')}")
    print(f"URL: {result.metadata.get('url', 'N/A')}")
    print(f"Summary: {result.metadata.get('summary', 'N/A')}")
    print("-" * 80)
```

---

## [​](#api-reference) API reference

For detailed documentation of all Exa API features and configurations, visit the [Exa API documentation](https://docs.exa.ai/).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/exa_search.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.