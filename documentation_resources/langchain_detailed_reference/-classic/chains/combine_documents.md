<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents -->

Modulev1.2.13 (latest)●Since v1.0

# combine\_documents

Different ways to combine documents.

## Functions

[function

acollapse\_docs

Execute a collapse function on a set of documents and merge their metadatas.](/python/langchain-classic/chains/combine_documents/reduce/acollapse_docs)[function

collapse\_docs

Execute a collapse function on a set of documents and merge their metadatas.](/python/langchain-classic/chains/combine_documents/reduce/collapse_docs)[function

split\_list\_of\_docs

Split `Document` objects to subsets that each meet a cumulative len. constraint.](/python/langchain-classic/chains/combine_documents/reduce/split_list_of_docs)[function

create\_stuff\_documents\_chain

Create a chain for passing a list of Documents to a model.](/python/langchain-classic/chains/combine_documents/stuff/create_stuff_documents_chain)

## Modules

[module

refine

Combine documents by doing a first pass and then refining on more documents.](/python/langchain-classic/chains/combine_documents/refine)[module

stuff

Chain that combines documents by stuffing into context.](/python/langchain-classic/chains/combine_documents/stuff)[module

base

Base interface for chains combining documents.](/python/langchain-classic/chains/combine_documents/base)[module

map\_rerank

Combining documents by mapping a chain over them first, then reranking results.](/python/langchain-classic/chains/combine_documents/map_rerank)[module

map\_reduce

Combining documents by mapping a chain over them first, then combining results.](/python/langchain-classic/chains/combine_documents/map_reduce)[module

reduce

Combine many documents together by recursively reducing them.](/python/langchain-classic/chains/combine_documents/reduce)


