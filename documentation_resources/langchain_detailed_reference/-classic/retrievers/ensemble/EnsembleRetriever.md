<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/ensemble/EnsembleRetriever -->

Classv1.2.13 (latest)●Since v1.0

# EnsembleRetriever


```
EnsembleRetriever()
```

## Bases

`BaseRetriever`

## Attributes

## Methods

## Inherited from[BaseRetriever](/python/langchain-core/retrievers/BaseRetriever)(langchain\_core)

### Attributes

[Amodel\_config](/python/langchain-core/retrievers/BaseRetriever/model_config)[Atags](/python/langchain-core/retrievers/BaseRetriever/tags)[Ametadata](/python/langchain-core/retrievers/BaseRetriever/metadata)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes



A

name

[Amodel\_config](/python/langchain-core/runnables/base/RunnableSerializable/model_config)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `retrievers`\* | `unknown` | A list of retrievers to ensemble. |
| `weights`\* | `unknown` | A list of weights corresponding to the retrievers. Defaults to equal weighting for all retrievers. |
| `c`\* | `unknown` | A constant added to the rank, controlling the balance between the importance of high-ranked items and the consideration given to lower-ranked items. |
| `id_key`\* | `unknown` | The key in the document's metadata used to determine unique documents. If not specified, page\_content is used. |

[attribute

retrievers: list[RetrieverLike]](/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/retrievers)

[attribute

weights: list[float]](/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/weights)

[attribute

c: int](/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/c)

[attribute

id\_key: str | None](/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/id_key)

[attribute

config\_specs: list[ConfigurableFieldSpec]

List configurable fields for this runnable.](/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/config_specs)

[method

invoke](/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/invoke)

[method

ainvoke](/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/ainvoke)

[method

rank\_fusion

Rank fusion.

Retrieve the results of the retrievers and use rank\_fusion\_func to get
the final result.](/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/rank_fusion)

[method

arank\_fusion

Rank fusion.

Asynchronously retrieve the results of the retrievers
and use rank\_fusion\_func to get the final result.](/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/arank_fusion)

[method

weighted\_reciprocal\_rank

Perform weighted Reciprocal Rank Fusion on multiple rank lists.

You can find more details about RRF here:
<https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf>.](/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/weighted_reciprocal_rank)

Retriever that ensembles the multiple retrievers.

It uses a rank fusion.

M

get\_config\_jsonschema

[Mget\_graph](/python/langchain-core/runnables/base/Runnable/get_graph)

[Mget\_prompts](/python/langchain-core/runnables/base/Runnable/get_prompts)

[Mpipe](/python/langchain-core/runnables/base/Runnable/pipe)

[Mpick](/python/langchain-core/runnables/base/Runnable/pick)

[Massign](/python/langchain-core/runnables/base/Runnable/assign)

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