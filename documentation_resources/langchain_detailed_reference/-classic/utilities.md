<!-- Source: https://reference.langchain.com/python/langchain-classic/utilities -->

Modulev1.2.13 (latest)●Since v1.0

# utilities

**Utilities** are the integrations with third-part systems and packages.

Other LangChain classes use **Utilities** to interact with third-part systems
and packages.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/utilities/DEPRECATED_LOOKUP)

## Functions

[function

create\_importer

Create a function that helps retrieve objects from their new locations.

The goal of this function is to help users transition from deprecated
imports to new imports.

The function will raise deprecation warning on loops using
`deprecated_lookups` or `fallback_module`.

Module lookups will import without deprecation warnings (used to speed
up imports from large namespaces like llms or chat models).

This function should ideally only be used with deprecated imports not with
existing imports that are valid, as in addition to raising deprecation warnings
the dynamic imports can create other issues for developers (e.g.,
loss of type information, IDE support for going to definition etc).](/python/langchain-classic/_api/module_import/create_importer)

## Modules

[module

openweathermap](/python/langchain-classic/utilities/openweathermap)[module

sql\_database](/python/langchain-classic/utilities/sql_database)[module

google\_jobs](/python/langchain-classic/utilities/google_jobs)[module

redis](/python/langchain-classic/utilities/redis)[module

reddit\_search](/python/langchain-classic/utilities/reddit_search)[module

arcee](/python/langchain-classic/utilities/arcee)[module

gitlab](/python/langchain-classic/utilities/gitlab)[module

powerbi](/python/langchain-classic/utilities/powerbi)[module

tensorflow\_datasets](/python/langchain-classic/utilities/tensorflow_datasets)[module

tavily\_search](/python/langchain-classic/utilities/tavily_search)[module

google\_serper](/python/langchain-classic/utilities/google_serper)[module

stackexchange](/python/langchain-classic/utilities/stackexchange)[module

arxiv](/python/langchain-classic/utilities/arxiv)[module

clickup](/python/langchain-classic/utilities/clickup)[module

spark\_sql](/python/langchain-classic/utilities/spark_sql)[module

portkey](/python/langchain-classic/utilities/portkey)[module

google\_finance](/python/langchain-classic/utilities/google_finance)[module

alpha\_vantage](/python/langchain-classic/utilities/alpha_vantage)[module

searchapi](/python/langchain-classic/utilities/searchapi)[module

google\_trends](/python/langchain-classic/utilities/google_trends)[module

google\_places\_api](/python/langchain-classic/utilities/google_places_api)[module

openapi](/python/langchain-classic/utilities/openapi)[module

merriam\_webster](/python/langchain-classic/utilities/merriam_webster)[module

requests](/python/langchain-classic/utilities/requests)[module

google\_lens](/python/langchain-classic/utilities/google_lens)[module

apify](/python/langchain-classic/utilities/apify)[module

google\_search](/python/langchain-classic/utilities/google_search)[module

python

For backwards compatibility.](/python/langchain-classic/utilities/python)[module

graphql](/python/langchain-classic/utilities/graphql)[module

github](/python/langchain-classic/utilities/github)[module

serpapi](/python/langchain-classic/utilities/serpapi)[module

duckduckgo\_search](/python/langchain-classic/utilities/duckduckgo_search)[module

golden\_query](/python/langchain-classic/utilities/golden_query)[module

wolfram\_alpha](/python/langchain-classic/utilities/wolfram_alpha)[module

steam](/python/langchain-classic/utilities/steam)[module

opaqueprompts](/python/langchain-classic/utilities/opaqueprompts)[module

pubmed](/python/langchain-classic/utilities/pubmed)[module

zapier](/python/langchain-classic/utilities/zapier)[module

metaphor\_search](/python/langchain-classic/utilities/metaphor_search)[module

jira](/python/langchain-classic/utilities/jira)[module

brave\_search](/python/langchain-classic/utilities/brave_search)[module

twilio](/python/langchain-classic/utilities/twilio)[module

vertexai](/python/langchain-classic/utilities/vertexai)[module

outline](/python/langchain-classic/utilities/outline)[module

max\_compute](/python/langchain-classic/utilities/max_compute)[module

google\_scholar](/python/langchain-classic/utilities/google_scholar)[module

dalle\_image\_generator](/python/langchain-classic/utilities/dalle_image_generator)[module

scenexplain](/python/langchain-classic/utilities/scenexplain)[module

bibtex](/python/langchain-classic/utilities/bibtex)[module

nasa](/python/langchain-classic/utilities/nasa)[module

dataforseo\_api\_search](/python/langchain-classic/utilities/dataforseo_api_search)[module

wikipedia](/python/langchain-classic/utilities/wikipedia)[module

searx\_search](/python/langchain-classic/utilities/searx_search)[module

anthropic](/python/langchain-classic/utilities/anthropic)[module

bing\_search](/python/langchain-classic/utilities/bing_search)[module

asyncio

Shims for asyncio features that may be missing from older python versions.](/python/langchain-classic/utilities/asyncio)[module

awslambda](/python/langchain-classic/utilities/awslambda)


