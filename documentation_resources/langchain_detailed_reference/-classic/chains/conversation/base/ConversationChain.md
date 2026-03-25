<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/conversation/base/ConversationChain -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# ConversationChain


```
ConversationChain
```

(

)

## Bases

`LLMChain`

## Attributes

[attribute

memory: BaseMemory](/python/langchain-classic/chains/conversation/base/ConversationChain/memory)[attribute

prompt: BasePromptTemplate](/python/langchain-classic/chains/conversation/base/ConversationChain/prompt)[attribute

input\_key: str](/python/langchain-classic/chains/conversation/base/ConversationChain/input_key)[attribute

output\_key: str](/python/langchain-classic/chains/conversation/base/ConversationChain/output_key)[attribute

model\_config](/python/langchain-classic/chains/conversation/base/ConversationChain/model_config)[attribute

input\_keys: list[str]](/python/langchain-classic/chains/conversation/base/ConversationChain/input_keys)

## Methods

[method

is\_lc\_serializable](/python/langchain-classic/chains/conversation/base/ConversationChain/is_lc_serializable)[method

validate\_prompt\_input\_variables](/python/langchain-classic/chains/conversation/base/ConversationChain/validate_prompt_input_variables)

## Inherited from[LLMChain](/python/langchain-classic/chains/llm/LLMChain)

### Attributes

[Allm: Runnable[LanguageModelInput, str] | Runnable[LanguageModelInput, BaseMessage]

—

Language model to call.](/python/langchain-classic/chains/llm/LLMChain/llm)[Aoutput\_parser: BaseLLMOutputParser

—

Output parser to use.](/python/langchain-classic/chains/llm/LLMChain/output_parser)[Areturn\_final\_only: bool

—

Whether to return only the final parsed result.](/python/langchain-classic/chains/llm/LLMChain/return_final_only)[Allm\_kwargs: dict](/python/langchain-classic/chains/llm/LLMChain/llm_kwargs)[Aoutput\_keys: list[str]

—

Will always return text key.](/python/langchain-classic/chains/llm/LLMChain/output_keys)

### Methods

[Mgenerate

—

Generate LLM result from inputs.](/python/langchain-classic/chains/llm/LLMChain/generate)[Magenerate

—

Generate LLM result from inputs.](/python/langchain-classic/chains/llm/LLMChain/agenerate)[Mprep\_prompts

—

Prepare prompts from inputs.](/python/langchain-classic/chains/llm/LLMChain/prep_prompts)[Maprep\_prompts

—

Prepare prompts from inputs.](/python/langchain-classic/chains/llm/LLMChain/aprep_prompts)[M](/python/langchain-classic/chains/llm/LLMChain/apply)

## Inherited from[Chain](/python/langchain-classic/chains/base/Chain)

### Attributes

[Acallbacks: Callbacks

—

Optional list of callback handlers (or callback manager).](/python/langchain-classic/chains/base/Chain/callbacks)[Averbose: bool

—

Whether or not run in verbose mode. In verbose mode, some intermediate logs](/python/langchain-classic/chains/base/Chain/verbose)[Atags: list[str] | None

—

Optional list of tags associated with the chain.](/python/langchain-classic/chains/base/Chain/tags)[A](/python/langchain-classic/chains/base/Chain/metadata)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)

### Methods

[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[M](/python/langchain-core/load/serializable/Serializable/to_json)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)



Chain to have a conversation and load context from memory.

This class is deprecated in favor of `RunnableWithMessageHistory`. Please refer
to this tutorial for more detail: <https://python.langchain.com/docs/tutorials/chatbot/>

`RunnableWithMessageHistory` offers several benefits, including:

- Stream, batch, and async support;
- More flexible memory handling, including the ability to manage memory
  outside the chain;
- Support for multiple threads.

Below is a minimal implementation, analogous to using `ConversationChain` with
the default `ConversationBufferMemory`:

```
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

store = {}  # memory is maintained outside the chain

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

model = ChatOpenAI(model="gpt-3.5-turbo-0125")

chain = RunnableWithMessageHistory(model, get_session_history)
chain.invoke(
    "Hi I'm Bob.",
    config={"configurable": {"session_id": "1"}},
)  # session_id determines thread
```

Memory objects can also be incorporated into the `get_session_history` callable:

```
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

store = {}  # memory is maintained outside the chain

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    memory = ConversationBufferWindowMemory(
        chat_memory=store[session_id],
        k=3,
        return_messages=True,
    )
    assert len(memory.memory_variables) == 1
    key = memory.memory_variables[0]
    messages = memory.load_memory_variables({})[key]
    store[session_id] = InMemoryChatMessageHistory(messages=messages)
    return store[session_id]

model = ChatOpenAI(model="gpt-3.5-turbo-0125")

chain = RunnableWithMessageHistory(model, get_session_history)
chain.invoke(
    "Hi I'm Bob.",
    config={"configurable": {"session_id": "1"}},
)  # session_id determines thread
```

