<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/chat_models/ChatModelTests/structured_output_kwargs -->

Attributev1.1.4 (latest)●Since v1.1

# structured\_output\_kwargs

Additional kwargs to pass to `with_structured_output()` in tests.

Override this property to customize how structured output is generated
for your model. The most common use case is specifying the `method`
parameter, which controls the mechanism used to enforce structured output:

- `'function_calling'`: Uses tool/function calling to enforce the schema.
- `'json_mode'`: Uses the model's JSON mode.
- `'json_schema'`: Uses native JSON schema support (e.g., OpenAI's
  structured outputs).


```
structured_output_kwargs: dict[str, Any]
```

**Example:**

```
@property
def structured_output_kwargs(self) -> dict:
    return {"method": "json_schema"}
```


