---
variables:
  - name: diagram_id
    type: string
  - name: error_text
    type: string
  - name: current_puml_code
    type: string
  - name: retry_count
    type: number
  - name: max_retries
    type: number
---
The PlantUML server returned a syntax error for diagram {{diagram_id}}.

## Error Text
{{{error_text}}}

## Current PlantUML Code
{{{current_puml_code}}}

## Instructions
1. Quote the error text verbatim
2. Locate the offending construct in the code
3. Apply the minimal fix to resolve the error
4. Return the corrected PlantUML code

Attempt {{retry_count}} of {{max_retries}}.
