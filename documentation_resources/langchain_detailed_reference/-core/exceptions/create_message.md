<!-- Source: https://reference.langchain.com/python/langchain-core/exceptions/create_message -->

Functionv1.2.21 (latest)●Since v0.3

# create\_message

Create a message with a link to the LangChain troubleshooting guide.


```
create_message(
    *,
    message: str,
    error_code: ErrorCode,
) -> str
```

**Example:**

```
create_message(
    message="Failed to parse output",
    error_code=ErrorCode.OUTPUT_PARSING_FAILURE,
)
"Failed to parse output. For troubleshooting, visit: ..."
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `message`\* | `str` | The message to display. |
| `error_code`\* | `ErrorCode` | The error code to display. |


