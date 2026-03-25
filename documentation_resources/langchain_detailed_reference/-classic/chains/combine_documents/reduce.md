<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/reduce -->

Modulev1.2.13 (latest)●Since v1.0

# reduce

Combine many documents together by recursively reducing them.

## Functions

[function

split\_list\_of\_docs

Split `Document` objects to subsets that each meet a cumulative len. constraint.](/python/langchain-classic/chains/combine_documents/reduce/split_list_of_docs)[function

collapse\_docs

Execute a collapse function on a set of documents and merge their metadatas.](/python/langchain-classic/chains/combine_documents/reduce/collapse_docs)[function

acollapse\_docs

Execute a collapse function on a set of documents and merge their metadatas.](/python/langchain-classic/chains/combine_documents/reduce/acollapse_docs)

## Classes

[class

BaseCombineDocumentsChain

Base interface for chains combining documents.

Subclasses of this chain deal with combining documents in a variety of
ways. This base class exists to add some uniformity in the interface these types
of chains should expose. Namely, they expect an input key related to the documents
to use (default `input_documents`), and then also expose a method to calculate
the length of a prompt from documents (useful for outside callers to use to
determine whether it's safe to pass a list of documents into this chain or whether
that will be longer than the context length).](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain)[class

CombineDocsProtocol

Interface for the combine\_docs method.](/python/langchain-classic/chains/combine_documents/reduce/CombineDocsProtocol)[class

AsyncCombineDocsProtocol

Interface for the combine\_docs method.](/python/langchain-classic/chains/combine_documents/reduce/AsyncCombineDocsProtocol)[deprecatedclass

ReduceDocumentsChain

Combine documents by recursively reducing them.

This involves

- `combine_documents_chain`
- `collapse_documents_chain`

`combine_documents_chain` is ALWAYS provided. This is final chain that is called.

We pass all previous results to this chain, and the output of this chain is
returned as a final result.

`collapse_documents_chain` is used if the documents passed in are too many to all
be passed to `combine_documents_chain` in one go. In this case,
`collapse_documents_chain` is called recursively on as big of groups of documents
as are allowed.](/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain)


