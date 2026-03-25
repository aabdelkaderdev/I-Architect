<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/format_instructions/PYDANTIC_FORMAT_INSTRUCTIONS -->

Attributev1.2.13 (latest)●Since v1.0

# PYDANTIC\_FORMAT\_INSTRUCTIONS


```
PYDANTIC_FORMAT_INSTRUCTIONS = 'The output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}\nthe object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.\n\nHere is the output schema:\n```\n{schema}\n```'
```


