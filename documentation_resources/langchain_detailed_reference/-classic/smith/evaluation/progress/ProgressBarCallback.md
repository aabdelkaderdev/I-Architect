<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback -->

Classv1.2.13 (latest)●Since v1.0

# ProgressBarCallback


```
ProgressBarCallback(
  self,
  total: int,
  ncols: int = 50,
  end_with: str
```

## Bases

`base_callbacks.BaseCallbackHandler`

## Constructors

## Attributes

## Methods

## Inherited from[BaseCallbackHandler](/python/langchain-core/callbacks/base/BaseCallbackHandler)(langchain\_core)

### Attributes

[Araise\_error](/python/langchain-core/callbacks/base/BaseCallbackHandler/raise_error)[Arun\_inline](/python/langchain-core/callbacks/base/BaseCallbackHandler/run_inline)[Aignore\_llm](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_llm)[Aignore\_retry](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_retry)[A](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_chain)



=

'\n'

)

ignore\_chain

[Aignore\_agent](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_agent)

[Aignore\_retriever](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_retriever)

[Aignore\_chat\_model](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_chat_model)

[Aignore\_custom\_event](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_custom_event)

## Inherited from[LLMManagerMixin](/python/langchain-core/callbacks/base/LLMManagerMixin)(langchain\_core)

### Methods

[Mon\_llm\_new\_token](/python/langchain-core/callbacks/base/LLMManagerMixin/on_llm_new_token)

## Inherited from[ChainManagerMixin](/python/langchain-core/callbacks/base/ChainManagerMixin)(langchain\_core)

### Methods

[Mon\_agent\_action](/python/langchain-core/callbacks/base/ChainManagerMixin/on_agent_action)[Mon\_agent\_finish](/python/langchain-core/callbacks/base/ChainManagerMixin/on_agent_finish)

## Inherited from[CallbackManagerMixin](/python/langchain-core/callbacks/base/CallbackManagerMixin)(langchain\_core)

### Methods

[Mon\_llm\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_llm_start)[Mon\_chat\_model\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chat_model_start)[Mon\_retriever\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_retriever_start)[Mon\_chain\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chain_start)[Mon\_tool\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_tool_start)

## Inherited from[RunManagerMixin](/python/langchain-core/callbacks/base/RunManagerMixin)(langchain\_core)

### Methods

[Mon\_text](/python/langchain-core/callbacks/base/RunManagerMixin/on_text)[Mon\_retry](/python/langchain-core/callbacks/base/RunManagerMixin/on_retry)[Mon\_custom\_event](/python/langchain-core/callbacks/base/RunManagerMixin/on_custom_event)

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `total`\* | `int` | The total number of items to be processed. |
| `ncols` | `int` | Default:`50`  The character width of the progress bar. |
| `end_with` | `str` | Default:`'\n'`  Last string to print after progress bar reaches end. |

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| total | [int](https://docs.python.org/3/library/functions.html#int) |
| ncols | [int](https://docs.python.org/3/library/functions.html#int) |
| end\_with | [str](https://docs.python.org/3/library/stdtypes.html#str) |

[attribute

total: total](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/total)

[attribute

ncols: ncols](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/ncols)

[attribute

end\_with: end\_with](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/end_with)

[attribute

counter: int](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/counter)

[attribute

lock](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/lock)

[method

increment

Increment the counter and update the progress bar.](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/increment)

[method

on\_chain\_error](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/on_chain_error)

[method

on\_chain\_end](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/on_chain_end)

[method

on\_retriever\_error](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/on_retriever_error)

[method

on\_retriever\_end](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/on_retriever_end)

[method

on\_llm\_error](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/on_llm_error)

[method

on\_llm\_end](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/on_llm_end)

[method

on\_tool\_error](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/on_tool_error)

[method

on\_tool\_end](/python/langchain-classic/smith/evaluation/progress/ProgressBarCallback/on_tool_end)

A simple progress bar for the console.