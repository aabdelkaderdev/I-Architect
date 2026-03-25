<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/citation_fuzzy_match -->

Modulev1.2.13 (latest)●Since v1.0

# citation\_fuzzy\_match

## Functions

[function

get\_llm\_kwargs

Return the kwargs for the LLMChain constructor.](/python/langchain-classic/chains/openai_functions/utils/get_llm_kwargs)[function

create\_citation\_fuzzy\_match\_runnable

Create a citation fuzzy match Runnable.

Example usage:

```
from langchain_classic.chains import create_citation_fuzzy_match_runnable
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

context = "Alice has blue eyes. Bob has brown eyes. Charlie has green eyes."
question = "What color are Bob's eyes?"

chain = create_citation_fuzzy_match_runnable(model)
chain.invoke({"question": question, "context": context})
```](/python/langchain-classic/chains/openai_functions/citation_fuzzy_match/create_citation_fuzzy_match_runnable)[deprecatedfunction

create\_citation\_fuzzy\_match\_chain

Create a citation fuzzy match chain.](/python/langchain-classic/chains/openai_functions/citation_fuzzy_match/create_citation_fuzzy_match_chain)

## Classes

[class

FactWithEvidence

Class representing a single statement.

Each fact has a body and a list of sources.
If there are multiple facts make sure to break them apart
such that each one only uses a set of sources that are relevant to it.](/python/langchain-classic/chains/openai_functions/citation_fuzzy_match/FactWithEvidence)[class

QuestionAnswer

A question and its answer as a list of facts.

Each fact should have a source.
Each sentence contains a body and a list of sources.](/python/langchain-classic/chains/openai_functions/citation_fuzzy_match/QuestionAnswer)[deprecatedclass

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


