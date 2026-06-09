---
variables:
  - {name: diagram_type, type: string}
  - {name: is_context, type: boolean}
  - {name: is_container, type: boolean}
  - {name: is_component, type: boolean}
  - {name: system_name, type: string}
  - {name: system_description, type: string}
  - {name: actors_json, type: string}
  - {name: external_systems_json, type: string}
  - {name: concern_id, type: string}
  - {name: condition, type: string}
  - {name: containers_json, type: string}
  - {name: parent_container_id, type: string}
  - {name: components_json, type: string}
  - {name: relationships_json, type: string}
---
{{! skill: c4:rules as c4_rules }}

Generate PlantUML code for a **{{diagram_type}}** C4 diagram.

{{#is_context}}
- Include `@startuml`, then `!include` for `C4_Context.puml`.
- Declare a `System(...)` for "{{system_name}}" with description "{{system_description}}".
- Declare each actor below as `Person(canonical_id, name, description)`.
- Declare each external system as `System_Ext(canonical_id, name, description)`.
- Emit one `Rel(...)` per relationship below.
- Actors and external systems are from:
{{{actors_json}}}
{{{external_systems_json}}}
{{/is_context}}

{{#is_container}}
- Include `@startuml`, then `!include` for `C4_Container.puml`.
- Wrap all containers in `System_Boundary({{concern_id}}, "{{condition}}")`.
- Declare each container as `Container(canonical_id, name, "", description)`.
  Use an empty technology string unless a technology field is explicitly present
  in the serialized container data.
- Containers are from:
{{{containers_json}}}
{{/is_container}}

{{#is_component}}
- Include `@startuml`, then `!include` for `C4_Component.puml`.
- Wrap all components in `Container_Boundary({{parent_container_id}}, "{{parent_container_id}}")`.
- Declare each component as `Component(canonical_id, name, "", description)`.
  Use an empty technology string unless a technology field is explicitly present
  in the serialized component data.
- Components are from:
{{{components_json}}}
{{/is_component}}

## Relationships
{{{relationships_json}}}

## C4 Syntax Reference
{{{c4_rules}}}

Produce valid PlantUML wrapped in `@startuml` / `@enduml`.
Include `LAYOUT_WITH_LEGEND()` before `@enduml`.
Include `LAYOUT_LANDSCAPE()` as the very last macro before `@enduml`.
Use each entity's `canonical_id` as the PlantUML alias, but replace hyphens
(`-`) with underscores (`_`). Example: `ENT-003` → `ENT_003`.
