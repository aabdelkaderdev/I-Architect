{{! Example: Non-ASR User Type }}
**Example — User Type (functional requirement implies a human actor)**

Input:
- Non-ASR: "System administrators shall be able to view audit logs filtered by date range and user."

Expected output:
```json
{
  "proposed_name": "SystemAdmin",
  "c4_level": "system",
  "c4_type": "actor",
  "description": "Human administrator who monitors system activity and reviews audit logs.",
  "responsibilities": [
    "View and filter audit logs",
    "Monitor system health and compliance"
  ],
  "source_requirements": ["REQ-XXX"],
  "proposing_subgraph": "non_asr",
  "justification": "The requirement describes a distinct human role with specific permissions (audit log access), which maps to the SystemAdmin actor in the C4 model."
}
```
