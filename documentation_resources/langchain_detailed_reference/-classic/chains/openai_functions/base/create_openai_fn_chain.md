<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/base/create_openai_fn_chain -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# create\_openai\_fn\_chain

[Legacy] Create an LLM chain that uses OpenAI functions.


```
create_openai_fn_chain(
  functions: Sequence[dict[str, Any] | type[BaseModel] | Callable],
  llm: BaseLanguageModel,
  prompt: BasePromptTemplate,
  *,
  enforce_single_function_usage: bool = True,
  output_key: str = 'function',
  output_parser: BaseLLMOutputParser | None = None,
  **kwargs: Any = {}
) -> LLMChain
```

**Example:**

```
from typing import Optional

from langchain_classic.chains.openai_functions import create_openai_fn_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field

class RecordPerson(BaseModel):
    """Record some identifying information about a person."""

    name: str = Field(..., description="The person's name")
    age: int = Field(..., description="The person's age")
    fav_food: str | None = Field(None, description="The person's favorite food")

class RecordDog(BaseModel):
    """Record some identifying information about a dog."""

    name: str = Field(..., description="The dog's name")
    color: str = Field(..., description="The dog's color")
    fav_food: str | None = Field(None, description="The dog's favorite food")

model = ChatOpenAI(model="gpt-4", temperature=0)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a world class algorithm for recording entities."),
        ("human", "Make calls to the relevant function to record the entities in the following input: {input}"),
        ("human", "Tip: Make sure to answer in the correct format"),
    ]
)
chain = create_openai_fn_chain([RecordPerson, RecordDog], model, prompt)
chain.run("Harry was a chubby brown beagle who loved chicken")
# -> RecordDog(name="Harry", color="brown", fav_food="chicken")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `functions`\* | `Sequence[dict[str, Any] | type[BaseModel] | Callable]` | A sequence of either dictionaries, pydantic.BaseModels classes, or Python functions. If dictionaries are passed in, they are assumed to already be a valid OpenAI functions. If only a single function is passed in, then it will be enforced that the model use that function. pydantic.BaseModels and Python functions should have docstrings describing what the function does. For best results, pydantic.BaseModels should have descriptions of the parameters and Python functions should have Google Python style args descriptions in the docstring. Additionally, Python functions should only use primitive types (str, int, float, bool) or pydantic.BaseModels for arguments. |
| `llm`\* | `BaseLanguageModel` | Language model to use, assumed to support the OpenAI function-calling API. |
| `prompt`\* | `BasePromptTemplate` | BasePromptTemplate to pass to the model. |
| `enforce_single_function_usage` | `bool` | Default:`True`  only used if a single function is passed in. If True, then the model will be forced to use the given function. If `False`, then the model will be given the option to use the given function or not. |
| `output_key` | `str` | Default:`'function'`  The key to use when returning the output in LLMChain.**call**. |
| `output_parser` | `BaseLLMOutputParser | None` | Default:`None`  BaseLLMOutputParser to use for parsing model outputs. By default will be inferred from the function types. If pydantic.BaseModels are passed in, then the OutputParser will try to parse outputs using those. Otherwise model outputs will simply be parsed as JSON. If multiple functions are passed in and they are not pydantic.BaseModels, the chain output will include both the name of the function that was returned and the arguments to pass to the function. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments to pass to LLMChain. |


