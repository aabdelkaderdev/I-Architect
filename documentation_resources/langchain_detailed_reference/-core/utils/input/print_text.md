<!-- Source: https://reference.langchain.com/python/langchain-core/utils/input/print_text -->

Functionv1.2.21 (latest)●Since v0.1

# print\_text

Print text with highlighting and no end characters.

If a color is provided, the text will be printed in that color.

If a file is provided, the text will be written to that file.


```
print_text(
  text: str,
  color: str | None = None,
  end: str = '',
  file: TextIO | None = None
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The text to print. |
| `color` | `str | None` | Default:`None`  The color to use. |
| `end` | `str` | Default:`''`  The end character to use. |
| `file` | `TextIO | None` | Default:`None`  The file to write to. |


