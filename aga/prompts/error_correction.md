---
variables:
  - {name: diagram_id, type: string}
  - {name: error_text, type: string}
  - {name: current_puml_code, type: string}
  - {name: retry_count, type: number}
  - {name: max_retries, type: number}
---
{{! skill: c4:rules as c4_rules }}

The `render_plantuml_tool` returned an error for diagram **{{diagram_id}}**.
This is render attempt **{{retry_count}}** of **{{max_retries}}**.

## Error Text
{{{error_text}}}

## Current PlantUML Code
```plantuml
{{{current_puml_code}}}
```

## Correction Instructions
1. Briefly restate the exact tool error before changing the code.
2. Locate the specific line or construct in the code that caused the error.
3. Cross-reference the C4 rules below to identify the violated constraint.
4. Apply the **minimal fix** — do not restructure the entire diagram.
5. Return the corrected PlantUML code and call `render_plantuml_tool` again.

## C4 Rules (for cross-reference)
{{{c4_rules}}}
