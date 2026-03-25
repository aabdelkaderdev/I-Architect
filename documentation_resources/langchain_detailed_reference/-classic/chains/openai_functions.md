<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions -->

Modulev1.2.13 (latest)●Since v1.0

# openai\_functions

## Functions

[function

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
```](/python/langchain-classic/chains/openai_functions/citation_fuzzy_match/create_citation_fuzzy_match_runnable)[function

get\_openai\_output\_parser

Get the appropriate function output parser given the user functions.](/python/langchain-classic/chains/structured_output/base/get_openai_output_parser)[deprecatedfunction

create\_openai\_fn\_chain

[Legacy] Create an LLM chain that uses OpenAI functions.](/python/langchain-classic/chains/openai_functions/base/create_openai_fn_chain)[deprecatedfunction

create\_structured\_output\_chain

[Legacy] Create an LLMChain that uses an OpenAI function to get a structured output.](/python/langchain-classic/chains/openai_functions/base/create_structured_output_chain)[deprecatedfunction

create\_citation\_fuzzy\_match\_chain

Create a citation fuzzy match chain.](/python/langchain-classic/chains/openai_functions/citation_fuzzy_match/create_citation_fuzzy_match_chain)[deprecatedfunction

create\_extraction\_chain

Creates a chain that extracts information from a passage.](/python/langchain-classic/chains/openai_functions/extraction/create_extraction_chain)[deprecatedfunction

create\_extraction\_chain\_pydantic

Creates a chain that extracts information from a passage using Pydantic schema.](/python/langchain-classic/chains/openai_functions/extraction/create_extraction_chain_pydantic)[deprecatedfunction

create\_qa\_with\_sources\_chain

Create a question answering chain that returns an answer with sources.](/python/langchain-classic/chains/openai_functions/qa_with_structure/create_qa_with_sources_chain)[deprecatedfunction

create\_qa\_with\_structure\_chain

Create a question answering chain with structure.

Create a question answering chain that returns an answer with sources
based on schema.](/python/langchain-classic/chains/openai_functions/qa_with_structure/create_qa_with_structure_chain)[deprecatedfunction

create\_tagging\_chain

Create tagging chain from schema.

Create a chain that extracts information from a passage
based on a schema.

This function is deprecated. Please use `with_structured_output` instead.
See example usage below:

```
from typing_extensions import Annotated, TypedDict
from langchain_anthropic import ChatAnthropic

class Joke(TypedDict):
    """Tagged joke."""

    setup: Annotated[str, ..., "The setup of the joke"]
    punchline: Annotated[str, ..., "The punchline of the joke"]

# Or any other chat model that supports tools.
# Please reference to the documentation of structured_output
# to see an up to date list of which models support
# with_structured_output.
model = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)
structured_model = model.with_structured_output(Joke)
structured_model.invoke(
    "Why did the cat cross the road? To get to the other "
    "side... and then lay down in the middle of it!"
)
```

Read more here: <https://docs.langchain.com/oss/python/langchain/models#structured-outputs>](/python/langchain-classic/chains/openai_functions/tagging/create_tagging_chain)[deprecatedfunction

create\_tagging\_chain\_pydantic

Create tagging chain from Pydantic schema.

Create a chain that extracts information from a passage
based on a Pydantic schema.

This function is deprecated. Please use `with_structured_output` instead.
See example usage below:

```
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic

class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")

# Or any other chat model that supports tools.
# Please reference to the documentation of structured_output
# to see an up to date list of which models support
# with_structured_output.
model = ChatAnthropic(model="claude-opus-4-1-20250805", temperature=0)
structured_model = model.with_structured_output(Joke)
structured_model.invoke(
    "Why did the cat cross the road? To get to the other "
    "side... and then lay down in the middle of it!"
)
```

Read more here: <https://docs.langchain.com/oss/python/langchain/models#structured-outputs>](/python/langchain-classic/chains/openai_functions/tagging/create_tagging_chain_pydantic)[deprecatedfunction

create\_openai\_fn\_runnable

Create a runnable sequence that uses OpenAI functions.](/python/langchain-classic/chains/structured_output/base/create_openai_fn_runnable)[deprecatedfunction

create\_structured\_output\_runnable

Create a runnable for extracting structured outputs.](/python/langchain-classic/chains/structured_output/base/create_structured_output_runnable)

## Modules

[module

citation\_fuzzy\_match](/python/langchain-classic/chains/openai_functions/citation_fuzzy_match)[module

extraction](/python/langchain-classic/chains/openai_functions/extraction)[module

qa\_with\_structure](/python/langchain-classic/chains/openai_functions/qa_with_structure)[module

base

Methods for creating chains that use OpenAI function-calling APIs.](/python/langchain-classic/chains/openai_functions/base)[module

openapi](/python/langchain-classic/chains/openai_functions/openapi)[module

utils](/python/langchain-classic/chains/openai_functions/utils)[module

tagging](/python/langchain-classic/chains/openai_functions/tagging)


