<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/api/prompt/API_URL_PROMPT_TEMPLATE -->

Attributev1.2.13 (latest)●Since v1.0

# API\_URL\_PROMPT\_TEMPLATE


```
API_URL_PROMPT_TEMPLATE = 'You are given the below API Documentation:\n{api_docs}\nUsing this documentation, generate the full API url to call for answering the user question.\nYou should build the API url in order to get a response that is as short as possible, while still getting the necessary information to answer the question. Pay attention to deliberately exclude any unnecessary pieces of data in the API call.\n\nQuestion:{question}\nAPI url:'
```


