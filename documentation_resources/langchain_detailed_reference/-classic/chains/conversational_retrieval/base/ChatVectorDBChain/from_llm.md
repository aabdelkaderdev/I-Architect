<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/conversational_retrieval/base/ChatVectorDBChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Load chain from LLM.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  vectorstore: VectorStore,
  condense_question_prompt: BasePromptTemplate = CONDENSE_QUESTION_PROMPT,
  chain_type: str = 'stuff',
  combine_docs_chain_kwargs: dict | None = None,
  callbacks: Callbacks = None,
  **kwargs: Any = {}
) -> BaseConversationalRetrievalChain
```


