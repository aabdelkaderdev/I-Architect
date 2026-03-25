<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/format_instructions/JSON_FORMAT_INSTRUCTIONS -->

Attributev1.2.21 (latest)●Since v0.1

# JSON\_FORMAT\_INSTRUCTIONS


```
JSON_FORMAT_INSTRUCTIONS = 'STRICT OUTPUT FORMAT:\n- Return only the JSON value that conforms to the schema. Do not include any additional text, explanations, headings, or separators.\n- Do not wrap the JSON in Markdown or code fences (
  no ``` or ```json).\n- Do not prepend or append any text (e.g.,
  do not write "Here is the JSON:").\n- The response must be a single top-level JSON value exactly as required by the schema (object/array/etc.), with no trailing commas or comments.\n\nThe output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}} the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.\n\nHere is the output schema (shown in a code block for readability only — do not include any backticks or Markdown in your output
):\n```\n{schema}\n```'
```


