<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/qa_generation/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

## Attributes

[attribute

PROMPT\_SELECTOR](/python/langchain-classic/chains/qa_generation/prompt/PROMPT_SELECTOR)

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
```](/python/langchain-classic/chains/llm/LLMChain)[deprecatedclass

QAGenerationChain

Base class for question-answer generation chains.

This class is deprecated. See below for an alternative implementation.

Advantages of this implementation include:

- Supports async and streaming;
- Surfaces prompt and text splitter for easier customization;
- Use of JsonOutputParser supports JSONPatch operations in streaming mode,
  as well as robustness to markdown.

```
from langchain_classic.chains.qa_generation.prompt import (
    CHAT_PROMPT as prompt,
)

# Note: import PROMPT if using a legacy non-chat model.
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.runnables.base import RunnableEach
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

model = ChatOpenAI()
text_splitter = RecursiveCharacterTextSplitter(chunk_overlap=500)
split_text = RunnableLambda(lambda x: text_splitter.create_documents([x]))

chain = RunnableParallel(
    text=RunnablePassthrough(),
    questions=(
        split_text | RunnableEach(bound=prompt | model | JsonOutputParser())
    ),
)
```](/python/langchain-classic/chains/qa_generation/base/QAGenerationChain)


