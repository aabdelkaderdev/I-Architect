<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/history_aware_retriever -->

Modulev1.2.13 (latest)●Since v1.0

# history\_aware\_retriever

## Functions

[function

create\_history\_aware\_retriever

Create a chain that takes conversation history and returns documents.

If there is no `chat_history`, then the `input` is just passed directly to the
retriever. If there is `chat_history`, then the prompt and LLM will be used
to generate a search query. That search query is then passed to the retriever.](/python/langchain-classic/chains/history_aware_retriever/create_history_aware_retriever)


