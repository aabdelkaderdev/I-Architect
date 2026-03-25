<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/RecordManager/get_time -->

Methodv1.2.21 (latest)●Since v0.1

# get\_time

Get the current server time as a high resolution timestamp!

It's important to get this from the server to ensure a monotonic clock,
otherwise there may be data loss when cleaning up old documents!


```
get_time(
    self,
) -> float
```


