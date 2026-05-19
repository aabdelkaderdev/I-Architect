# Quickstart: RAA Skill Reference Documents

This guide describes how developers can read and verify the RAA Skill Reference Documents.

## 1. Verifying Reference Structure

You can run a simple markdown header checks script to make sure no sections are missing from the skill reference files. For example:

```python
import re
from pathlib import Path

REQUIRED_HEADERS = [
    r"^## 1\.\s+Purpose",
    r"^## 2\.\s+Input",
    r"^## 3\.\s+Normative\s+rules",
    r"^## 4\.\s+Decision\s+guidelines",
    r"^## 5\.\s+Output\s+schema",
    r"^## 6\.\s+Error\s+cases",
    r"^## 7\.\s+Examples",
]

def check_file(filepath: Path):
    content = filepath.read_text(encoding="utf-8")
    for header in REQUIRED_HEADERS:
        if not re.search(header, content, re.MULTILINE):
            print(f"[-] Missing required header: {header} in {filepath.name}")
```

## 2. Navigating References

- To check C4 level promotion or relationship mapping, consult `C4_Level_Mapping.md`.
- To inspect how entity names and identifiers are generated, consult `Entity_Extraction.md`.
- For pattern selection rules, consult `Pattern_Selection.md`.