**Example:**

```
from langchain_classic.chains import ConversationChain
from langchain_openai import OpenAI

conversation = ConversationChain(llm=OpenAI())
```

apply

—

Utilize the LLM generate method for speed gains.

[Maapply

—

Utilize the LLM generate method for speed gains.](/python/langchain-classic/chains/llm/LLMChain/aapply)

[Mcreate\_outputs

—

Create outputs from response.](/python/langchain-classic/chains/llm/LLMChain/create_outputs)

[Mpredict

—

Format prompt with kwargs and pass to LLM.](/python/langchain-classic/chains/llm/LLMChain/predict)

[Mapredict

—

Format prompt with kwargs and pass to LLM.](/python/langchain-classic/chains/llm/LLMChain/apredict)

[Mpredict\_and\_parse

—

Call predict and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/predict_and_parse)

[Mapredict\_and\_parse

—

Call apredict and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/apredict_and_parse)

[Mapply\_and\_parse

—

Call apply and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/apply_and_parse)

[Maapply\_and\_parse

—

Call apply and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/aapply_and_parse)

[Mfrom\_string

—

Create LLMChain from LLM and template.](/python/langchain-classic/chains/llm/LLMChain/from_string)

metadata

: builtins.dict[str, Any] | None

—

Optional metadata associated with the chain.

[Acallback\_manager: BaseCallbackManager | None

—

[DEPRECATED] Use `callbacks` instead.](/python/langchain-classic/chains/base/Chain/callback_manager)

[Aoutput\_keys: list[str]

—

Keys expected to be in the chain output.](/python/langchain-classic/chains/base/Chain/output_keys)

### Methods

[Mget\_input\_schema](/python/langchain-classic/chains/base/Chain/get_input_schema)[Mget\_output\_schema](/python/langchain-classic/chains/base/Chain/get_output_schema)[Minvoke](/python/langchain-classic/chains/base/Chain/invoke)[Mainvoke](/python/langchain-classic/chains/base/Chain/ainvoke)[Mraise\_callback\_manager\_deprecation

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

Dictionary representation of chain.](/python/langchain-classic/chains/base/Chain/dict)[Msave

—

Save the chain.](/python/langchain-classic/chains/base/Chain/save)[Mapply

—

Call the chain on all inputs in the list.](/python/langchain-classic/chains/base/Chain/apply)

to\_json

[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)[Mget\_config\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_config_jsonschema)[Mget\_graph](/python/langchain-core/runnables/base/Runnable/get_graph)[Mget\_prompts](/python/langchain-core/runnables/base/Runnable/get_prompts)[Mpipe](/python/langchain-core/runnables/base/Runnable/pipe)[Mpick](/python/langchain-core/runnables/base/Runnable/pick)[Massign](/python/langchain-core/runnables/base/Runnable/assign)[Minvoke](/python/langchain-core/runnables/base/Runnable/invoke)[Mainvoke](/python/langchain-core/runnables/base/Runnable/ainvoke)[Mbatch](/python/langchain-core/runnables/base/Runnable/batch)[Mbatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/batch_as_completed)[Mabatch](/python/langchain-core/runnables/base/Runnable/abatch)[Mabatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/abatch_as_completed)[Mstream](/python/langchain-core/runnables/base/Runnable/stream)[Mastream](/python/langchain-core/runnables/base/Runnable/astream)[Mastream\_log](/python/langchain-core/runnables/base/Runnable/astream_log)[Mastream\_events](/python/langchain-core/runnables/base/Runnable/astream_events)[Mtransform](/python/langchain-core/runnables/base/Runnable/transform)[Matransform](/python/langchain-core/runnables/base/Runnable/atransform)[Mbind](/python/langchain-core/runnables/base/Runnable/bind)[Mwith\_config](/python/langchain-core/runnables/base/Runnable/with_config)[Mwith\_listeners](/python/langchain-core/runnables/base/Runnable/with_listeners)[Mwith\_alisteners](/python/langchain-core/runnables/base/Runnable/with_alisteners)[Mwith\_types](/python/langchain-core/runnables/base/Runnable/with_types)[Mwith\_retry](/python/langchain-core/runnables/base/Runnable/with_retry)[Mmap](/python/langchain-core/runnables/base/Runnable/map)[Mwith\_fallbacks](/python/langchain-core/runnables/base/Runnable/with_fallbacks)[Mas\_tool](/python/langchain-core/runnables/base/Runnable/as_tool)

Default memory store.

Default conversation prompt to use.

Use this since so some prompt vars come from history.

Validate that prompt input variables are consistent.