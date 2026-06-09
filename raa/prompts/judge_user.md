{{! Judge — User Prompt }}
Evaluate the following candidate architecture against the batch's requirements.

{{! Batch Requirements — all ASRs and non-ASRs }}
Requirements in this batch:
{{#requirements}}
- [{{id}}] {{text}}
{{/requirements}}

{{! ASR Proposals }}
Proposals from the ASR Subgraph:
{{#asr_proposals}}
- proposal_ref: {{proposal_ref}}
  proposed_name: {{proposed_name}}
  proposing_subgraph: {{proposing_subgraph}}
  c4_level: {{c4_level}}, c4_type: {{c4_type}}
  description: {{description}}
  responsibilities: {{#responsibilities}}- {{.}}
  {{/responsibilities}}
  source_requirements: {{source_requirements_joined}}
  justification: {{justification}}
{{/asr_proposals}}

{{! Non-ASR Proposals }}
Proposals from the Non-ASR Subgraph:
{{#non_asr_proposals}}
- proposal_ref: {{proposal_ref}}
  proposed_name: {{proposed_name}}
  proposing_subgraph: {{proposing_subgraph}}
  c4_level: {{c4_level}}, c4_type: {{c4_type}}
  description: {{description}}
  responsibilities: {{#responsibilities}}- {{.}}
  {{/responsibilities}}
  source_requirements: {{source_requirements_joined}}
  justification: {{justification}}
{{/non_asr_proposals}}

{{#registry_snapshot.entries}}
Existing registry entries:
{{#.}}
- {{canonical_name}} ({{canonical_id}}, {{c4_type}}): {{description}}
{{/.}}
{{/registry_snapshot.entries}}

---

**Your task for this call:** {{step_instruction}}

Return ONLY the requested output fields. Do not execute other SAAM steps.
Return one annotation per proposal using proposal_ref as the identifier.
Do not echo the full proposal object.
