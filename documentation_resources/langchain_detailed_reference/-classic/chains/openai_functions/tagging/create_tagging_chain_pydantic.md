<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/tagging/create_tagging_chain_pydantic -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# create\_tagging\_chain\_pydantic

Create tagging chain from Pydantic schema.

Create a chain that extracts information from a passage
based on a Pydantic schema.

This function is deprecated. Please use `with_structured_output` instead.
See example usage below:

```
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic

class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")

# Or any other chat model that supports tools.
# Please reference to the documentation of structured_output
# to see an up to date list of which models support
# with_structured_output.
model = ChatAnthropic(model="claude-opus-4-1-20250805", temperature=0)
structured_model = model.with_structured_output(Joke)
structured_model.invoke(
    "Why did the cat cross the road? To get to the other "
    "side... and then lay down in the middle of it!"
)
```

Read more here: <https://docs.langchain.com/oss/python/langchain/models#structured-outputs>


```
create_tagging_chain_pydantic(
  pydantic_schema: Any,
  llm: BaseLanguageModel,
  prompt: ChatPromptTemplate | None = None,
  **kwargs: Any = {}
) -> Chain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `pydantic_schema`\* | `Any` | The Pydantic schema of the entities to extract. |
| `llm`\* | `BaseLanguageModel` | The language model to use. |
| `prompt` | `ChatPromptTemplate | None` | Default:`None`  The prompt template to use for the chain. |
| `kwargs` | `Any` | Default:`{}`  Additional keyword arguments to pass to the chain. |


