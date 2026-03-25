<!-- Source: https://reference.langchain.com/python/langchain-classic/indexes/vectorstore -->

Modulev1.2.13 (latest)●Since v1.0

# vectorstore

Vectorstore stubs for the indexing api.

## Classes

[class

RetrievalQAWithSourcesChain

Question-answering with sources over an index.](/python/langchain-classic/chains/qa_with_sources/retrieval/RetrievalQAWithSourcesChain)[class

VectorStoreIndexWrapper

Wrapper around a `VectorStore` for easy access.](/python/langchain-classic/indexes/vectorstore/VectorStoreIndexWrapper)[class

VectorstoreIndexCreator

Logic for creating indexes.](/python/langchain-classic/indexes/vectorstore/VectorstoreIndexCreator)[deprecatedclass

RetrievalQA

Chain for question-answering against an index.

This class is deprecated. See below for an example implementation using
`create_retrieval_chain`:

```
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

retriever = ...  # Your retriever
model = ChatOpenAI()

system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Use three sentence maximum and keep the answer concise. "
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(model, prompt)
chain = create_retrieval_chain(retriever, question_answer_chain)

chain.invoke({"input": query})
```](/python/langchain-classic/chains/retrieval_qa/base/RetrievalQA)


