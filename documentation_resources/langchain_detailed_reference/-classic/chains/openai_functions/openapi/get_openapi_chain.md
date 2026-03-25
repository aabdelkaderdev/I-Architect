<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/openapi/get_openapi_chain -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# get\_openapi\_chain

Create a chain for querying an API from a OpenAPI spec.


```
get_openapi_chain(
  spec: OpenAPISpec | str,
  llm: BaseLanguageModel | None = None,
  prompt: BasePromptTemplate | None = None,
  request_chain: Chain | None = None,
  llm_chain_kwargs: dict | None = None,
  verbose: bool = False,
  headers: dict | None = None,
  params: dict | None = None,
  **kwargs: Any = {}
) -> SequentialChain
```

**this class is deprecated. See below for a replacement implementation.:**

The benefits of this implementation are:

- Uses LLM tool calling features to encourage properly-formatted API requests;
- Includes async support.

```
from typing import Any

from langchain_classic.chains.openai_functions.openapi import openapi_spec_to_openai_fn
from langchain_community.utilities.openapi import OpenAPISpec
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Define API spec. Can be JSON or YAML
api_spec = \"\"\"
{
"openapi": "3.1.0",
"info": {
    "title": "JSONPlaceholder API",
    "version": "1.0.0"
},
"servers": [
    {
    "url": "https://jsonplaceholder.typicode.com"
    }
],
"paths": {
    "/posts": {
    "get": {
        "summary": "Get posts",
        "parameters": [
        {
            "name": "_limit",
            "in": "query",
            "required": false,
            "schema": {
            "type": "integer",
            "example": 2
            },
            "description": "Limit the number of results"
        }
        ]
    }
    }
}
}
\"\"\"

parsed_spec = OpenAPISpec.from_text(api_spec)
openai_fns, call_api_fn = openapi_spec_to_openai_fn(parsed_spec)
tools = [
    {"type": "function", "function": fn}
    for fn in openai_fns
]

prompt = ChatPromptTemplate.from_template(
    "Use the provided APIs to respond to this user query:\\n\\n{query}"
)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)

def _execute_tool(message) -> Any:
    if tool_calls := message.tool_calls:
        tool_call = message.tool_calls[0]
        response = call_api_fn(name=tool_call["name"], fn_args=tool_call["args"])
        response.raise_for_status()
        return response.json()
    else:
        return message.content

chain = prompt | model | _execute_tool
```

```
response = chain.invoke({"query": "Get me top two posts."})
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `spec`\* | `OpenAPISpec | str` | OpenAPISpec or url/file/text string corresponding to one. |
| `llm` | `BaseLanguageModel | None` | Default:`None`  language model, should be an OpenAI function-calling model, e.g. `ChatOpenAI(model="gpt-3.5-turbo-0613")`. |
| `prompt` | `BasePromptTemplate | None` | Default:`None`  Main prompt template to use. |
| `request_chain` | `Chain | None` | Default:`None`  Chain for taking the functions output and executing the request. |
| `params` | `dict | None` | Default:`None`  Request parameters. |
| `headers` | `dict | None` | Default:`None`  Request headers. |
| `verbose` | `bool` | Default:`False`  Whether to run the chain in verbose mode. |
| `llm_chain_kwargs` | `dict | None` | Default:`None`  LLM chain additional keyword arguments. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments to pass to the chain. |


