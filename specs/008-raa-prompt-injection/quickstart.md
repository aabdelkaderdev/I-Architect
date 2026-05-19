# Quickstart: Prompt Constraint Injection

This guide demonstrates how to load constraint excerpts for RAA nodes.

## 1. Retrieving a Single Tag Excerpt

```python
from raa.utils.prompt_loader import load_excerpt

# Load c4 levels constraints
c4_levels_text = load_excerpt("c4:levels")
print(c4_levels_text)
```

## 2. Retrieving Excerpts for a Node

```python
from raa.utils.prompt_loader import get_node_constraints

# Load constraints for relationship extraction node
constraints = get_node_constraints("relationship_extraction")
# Returns a dictionary mapping tags to their string content:
# {
#     "c4:notation": "...",
#     "c4:technology": "..."
# }
```

## 3. Formatting Prompt Excerpts

```python
from raa.utils.prompt_loader import format_constraints_block

constraints = get_node_constraints("pattern_selection")
block = format_constraints_block(constraints)
# Outputs:
# --- CONSTRAINTS ---
# [c4:levels]
# ...
# -------------------
```
