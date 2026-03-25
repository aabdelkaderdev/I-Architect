<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/query_constructor/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

LLM Chain for turning a user text query into a structured query.

## Attributes

[attribute

DEFAULT\_EXAMPLES: list](/python/langchain-classic/chains/query_constructor/prompt/DEFAULT_EXAMPLES)[attribute

DEFAULT\_PREFIX: str](/python/langchain-classic/chains/query_constructor/prompt/DEFAULT_PREFIX)[attribute

DEFAULT\_SCHEMA\_PROMPT](/python/langchain-classic/chains/query_constructor/prompt/DEFAULT_SCHEMA_PROMPT)[attribute

DEFAULT\_SUFFIX: str](/python/langchain-classic/chains/query_constructor/prompt/DEFAULT_SUFFIX)[attribute

EXAMPLE\_PROMPT](/python/langchain-classic/chains/query_constructor/prompt/EXAMPLE_PROMPT)[attribute

EXAMPLES\_WITH\_LIMIT: list](/python/langchain-classic/chains/query_constructor/prompt/EXAMPLES_WITH_LIMIT)[attribute

PREFIX\_WITH\_DATA\_SOURCE](/python/langchain-classic/chains/query_constructor/prompt/PREFIX_WITH_DATA_SOURCE)[attribute

SCHEMA\_WITH\_LIMIT\_PROMPT](/python/langchain-classic/chains/query_constructor/prompt/SCHEMA_WITH_LIMIT_PROMPT)[attribute

SUFFIX\_WITHOUT\_DATA\_SOURCE: str](/python/langchain-classic/chains/query_constructor/prompt/SUFFIX_WITHOUT_DATA_SOURCE)[attribute

USER\_SPECIFIED\_EXAMPLE\_PROMPT](/python/langchain-classic/chains/query_constructor/prompt/USER_SPECIFIED_EXAMPLE_PROMPT)

## Functions

[function

get\_parser

Return a parser for the query language.](/python/langchain-classic/chains/query_constructor/parser/get_parser)[function

fix\_filter\_directive

Fix invalid filter directive.](/python/langchain-classic/chains/query_constructor/base/fix_filter_directive)[function

construct\_examples

Construct examples from input-output pairs.](/python/langchain-classic/chains/query_constructor/base/construct_examples)[function

get\_query\_constructor\_prompt

Create query construction prompt.](/python/langchain-classic/chains/query_constructor/base/get_query_constructor_prompt)[function

load\_query\_constructor\_runnable

Load a query constructor runnable chain.](/python/langchain-classic/chains/query_constructor/base/load_query_constructor_runnable)[deprecatedfunction

load\_query\_constructor\_chain

Load a query constructor chain.](/python/langchain-classic/chains/query_constructor/base/load_query_constructor_chain)

## Classes

[class

AttributeInfo

Information about a data source attribute.](/python/langchain-classic/chains/query_constructor/schema/AttributeInfo)[class

StructuredQueryOutputParser

Output parser that parses a structured query.](/python/langchain-classic/chains/query_constructor/base/StructuredQueryOutputParser)[deprecatedclass

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


