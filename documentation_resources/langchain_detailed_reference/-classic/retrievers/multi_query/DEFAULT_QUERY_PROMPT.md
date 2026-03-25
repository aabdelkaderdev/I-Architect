<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/multi_query/DEFAULT_QUERY_PROMPT -->

Attributev1.2.13 (latest)●Since v1.0

# DEFAULT\_QUERY\_PROMPT


```
DEFAULT_QUERY_PROMPT = PromptTemplate(
  input_variables=['question'],
  template='You are an AI language model assistant. Your task is\n    to generate 3 different versions of the given user\n    question to retrieve relevant documents from a vector  database.\n    By generating multiple perspectives on the user question,
  \n    your goal is to help the user overcome some of the limitations\n    of distance-based similarity search. Provide these alternative\n    questions separated by newlines. Original question: {question}'
)
```


