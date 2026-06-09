{{! ASR Subgraph — User Prompt }}
Analyse the following inputs and propose architecturally significant entities.

{{! Quality Weights — ordered by priority }}
The system's quality attribute priorities are:
{{#quality_weights}}
- {{@key}}: {{.}}
{{/quality_weights}}

{{#condition}}
Operational condition: {{condition}}
{{/condition}}

{{! Architectural Decisions }}
{{#decisions}}
- Selected pattern: {{selected_pattern}}
{{/decisions}}

{{! ASR Requirements }}
Architecturally significant requirements for this batch:
{{#asrs}}
- [{{id}}] {{text}} (Quality attributes: {{quality_attributes_joined}})
{{/asrs}}

{{! Registry Snapshot — entities already registered }}
{{#registry_snapshot.entries}}
Entities already defined in the system:
{{#.}}
- {{canonical_name}} ({{c4_type}}): {{description}}
{{/.}}
{{/registry_snapshot.entries}}

{{^registry_snapshot.entries}}
No entities have been registered yet.
{{/registry_snapshot.entries}}

Propose entities implied by the ASRs and decisions above. For each entity, explain
your justification. Do NOT propose entities already present in the registry snapshot.
