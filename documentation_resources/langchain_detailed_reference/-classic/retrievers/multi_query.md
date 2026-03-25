<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/multi_query -->

Modulev1.2.13 (latest)●Since v1.0

# multi\_query

## Attributes

[attribute

logger](/python/langchain-classic/retrievers/multi_query/logger)[attribute

DEFAULT\_QUERY\_PROMPT](/python/langchain-classic/retrievers/multi_query/DEFAULT_QUERY_PROMPT)

## Classes

[class

LineListOutputParser

Output parser for a list of lines.](/python/langchain-classic/retrievers/multi_query/LineListOutputParser)[class

MultiQueryRetriever

Given a query, use an LLM to write a set of queries.

Retrieve docs for each query. Return the unique union of all retrieved docs.](/python/langchain-classic/retrievers/multi_query/MultiQueryRetriever)[deprecatedclass

LLMChain

Chain to run queries against LLMs.

This class is deprecated. See below for an example implementation using
LangChain runnables:

```
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

prompt_template = "Tell me a {adjective} joke"
prompt = PromptTemplate(input_variables=["adjective"], template=prompt_template)
model = OpenAI()
chain = prompt | model | StrOutputParser()

chain.invoke("your adjective here")
```](/python/langchain-classic/chains/llm/LLMChain)


