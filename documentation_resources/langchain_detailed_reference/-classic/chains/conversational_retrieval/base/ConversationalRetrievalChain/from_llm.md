<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/conversational_retrieval/base/ConversationalRetrievalChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Convenience method to load chain from LLM and retriever.

This provides some logic to create the `question_generator` chain
as well as the combine\_docs\_chain.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  retriever: BaseRetriever,
  condense_question_prompt: BasePromptTemplate = CONDENSE_QUESTION_PROMPT,
  chain_type: str = 'stuff',
  verbose: bool = False,
  condense_question_llm: BaseLanguageModel | None = None,
  combine_docs_chain_kwargs: dict | None = None,
  callbacks: Callbacks = None,
  **kwargs: Any = {}
) -> BaseConversationalRetrievalChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The default language model to use at every part of this chain (eg in both the question generation and the answering) |
| `retriever`\* | `BaseRetriever` | The retriever to use to fetch relevant documents from. |
| `condense_question_prompt` | `BasePromptTemplate` | Default:`CONDENSE_QUESTION_PROMPT`  The prompt to use to condense the chat history and new question into a standalone question. |
| `chain_type` | `str` | Default:`'stuff'`  The chain type to use to create the combine\_docs\_chain, will be sent to `load_qa_chain`. |
| `verbose` | `bool` | Default:`False`  Verbosity flag for logging to stdout. |
| `condense_question_llm` | `BaseLanguageModel | None` | Default:`None`  The language model to use for condensing the chat history and new question into a standalone question. If none is provided, will default to `llm`. |
| `combine_docs_chain_kwargs` | `dict | None` | Default:`None`  Parameters to pass as kwargs to `load_qa_chain` when constructing the combine\_docs\_chain. |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to pass to all subchains. |
| `kwargs` | `Any` | Default:`{}`  Additional parameters to pass when initializing ConversationalRetrievalChain |


