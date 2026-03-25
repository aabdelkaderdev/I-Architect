<!-- Source: https://reference.langchain.com/python/langchain-core/utils/utils/mock_now -->

Functionv1.2.21 (latest)●Since v0.1

# mock\_now

Context manager for mocking out datetime.now() in unit tests.


```
mock_now(
    dt_value: datetime.datetime,
) -> Iterator[type]
```

**Example:**

```
with mock_now(datetime.datetime(2011, 2, 3, 10, 11)):
    assert datetime.datetime.now() == datetime.datetime(2011, 2, 3, 10, 11)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `dt_value`\* | `datetime.datetime` | The datetime value to use for datetime.now(). |


