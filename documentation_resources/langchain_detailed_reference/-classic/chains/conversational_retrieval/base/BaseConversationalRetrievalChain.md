<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain -->

Classv1.2.13 (latest)●Since v1.0

# BaseConversationalRetrievalChain


```
BaseConversationalRetrievalChain()
```

## Bases

`Chain`

## Attributes

## Methods

## Inherited from[Chain](/python/langchain-classic/chains/base/Chain)

### Attributes

[Amemory: BaseMemory | None

—

Optional memory object.](/python/langchain-classic/chains/base/Chain/memory)[Acallbacks: Callbacks

—

Optional list of callback handlers (or callback manager).](/python/langchain-classic/chains/base/Chain/callbacks)[Averbose: bool

—

Whether or not run in verbose mode. In verbose mode, some intermediate logs](/python/langchain-classic/chains/base/Chain/verbose)



A

tags

: list[str] | None

—

Optional list of tags associated with the chain.

[Ametadata: builtins.dict[str, Any] | None

—

Optional metadata associated with the chain.](/python/langchain-classic/chains/base/Chain/metadata)

[Acallback\_manager: BaseCallbackManager | None

—

[DEPRECATED] Use `callbacks` instead.](/python/langchain-classic/chains/base/Chain/callback_manager)

### Methods

[Mget\_output\_schema](/python/langchain-classic/chains/base/Chain/get_output_schema)[Minvoke](/python/langchain-classic/chains/base/Chain/invoke)[Mainvoke](/python/langchain-classic/chains/base/Chain/ainvoke)[Mraise\_callback\_manager\_deprecation

—

Raise deprecation warning if callback\_manager is used.](/python/langchain-classic/chains/base/Chain/raise_callback_manager_deprecation)[Mset\_verbose

—

Set the chain verbosity.](/python/langchain-classic/chains/base/Chain/set_verbose)[Macall

—

Asynchronously execute the chain.](/python/langchain-classic/chains/base/Chain/acall)[Mprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/prep_outputs)[Maprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/aprep_outputs)[Mprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/prep_inputs)[Maprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/aprep_inputs)[Mrun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/run)[Marun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/arun)[Mdict

—

Dictionary representation of chain.](/python/langchain-classic/chains/base/Chain/dict)[Mapply

—

Call the chain on all inputs in the list.](/python/langchain-classic/chains/base/Chain/apply)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

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

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)[Mget\_config\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_config_jsonschema)

[attribute

combine\_docs\_chain: BaseCombineDocumentsChain

The chain used to combine any retrieved documents.](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/combine_docs_chain)

[attribute

question\_generator: LLMChain

The chain used to generate a new question for the sake of retrieval.
This chain will take in the current question (with variable `question`)
and any chat history (with variable `chat_history`) and will produce
a new standalone question to be used later on.](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/question_generator)

[attribute

output\_key: str

The output key to return the final answer of this chain in.](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/output_key)

[attribute

rephrase\_question: bool

Whether or not to pass the new generated question to the combine\_docs\_chain.
If `True`, will pass the new generated question along.
If `False`, will only use the new generated question for retrieval and pass the
original question along to the combine\_docs\_chain.](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/rephrase_question)

[attribute

return\_source\_documents: bool

Return the retrieved source documents as part of the final result.](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/return_source_documents)

[attribute

return\_generated\_question: bool

Return the generated question as part of the final result.](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/return_generated_question)

[attribute

get\_chat\_history: Callable[[list[CHAT\_TURN\_TYPE]], str] | None

An optional function to get a string of the chat history.
If `None` is provided, will use a default.](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/get_chat_history)

[attribute

response\_if\_no\_docs\_found: str | None

If specified, the chain will return a fixed response if no docs
are found for the question.](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/response_if_no_docs_found)

[attribute

model\_config](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/model_config)

[attribute

input\_keys: list[str]

Input keys.](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/input_keys)

[attribute

output\_keys: list[str]

Return the output keys.](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/output_keys)

[method

get\_input\_schema](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/get_input_schema)

[method

save](/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/save)

Chain for chatting with an index.

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