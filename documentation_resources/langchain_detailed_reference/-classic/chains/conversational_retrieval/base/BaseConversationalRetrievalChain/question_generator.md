<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/question_generator -->

Attributev1.2.13 (latest)●Since v1.0

# question\_generator

The chain used to generate a new question for the sake of retrieval.
This chain will take in the current question (with variable `question`)
and any chat history (with variable `chat_history`) and will produce
a new standalone question to be used later on.


```
question_generator: LLMChain
```


