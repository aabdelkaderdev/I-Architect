<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/structured_output/base/create_openai_fn_runnable -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# create\_openai\_fn\_runnable

Create a runnable sequence that uses OpenAI functions.


```
create_openai_fn_runnable(
  functions: Sequence[dict[str, Any] | type[BaseModel] | Callable],
  llm: Runnable,
  prompt: BasePromptTemplate | None = None,
  *,
  enforce_single_function_usage: bool = True,
  output_parser: BaseOutputParser | BaseGenerationOutputParser | None = None,
  **llm_kwargs: Any = {}
) -> Runnable
```

**Example:**

```
from typing import Optional

from langchain_classic.chains.structured_output import create_openai_fn_runnable
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class RecordPerson(BaseModel):
    '''Record some identifying information about a person.'''

    name: str = Field(..., description="The person's name")
    age: int = Field(..., description="The person's age")
    fav_food: str | None = Field(None, description="The person's favorite food")

class RecordDog(BaseModel):
    '''Record some identifying information about a dog.'''

    name: str = Field(..., description="The dog's name")
    color: str = Field(..., description="The dog's color")
    fav_food: str | None = Field(None, description="The dog's favorite food")

model = ChatOpenAI(model="gpt-4", temperature=0)
structured_model = create_openai_fn_runnable([RecordPerson, RecordDog], model)
structured_model.invoke("Harry was a chubby brown beagle who loved chicken)
# -> RecordDog(name="Harry", color="brown", fav_food="chicken")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `functions`\* | `Sequence[dict[str, Any] | type[BaseModel] | Callable]` | A sequence of either dictionaries, pydantic.BaseModels classes, or Python functions. If dictionaries are passed in, they are assumed to already be a valid OpenAI functions. If only a single function is passed in, then it will be enforced that the model use that function. pydantic.BaseModels and Python functions should have docstrings describing what the function does. For best results, pydantic.BaseModels should have descriptions of the parameters and Python functions should have Google Python style args descriptions in the docstring. Additionally, Python functions should only use primitive types (str, int, float, bool) or pydantic.BaseModels for arguments. |
| `llm`\* | `Runnable` | Language model to use, assumed to support the OpenAI function-calling API. |
| `prompt` | `BasePromptTemplate | None` | Default:`None`  BasePromptTemplate to pass to the model. |
| `enforce_single_function_usage` | `bool` | Default:`True`  only used if a single function is passed in. If True, then the model will be forced to use the given function. If `False`, then the model will be given the option to use the given function or not. |
| `output_parser` | `BaseOutputParser | BaseGenerationOutputParser | None` | Default:`None`  BaseLLMOutputParser to use for parsing model outputs. By default will be inferred from the function types. If pydantic.BaseModels are passed in, then the OutputParser will try to parse outputs using those. Otherwise model outputs will simply be parsed as JSON. If multiple functions are passed in and they are not pydantic.BaseModels, the chain output will include both the name of the function that was returned and the arguments to pass to the function. |
| `**llm_kwargs` | `Any` | Default:`{}`  Additional named arguments to pass to the language model. |


