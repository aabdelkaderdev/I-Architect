<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_execution/BaseExecutionPolicy/spawn -->

Methodv1.2.13 (latest)●Since v1.0

# spawn

Launch the persistent shell process.


```
spawn(
  self,
  *,
  workspace: Path,
  env: Mapping[str, str],
  command: Sequence[str]
) -> subprocess.Popen[str]
```


