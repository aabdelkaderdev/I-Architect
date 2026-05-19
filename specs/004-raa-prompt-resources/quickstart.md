# Quickstart: RAA Prompt Resource Bundle

This guide explains how RAA runtime nodes load prompt templates and excerpts from the Prompt Resource Bundle.

## 1. Dynamic Prompt Building

Nodes fetch relevant prompt files dynamically during execution. The following python snippet demonstrates how helper functions read the resource files:

```python
import os
from pathlib import Path

PROMPTS_DIR = Path("raa/prompts")

def get_constraint(name: str) -> str:
    """Reads a constraint file, e.g., 'c4_constraints'."""
    filepath = PROMPTS_DIR / f"{name}.md"
    return filepath.read_text(encoding="utf-8").strip()

def get_excerpt(tag: str) -> str:
    """Reads an excerpt file using a tag name, mapping ':' to '_'."""
    filename = tag.replace(":", "_") + ".txt"
    filepath = PROMPTS_DIR / "excerpts" / filename
    return filepath.read_text(encoding="utf-8").strip()
```

## 2. Example Usage in LLM Node Prompt Template

When constructing the prompt for the Entity Extraction node:
```python
system_prompt = f"""
You are an architectural entity extraction assistant.
Follow these C4 Model constraints:
{get_constraint('c4_constraints')}

Recall these definitions:
- Levels: {get_excerpt('c4:levels')}
- Notation: {get_excerpt('c4:notation')}
"""
```
This ensures the agent uses the precise authoritative guidelines without bloating the context window with the entire C4 specification.
