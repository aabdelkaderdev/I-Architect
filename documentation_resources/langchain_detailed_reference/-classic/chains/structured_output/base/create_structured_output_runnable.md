<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/structured_output/base/create_structured_output_runnable -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# create\_structured\_output\_runnable

Create a runnable for extracting structured outputs.


```
create_structured_output_runnable(
  output_schema: dict[str, Any] | type[BaseModel],
  llm: Runnable,
  prompt: BasePromptTemplate | None = None,
  *,
  output_parser: BaseOutputParser | BaseGenerationOutputParser | None = None,
  enforce_function_usage: bool = True,
  return_single: bool = True,
  mode: Literal['openai-functions', 'openai-tools', 'openai-json'] = 'openai-functions',
  **kwargs: Any = {}
) -> Runnable
```

OpenAI tools example with Pydantic schema (mode='openai-tools'):

```
from typing import Optional

from langchain_classic.chains import create_structured_output_runnable
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class RecordDog(BaseModel):
    '''Record some identifying information about a dog.'''

    name: str = Field(..., description="The dog's name")
    color: str = Field(..., description="The dog's color")
    fav_food: str | None = Field(None, description="The dog's favorite food")

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an extraction algorithm. Please extract every possible instance"),
        ('human', '{input}')
    ]
)
structured_model = create_structured_output_runnable(
    RecordDog,
    model,
    mode="openai-tools",
    enforce_function_usage=True,
    return_single=True
)
structured_model.invoke({"input": "Harry was a chubby brown beagle who loved chicken"})
# -> RecordDog(name="Harry", color="brown", fav_food="chicken")
```

OpenAI tools example with dict schema (mode="openai-tools"):

```
from typing import Optional

from langchain_classic.chains import create_structured_output_runnable
from langchain_openai import ChatOpenAI

dog_schema = {
    "type": "function",
    "function": {
        "name": "record_dog",
        "description": "Record some identifying information about a dog.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "description": "The dog's name",
                    "type": "string"
                },
                "color": {
                    "description": "The dog's color",
                    "type": "string"
                },
                "fav_food": {
                    "description": "The dog's favorite food",
                    "type": "string"
                }
            },
            "required": ["name", "color"]
        }
    }
}

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
structured_model = create_structured_output_runnable(
    dog_schema,
    model,
    mode="openai-tools",
    enforce_function_usage=True,
    return_single=True
)
structured_model.invoke("Harry was a chubby brown beagle who loved chicken")
# -> {'name': 'Harry', 'color': 'brown', 'fav_food': 'chicken'}
```

OpenAI functions example (mode="openai-functions"):

```
from typing import Optional

from langchain_classic.chains import create_structured_output_runnable
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class Dog(BaseModel):
    '''Identifying information about a dog.'''

    name: str = Field(..., description="The dog's name")
    color: str = Field(..., description="The dog's color")
    fav_food: str | None = Field(None, description="The dog's favorite food")

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
structured_model = create_structured_output_runnable(Dog, model, mode="openai-functions")
structured_model.invoke("Harry was a chubby brown beagle who loved chicken")
# -> Dog(name="Harry", color="brown", fav_food="chicken")
```

**OpenAI functions with prompt example:**

```
from typing import Optional

from langchain_classic.chains import create_structured_output_runnable
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class Dog(BaseModel):
    '''Identifying information about a dog.'''

    name: str = Field(..., description="The dog's name")
    color: str = Field(..., description="The dog's color")
    fav_food: str | None = Field(None, description="The dog's favorite food")

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
structured_model = create_structured_output_runnable(Dog, model, mode="openai-functions")
system = '''Extract information about any dogs mentioned in the user input.'''
prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{input}"),]
)
chain = prompt | structured_model
chain.invoke({"input": "Harry was a chubby brown beagle who loved chicken"})
# -> Dog(name="Harry", color="brown", fav_food="chicken")
```

OpenAI json response format example (mode="openai-json"):

```
from typing import Optional

from langchain_classic.chains import create_structured_output_runnable
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class Dog(BaseModel):
    '''Identifying information about a dog.'''

    name: str = Field(..., description="The dog's name")
    color: str = Field(..., description="The dog's color")
    fav_food: str | None = Field(None, description="The dog's favorite food")

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
structured_model = create_structured_output_runnable(Dog, model, mode="openai-json")
system = '''You are a world class assistant for extracting information in structured JSON formats. 
Extract a valid JSON blob from the user input that matches the following JSON Schema:

{output_schema}'''
prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{input}"),]
)
chain = prompt | structured_model
chain.invoke({"input": "Harry was a chubby brown beagle who loved chicken"})
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `output_schema`\* | `dict[str, Any] | type[BaseModel]` | Either a dictionary or pydantic.BaseModel class. If a dictionary is passed in, it's assumed to already be a valid JsonSchema. For best results, pydantic.BaseModels should have docstrings describing what the schema represents and descriptions for the parameters. |
| `llm`\* | `Runnable` | Language model to use. Assumed to support the OpenAI function-calling API if mode is 'openai-function'. Assumed to support OpenAI response\_format parameter if mode is 'openai-json'. |
| `prompt` | `BasePromptTemplate | None` | Default:`None`  BasePromptTemplate to pass to the model. If mode is 'openai-json' and prompt has input variable 'output\_schema' then the given output\_schema will be converted to a JsonSchema and inserted in the prompt. |
| `output_parser` | `BaseOutputParser | BaseGenerationOutputParser | None` | Default:`None`  Output parser to use for parsing model outputs. By default will be inferred from the function types. If pydantic.BaseModel is passed in, then the OutputParser will try to parse outputs using the pydantic class. Otherwise model outputs will be parsed as JSON. |
| `mode` | `Literal['openai-functions', 'openai-tools', 'openai-json']` | Default:`'openai-functions'`  How structured outputs are extracted from the model. If 'openai-functions' then OpenAI function calling is used with the deprecated 'functions', 'function\_call' schema. If 'openai-tools' then OpenAI function calling with the latest 'tools', 'tool\_choice' schema is used. This is recommended over 'openai-functions'. If 'openai-json' then OpenAI model with response\_format set to JSON is used. |
| `enforce_function_usage` | `bool` | Default:`True`  Only applies when mode is 'openai-tools' or 'openai-functions'. If `True`, then the model will be forced to use the given output schema. If `False`, then the model can elect whether to use the output schema. |
| `return_single` | `bool` | Default:`True`  Only applies when mode is 'openai-tools'. Whether to a list of structured outputs or a single one. If `True` and model does not return any structured outputs then chain output is None. If `False` and model does not return any structured outputs then chain output is an empty list. |
| `kwargs` | `Any` | Default:`{}`  Additional named arguments. |


