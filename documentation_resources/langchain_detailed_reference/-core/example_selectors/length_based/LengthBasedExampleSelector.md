<!-- Source: https://reference.langchain.com/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector -->

Classv1.2.21 (latest)●Since v0.1

# LengthBasedExampleSelector

Select examples based on length.


```
LengthBasedExampleSelector()
```

## Bases

`BaseExampleSelector``BaseModel`

**Example:**

```
from langchain_core.example_selectors import LengthBasedExampleSelector
from langchain_core.prompts import PromptTemplate

# Define examples
examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "fast", "output": "slow"},
]

# Create prompt template
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}",
)

# Create selector with max length constraint
selector = LengthBasedExampleSelector(
    examples=examples,
    example_prompt=example_prompt,
    max_length=50,  # Maximum prompt length
)

# Select examples for a new input
selected = selector.select_examples({"input": "large", "output": "tiny"})
# Returns examples that fit within max_length constraint
```

## Attributes

[attribute

examples: list[dict]

A list of the examples that the prompt template expects.](/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector/examples)[attribute

example\_prompt: PromptTemplate

Prompt template used to format the examples.](/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector/example_prompt)[attribute

get\_text\_length: Callable[[str], int]

Function to measure prompt length. Defaults to word count.](/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector/get_text_length)[attribute

max\_length: int

Max length for the prompt, beyond which examples are cut.](/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector/max_length)[attribute

example\_text\_lengths: list[int]

Length of each example.](/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector/example_text_lengths)

## Methods

[method

add\_example

Add new example to list.](/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector/add_example)[method

aadd\_example

Async add new example to list.](/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector/aadd_example)[method

post\_init

Validate that the examples are formatted correctly.](/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector/post_init)[method

select\_examples

Select which examples to use based on the input lengths.](/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector/select_examples)[method

aselect\_examples

Async select which examples to use based on the input lengths.](/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector/aselect_examples)


