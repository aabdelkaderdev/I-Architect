{{! Example: Judge Evaluation Chain }}
**Example — Full SAAM Evaluation Chain**

Scenario (shared across all steps):
- ASR: "The system shall encrypt all customer PII at rest using AES-256."
  Quality attributes: [Security]
- Non-ASR: "Customers can download their data as a CSV file."
- Registry: empty (first batch)

Proposals from subgraphs:
- ASR: EncryptionService (service) — encrypts and decrypts PII data at rest
- Non-ASR: DataExportService (service) — generates CSV exports of customer data

---

**Step 3 — Classification:**
- EncryptionService → direct (the ASR explicitly references encryption)
- DataExportService → direct (the non-ASR explicitly references data export)

**Step 4 — Coverage:**
- REQ-001 (encryption): satisfied by EncryptionService — it encrypts PII at rest
- REQ-010 (CSV export): satisfied by DataExportService — it generates CSV files
- No coverage gaps.

**Step 5 — Interactions:**
- No shared entity names between proposals → no interactions, no conflicts.
