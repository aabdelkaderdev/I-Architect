<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# MapRerankDocumentsChain


```
MapRerankDocumentsChain()
```

## Bases

`BaseCombineDocumentsChain`

## Attributes

## Methods

## Inherited from[BaseCombineDocumentsChain](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain)

### Attributes

[Ainput\_key: str](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain/input_key)[Aoutput\_key: str](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain/output_key)[Ainput\_keys: list[str]

—

Expect input key.](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain/input_keys)

### Methods



M

get\_input\_schema

[Mprompt\_length

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

Keys expected to be in the chain input.](/python/langchain-classic/chains/base/Chain/input_keys)

### Methods

[Mget\_input\_schema](/python/langchain-classic/chains/base/Chain/get_input_schema)[Minvoke](/python/langchain-classic/chains/base/Chain/invoke)[Mainvoke](/python/langchain-classic/chains/base/Chain/ainvoke)[Mraise\_callback\_manager\_deprecation

—

Raise deprecation warning if callback\_manager is used.](/python/langchain-classic/chains/base/Chain/raise_callback_manager_deprecation)[Mset\_verbose

—

Set the chain verbosity.](/python/langchain-classic/chains/base/Chain/set_verbose)

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

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)[Mget\_config\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_config_jsonschema)

[attribute

llm\_chain: LLMChain

Chain to apply to each document individually.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/llm_chain)

[attribute

document\_variable\_name: str

The variable name in the llm\_chain to put the documents in.
If only one variable in the llm\_chain, this need not be provided.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/document_variable_name)

[attribute

rank\_key: str

Key in output of llm\_chain to rank on.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/rank_key)

[attribute

answer\_key: str

Key in output of llm\_chain to return as answer.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/answer_key)

[attribute

metadata\_keys: list[str] | None

Additional metadata from the chosen document to return.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/metadata_keys)

[attribute

return\_intermediate\_steps: bool

Return intermediate steps.
Intermediate steps include the results of calling llm\_chain on each document.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/return_intermediate_steps)

[attribute

model\_config](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/model_config)

[attribute

output\_keys: list[str]

Expect input key.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/output_keys)

[method

get\_output\_schema](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/get_output_schema)

[method

validate\_llm\_output

Validate that the combine chain outputs a dictionary.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/validate_llm_output)

[method

get\_default\_document\_variable\_name

Get default document variable name, if not provided.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/get_default_document_variable_name)

[method

combine\_docs

Combine documents in a map rerank manner.

Combine by mapping first chain over all documents, then reranking the results.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/combine_docs)

[method

acombine\_docs

Combine documents in a map rerank manner.

Combine by mapping first chain over all documents, then reranking the results.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/acombine_docs)

Combining documents by mapping a chain over them, then reranking results.

This algorithm calls an LLMChain on each input document. The LLMChain is expected
to have an OutputParser that parses the result into both an answer (`answer_key`)
and a score (`rank_key`). The answer with the highest score is then returned.

**Example:**

```
from langchain_classic.chains import MapRerankDocumentsChain, LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_classic.output_parsers.regex import RegexParser

document_variable_name = "context"
model = OpenAI()
# The prompt here should take as an input variable the
# `document_variable_name`
# The actual prompt will need to be a lot more complex, this is just
# an example.
prompt_template = (
    "Use the following context to tell me the chemical formula "
    "for water. Output both your answer and a score of how confident "
    "you are. Context: {context}"
)
output_parser = RegexParser(
    regex=r"(.*?)\nScore: (.*)",
    output_keys=["answer", "score"],
)
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context"],
    output_parser=output_parser,
)
llm_chain = LLMChain(llm=model, prompt=prompt)
chain = MapRerankDocumentsChain(
    llm_chain=llm_chain,
    document_variable_name=document_variable_name,
    rank_key="score",
    answer_key="answer",
)
```

M

acall

—

Asynchronously execute the chain.

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