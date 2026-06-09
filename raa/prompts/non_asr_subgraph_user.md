{{! Non-ASR Subgraph — User Prompt }}
Analyse the following functional requirements and propose entities they imply.

{{! Non-ASR Requirements }}
Functional requirements for this batch:
{{#non_asrs}}
- [{{id}}] {{text}}
{{/non_asrs}}

{{#registry_snapshot.entries}}
Entities already defined in the system:
{{#.}}
- {{canonical_name}} ({{c4_type}}): {{description}}
{{/.}}
{{/registry_snapshot.entries}}

{{^registry_snapshot.entries}}
No entities have been registered yet.
{{/registry_snapshot.entries}}

Propose entities implied by the functional requirements above. Focus on user types,
external systems, and feature-bearing services that the requirements suggest but
do not explicitly name. Do NOT propose entities already present in the registry.
