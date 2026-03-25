<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/structured/StructuredOutputParser/get_format_instructions -->

Methodv1.2.13 (latest)●Since v1.0

# get\_format\_instructions

Get format instructions for the output parser.

Example:

```
from langchain_classic.output_parsers.structured import (
    StructuredOutputParser, ResponseSchema
)

response_schemas = [
    ResponseSchema(
        name="foo",
        description="a list of strings",
        type="List[string]"
        ),
    ResponseSchema(
        name="bar",
        description="a string",
        type="string"
        ),
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)

print(parser.get_format_instructions())  # noqa: T201

output:
# The output should be a Markdown code snippet formatted in the following
# schema, including the leading and trailing "```json" and "```":
#
# ```json
# {
#     "foo": List[string]  // a list of strings
#     "bar": string  // a string
# }
# ```

Args:
    only_json: If `True`, only the json in the Markdown code snippet
        will be returned, without the introducing text.
```


```
get_format_instructions(
    self,
    only_json: bool = False,
) -> str
```


