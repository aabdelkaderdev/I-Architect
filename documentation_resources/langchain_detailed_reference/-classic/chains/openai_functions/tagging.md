<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/tagging -->

Modulev1.2.13 (latest)●Since v1.0

# tagging

## Functions

[function

get\_llm\_kwargs

Return the kwargs for the LLMChain constructor.](/python/langchain-classic/chains/openai_functions/utils/get_llm_kwargs)[deprecatedfunction

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

Read more here: <https://docs.langchain.com/oss/python/langchain/models#structured-outputs>](/python/langchain-classic/chains/openai_functions/tagging/create_tagging_chain_pydantic)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[deprecatedclass

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


