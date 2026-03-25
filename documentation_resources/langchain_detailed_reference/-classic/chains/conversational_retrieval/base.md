<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/conversational_retrieval/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Chain for chatting with a vector database.

## Attributes

[attribute

CONDENSE\_QUESTION\_PROMPT](/python/langchain-classic/chains/conversational_retrieval/prompts/CONDENSE_QUESTION_PROMPT)

## Functions

[deprecatedfunction

load\_qa\_chain

Load question answering chain.](/python/langchain-classic/chains/question_answering/chain/load_qa_chain)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

BaseCombineDocumentsChain

Base interface for chains combining documents.

Subclasses of this chain deal with combining documents in a variety of
ways. This base class exists to add some uniformity in the interface these types
of chains should expose. Namely, they expect an input key related to the documents
to use (default `input_documents`), and then also expose a method to calculate
the length of a prompt from documents (useful for outside callers to use to
determine whether it's safe to pass a list of documents into this chain or whether
that will be longer than the context length).](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain)[class

InputType

Input type for ConversationalRetrievalChain.](/python/langchain-classic/chains/conversational_retrieval/base/InputType)[class

BaseConversationalRetrievalChain

Chain for chatting with an index.](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain)[class

ChatVectorDBChain

Chain for chatting with a vector database.](/python/langchain-classic/chains/conversational_retrieval/base/ChatVectorDBChain)[deprecatedclass

StuffDocumentsChain

Chain that combines documents by stuffing into context.

This chain takes a list of documents and first combines them into a single string.
It does this by formatting each document into a string with the `document_prompt`
and then joining them together with `document_separator`. It then adds that new
string to the inputs with the variable name set by `document_variable_name`.
Those inputs are then passed to the `llm_chain`.](/python/langchain-classic/chains/combine_documents/stuff/StuffDocumentsChain)[deprecatedclass

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

ConversationalRetrievalChain

Chain for having a conversation based on retrieved documents.

This class is deprecated. See below for an example implementation using
`create_retrieval_chain`. Additional walkthroughs can be found at
<https://python.langchain.com/docs/use_cases/question_answering/chat_history>

```
from langchain_classic.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

retriever = ...  # Your retriever

model = ChatOpenAI()

# Contextualize question
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, just "
    "reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    model, retriever, contextualize_q_prompt
)

# Answer question
qa_system_prompt = (
    "You are an assistant for question-answering tasks. Use "
    "the following pieces of retrieved context to answer the "
    "question. If you don't know the answer, just say that you "
    "don't know. Use three sentences maximum and keep the answer "
    "concise."
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
# Below we use create_stuff_documents_chain to feed all retrieved context
# into the LLM. Note that we can also use StuffDocumentsChain and other
# instances of BaseCombineDocumentsChain.
question_answer_chain = create_stuff_documents_chain(model, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# Usage:
chat_history = []  # Collect chat history here (a sequence of messages)
rag_chain.invoke({"input": query, "chat_history": chat_history})
```

This chain takes in chat history (a list of messages) and new questions,
and then returns an answer to that question.
The algorithm for this chain consists of three parts:

1. Use the chat history and the new question to create a "standalone question".
   This is done so that this question can be passed into the retrieval step to
   fetch relevant documents. If only the new question was passed in, then relevant
   context may be lacking. If the whole conversation was passed into retrieval,
   there may be unnecessary information there that would distract from retrieval.
2. This new question is passed to the retriever and relevant documents are
   returned.
3. The retrieved documents are passed to an LLM along with either the new question
   (default behavior) or the original question and chat history to generate a final
   response.](/python/langchain-classic/chains/conversational_retrieval/base/ConversationalRetrievalChain)

## Type Aliases

[typeAlias

CHAT\_TURN\_TYPE: tuple[str, str] | BaseMessage](/python/langchain-classic/chains/conversational_retrieval/base/CHAT_TURN_TYPE)


