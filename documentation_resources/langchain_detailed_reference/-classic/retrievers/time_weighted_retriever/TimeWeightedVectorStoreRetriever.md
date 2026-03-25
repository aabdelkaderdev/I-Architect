<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever -->

Classv1.2.13 (latest)●Since v1.0

# TimeWeightedVectorStoreRetriever


```
TimeWeightedVectorStoreRetriever()
```

## Bases

`BaseRetriever`

## Attributes

## Methods

## Inherited from[BaseRetriever](/python/langchain-core/retrievers/BaseRetriever)(langchain\_core)

### Attributes

[Atags](/python/langchain-core/retrievers/BaseRetriever/tags)[Ametadata](/python/langchain-core/retrievers/BaseRetriever/metadata)

### Methods

[Minvoke](/python/langchain-core/retrievers/BaseRetriever/invoke)[Mainvoke](/python/langchain-core/retrievers/BaseRetriever/ainvoke)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)



(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

[attribute

vectorstore: VectorStore

The `VectorStore` to store documents and determine salience.](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/vectorstore)

[attribute

search\_kwargs: dict

Keyword arguments to pass to the `VectorStore` similarity search.](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/search_kwargs)

[attribute

memory\_stream: list[Document]

The memory\_stream of documents to search through.](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/memory_stream)

[attribute

decay\_rate: float

The exponential decay factor used as `(1.0-decay_rate)**(hrs_passed)`.](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/decay_rate)

[attribute

k: int

The maximum number of documents to retrieve in a given call.](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/k)

[attribute

other\_score\_keys: list[str]

Other keys in the metadata to factor into the score, e.g. 'importance'.](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/other_score_keys)

[attribute

default\_salience: float | None

The salience to assign memories not retrieved from the vector store.

None assigns no salience to documents not fetched from the vector store.](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/default_salience)

[attribute

model\_config](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/model_config)

[method

get\_salient\_docs

Return documents that are salient to the query.](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/get_salient_docs)

[method

aget\_salient\_docs

Return documents that are salient to the query.](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/aget_salient_docs)

[method

add\_documents

Add documents to vectorstore.](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/add_documents)

[method

aadd\_documents

Add documents to vectorstore.](/python/langchain-classic/retrievers/time_weighted_retriever/TimeWeightedVectorStoreRetriever/aadd_documents)

Time Weighted Vector Store Retriever.

Retriever that combines embedding similarity with recency in retrieving values.

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