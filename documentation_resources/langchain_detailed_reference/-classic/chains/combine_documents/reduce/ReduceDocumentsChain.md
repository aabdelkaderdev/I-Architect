<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# ReduceDocumentsChain


```
ReduceDocumentsChain()
```

## Bases

`BaseCombineDocumentsChain`

## Attributes

## Methods

## Inherited from[BaseCombineDocumentsChain](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain)

### Attributes

[Ainput\_key: str](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain/input_key)[Aoutput\_key: str](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain/output_key)[Ainput\_keys: list[str]

—

Expect input key.](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain/input_keys)[A](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain/output_keys)



output\_keys

: list[str]

—

Return output key.

### Methods

[Mget\_input\_schema](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain/get_input_schema)[Mget\_output\_schema](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain/get_output_schema)[Mprompt\_length

—

Return the prompt length given the documents passed in.](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain/prompt_length)

## Inherited from[Chain](/python/langchain-classic/chains/base/Chain)

### Attributes

[Amemory: BaseMemory | None

—

Optional memory object.](/python/langchain-classic/chains/base/Chain/memory)[Acallbacks: Callbacks

—

Optional list of callback handlers (or callback manager).](/python/langchain-classic/chains/base/Chain/callbacks)[Averbose: bool

—

Whether or not run in verbose mode. In verbose mode, some intermediate logs](/python/langchain-classic/chains/base/Chain/verbose)[Atags: list[str] | None

—

Optional list of tags associated with the chain.](/python/langchain-classic/chains/base/Chain/tags)[Ametadata: builtins.dict[str, Any] | None

—

Optional metadata associated with the chain.](/python/langchain-classic/chains/base/Chain/metadata)[Acallback\_manager: BaseCallbackManager | None

—

[DEPRECATED] Use `callbacks` instead.](/python/langchain-classic/chains/base/Chain/callback_manager)[Ainput\_keys: list[str]

—

Keys expected to be in the chain input.](/python/langchain-classic/chains/base/Chain/input_keys)[Aoutput\_keys: list[str]

—

Keys expected to be in the chain output.](/python/langchain-classic/chains/base/Chain/output_keys)

### Methods

[Mget\_input\_schema](/python/langchain-classic/chains/base/Chain/get_input_schema)[Mget\_output\_schema](/python/langchain-classic/chains/base/Chain/get_output_schema)[Minvoke](/python/langchain-classic/chains/base/Chain/invoke)[Mainvoke](/python/langchain-classic/chains/base/Chain/ainvoke)[Mraise\_callback\_manager\_deprecation

—

Raise deprecation warning if callback\_manager is used.](/python/langchain-classic/chains/base/Chain/raise_callback_manager_deprecation)[M](/python/langchain-classic/chains/base/Chain/set_verbose)

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

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

[attribute

combine\_documents\_chain: BaseCombineDocumentsChain

Final chain to call to combine documents.

This is typically a `StuffDocumentsChain`.](/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain/combine_documents_chain)

[attribute

collapse\_documents\_chain: BaseCombineDocumentsChain | None

Chain to use to collapse documents if needed until they can all fit.
If `None`, will use the `combine_documents_chain`.

This is typically a `StuffDocumentsChain`.](/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain/collapse_documents_chain)

[attribute

token\_max: int

The maximum number of tokens to group documents into.

For example, if set to 3000 then documents will be grouped into chunks of no greater
than 3000 tokens before trying to combine them into a smaller chunk.](/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain/token_max)

[attribute

collapse\_max\_retries: int | None

The maximum number of retries to collapse documents to fit `token_max`.

If `None`, it will keep trying to collapse documents to fit `token_max`.

Otherwise, after it reaches the max number, it will throw an error.](/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain/collapse_max_retries)

[attribute

model\_config](/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain/model_config)

[method

combine\_docs

Combine multiple documents recursively.](/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain/combine_docs)

[method

acombine\_docs

Async combine multiple documents recursively.](/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain/acombine_docs)

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
as are allowed.

**Example:**

```
from langchain_classic.chains import (
    StuffDocumentsChain,
    LLMChain,
    ReduceDocumentsChain,
)
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# This controls how each document will be formatted. Specifically,
# it will be passed to `format_document` - see that function for more
# details.
document_prompt = PromptTemplate(
    input_variables=["page_content"], template="{page_content}"
)
document_variable_name = "context"
model = OpenAI()
# The prompt here should take as an input variable the
# `document_variable_name`
prompt = PromptTemplate.from_template("Summarize this content: {context}")
llm_chain = LLMChain(llm=model, prompt=prompt)
combine_documents_chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_prompt=document_prompt,
    document_variable_name=document_variable_name,
)
chain = ReduceDocumentsChain(
    combine_documents_chain=combine_documents_chain,
)
# If we wanted to, we could also pass in collapse_documents_chain
# which is specifically aimed at collapsing documents BEFORE
# the final call.
prompt = PromptTemplate.from_template("Collapse this content: {context}")
llm_chain = LLMChain(llm=model, prompt=prompt)
collapse_documents_chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_prompt=document_prompt,
    document_variable_name=document_variable_name,
)
chain = ReduceDocumentsChain(
    combine_documents_chain=combine_documents_chain,
    collapse_documents_chain=collapse_documents_chain,
)
```

set\_verbose

—

Set the chain verbosity.

[Macall

—

Asynchronously execute the chain.](/python/langchain-classic/chains/base/Chain/acall)

[Mprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/prep_outputs)

[Maprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/aprep_outputs)

[Mprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/prep_inputs)

[Maprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/aprep_inputs)

[Mrun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/run)

[Marun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/arun)

[Mdict

—

Dictionary representation of chain.](/python/langchain-classic/chains/base/Chain/dict)

[Msave

—

Save the chain.](/python/langchain-classic/chains/base/Chain/save)

[Mapply

—

Call the chain on all inputs in the list.](/python/langchain-classic/chains/base/Chain/apply)

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