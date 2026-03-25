<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever -->

Classv1.2.13 (latest)●Since v1.0

# ParentDocumentRetriever


```
ParentDocumentRetriever()
```

## Bases

`MultiVectorRetriever`

## Attributes

## Methods

## Inherited from[MultiVectorRetriever](/python/langchain-classic/retrievers/multi_vector/MultiVectorRetriever)

### Attributes

[Avectorstore: VectorStore

—

The underlying `VectorStore` to use to store small chunks](/python/langchain-classic/retrievers/multi_vector/MultiVectorRetriever/vectorstore)[Abyte\_store: ByteStore | None

—

The lower-level backing storage layer for the parent documents](/python/langchain-classic/retrievers/multi_vector/MultiVectorRetriever/byte_store)[Adocstore: BaseStore[str, Document]

—

The storage interface for the parent documents](/python/langchain-classic/retrievers/multi_vector/MultiVectorRetriever/docstore)



[Aid\_key: str](/python/langchain-classic/retrievers/multi_vector/MultiVectorRetriever/id_key)

[Asearch\_kwargs: dict

—

Keyword arguments to pass to the search function.](/python/langchain-classic/retrievers/multi_vector/MultiVectorRetriever/search_kwargs)

[Asearch\_type: SearchType

—

Type of search to perform (similarity / mmr)](/python/langchain-classic/retrievers/multi_vector/MultiVectorRetriever/search_type)

## Inherited from[BaseRetriever](/python/langchain-core/retrievers/BaseRetriever)(langchain\_core)

### Attributes

[Amodel\_config](/python/langchain-core/retrievers/BaseRetriever/model_config)[Atags](/python/langchain-core/retrievers/BaseRetriever/tags)[Ametadata](/python/langchain-core/retrievers/BaseRetriever/metadata)

### Methods

[Minvoke](/python/langchain-core/retrievers/BaseRetriever/invoke)[Mainvoke](/python/langchain-core/retrievers/BaseRetriever/ainvoke)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)[Amodel\_config](/python/langchain-core/runnables/base/RunnableSerializable/model_config)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

[attribute

child\_splitter: TextSplitter

The text splitter to use to create child documents.](/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever/child_splitter)

[attribute

parent\_splitter: TextSplitter | None

The text splitter to use to create parent documents.
If none, then the parent documents will be the raw documents passed in.](/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever/parent_splitter)

[attribute

child\_metadata\_fields: Sequence[str] | None

Metadata fields to leave in child documents. If `None`, leave all parent document
metadata.](/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever/child_metadata_fields)

[method

add\_documents

Adds documents to the docstore and vectorstores.](/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever/add_documents)

[method

aadd\_documents

Adds documents to the docstore and vectorstores.](/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever/aadd_documents)

Retrieve small chunks then retrieve their parent documents.

When splitting documents for retrieval, there are often conflicting desires:

1. You may want to have small documents, so that their embeddings can most
   accurately reflect their meaning. If too long, then the embeddings can
   lose meaning.
2. You want to have long enough documents that the context of each chunk is
   retained.

The ParentDocumentRetriever strikes that balance by splitting and storing
small chunks of data. During retrieval, it first fetches the small chunks
but then looks up the parent IDs for those chunks and returns those larger
documents.

Note that "parent document" refers to the document that a small chunk
originated from. This can either be the whole raw document OR a larger
chunk.

M

get\_config\_jsonschema

[Mget\_graph](/python/langchain-core/runnables/base/Runnable/get_graph)

[Mget\_prompts](/python/langchain-core/runnables/base/Runnable/get_prompts)

[Mpipe](/python/langchain-core/runnables/base/Runnable/pipe)

[Mpick](/python/langchain-core/runnables/base/Runnable/pick)

[Massign](/python/langchain-core/runnables/base/Runnable/assign)

[Minvoke](/python/langchain-core/runnables/base/Runnable/invoke)

[Mainvoke](/python/langchain-core/runnables/base/Runnable/ainvoke)

[Mbatch](/python/langchain-core/runnables/base/Runnable/batch)

[Mbatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/batch_as_completed)

[Mabatch](/python/langchain-core/runnables/base/Runnable/abatch)

[Mabatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/abatch_as_completed)

[Mstream](/python/langchain-core/runnables/base/Runnable/stream)

[Mastream](/python/langchain-core/runnables/base/Runnable/astream)

[Mastream\_log](/python/langchain-core/runnables/base/Runnable/astream_log)

[Mastream\_events](/python/langchain-core/runnables/base/Runnable/astream_events)

[Mtransform](/python/langchain-core/runnables/base/Runnable/transform)

[Matransform](/python/langchain-core/runnables/base/Runnable/atransform)

[Mbind](/python/langchain-core/runnables/base/Runnable/bind)

[Mwith\_config](/python/langchain-core/runnables/base/Runnable/with_config)

[Mwith\_listeners](/python/langchain-core/runnables/base/Runnable/with_listeners)

[Mwith\_alisteners](/python/langchain-core/runnables/base/Runnable/with_alisteners)

[Mwith\_types](/python/langchain-core/runnables/base/Runnable/with_types)

[Mwith\_retry](/python/langchain-core/runnables/base/Runnable/with_retry)

[Mmap](/python/langchain-core/runnables/base/Runnable/map)

[Mwith\_fallbacks](/python/langchain-core/runnables/base/Runnable/with_fallbacks)

[Mas\_tool](/python/langchain-core/runnables/base/Runnable/as_tool)