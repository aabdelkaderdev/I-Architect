---
variables:
  - name: diagram_type
    type: string
  - name: focus_entity_id
    type: string
  - name: focus_entity_label
    type: string
  - name: focus_entity_description
    type: string
  - name: elements_block
    type: string
  - name: relationships_block
    type: string
---
{{! skill: c4:rules as c4_rules }}

Generate PlantUML code for a {{diagram_type}} diagram.

## Focus Entity
- ID: {{focus_entity_id}}
- Label: {{focus_entity_label}}
- Description: {{focus_entity_description}}

## Elements
{{{elements_block}}}

## Relationships
{{{relationships_block}}}

## Generation Rules
{{{c4_rules}}}

Produce valid PlantUML wrapped in @startuml / @enduml.
Include LAYOUT_WITH_LEGEND() at the end.
