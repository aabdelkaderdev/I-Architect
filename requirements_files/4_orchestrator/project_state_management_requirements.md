# Project State Management — Functional & Non-Functional Requirements

> **Version:** 1.0
> **Source Plan:** `requirements_planning/4_orchestrator/project_state_management_plan.md`
> **SRS Reference:** I-Architect SRS v2.3
> **Date:** 2026-03-24

---

## 1. Functional Requirements (FR)

### FR-PSM-001: Automatic Project Directory Scaffolding
- **Description:** Upon project creation, the system SHALL automatically generate the complete directory structure under `MEDIA_ROOT/projects/{project_uuid}/` including all mandatory subdirectories: `pdf/`, `structured_requirements/`, `filtered_requirements/`, `arlo_cache/`, `arlo_output/`, `agent_states/`, `raa_output/`, `aga_output/`, `sa_output/`, and the `user_profile.json` configuration file.
- **SRS Trace:** §2
- **Priority:** Must
- **Acceptance Criteria:** After project creation via the API, the full directory tree exists on disk and `user_profile.json` contains valid default configuration values.

### FR-PSM-002: Project Folder Name Uniqueness Validation
- **Description:** The system SHALL verify that the requested project folder name (UUID) is unique and does not conflict with any existing project. Duplicate names SHALL be rejected with a specific validation error.
- **SRS Trace:** §1.2
- **Priority:** Must
- **Acceptance Criteria:** Attempting to create a project with a duplicate UUID returns HTTP `409 Conflict` with an error message identifying the naming violation.

### FR-PSM-003: Single Document Per Project Enforcement
- **Description:** Each project SHALL accept exactly one document upload. The system SHALL reject subsequent document uploads to the same project unless the existing document is explicitly deleted first.
- **SRS Trace:** §1.2
- **Priority:** Must
- **Acceptance Criteria:** A second upload attempt to a project with an existing document returns HTTP `422 Unprocessable Entity` with message: *"This project already has an uploaded document. Delete it before uploading a new one."*

### FR-PSM-004: File Naming Convention Enforcement
- **Description:** All agent output files SHALL follow the strict naming convention: `{agent_name}_{llm_name}_{YYYYMMDD_HHMMSS}.{ext}`. The system SHALL reject and log any file save attempt that does not conform to this pattern.
- **SRS Trace:** §3, §6
- **Priority:** Must
- **Acceptance Criteria:** Files saved by agents match the regex pattern `^[a-z]+_[a-zA-Z0-9]+_\d{8}_\d{6}\.[a-z]+$`; non-conforming saves are blocked.

### FR-PSM-005: PDF Folder Write Isolation
- **Description:** The `/{project}/pdf/` directory SHALL be a write-restricted zone. Only the `PdfReportService` class SHALL have write access. All other agents and services SHALL have read-only access to this directory.
- **SRS Trace:** §6
- **Priority:** Must
- **Acceptance Criteria:** Agent processes attempting to write to `pdf/` receive a `PermissionError`; only `PdfReportService` writes succeed.

### FR-PSM-006: Workflow-Specific Parallel Directory Structure
- **Description:** For Workflow 2 and 3, the system SHALL dynamically create parallel sub-directories (`llm_alpha/`, `llm_beta/`, `llm_gamma/`, `mcp_aggregator/`) within the relevant agent output folders (`raa_output/`, `aga_output/`, `sa_output/`) based on the selected workflow configuration.
- **SRS Trace:** §4.2, §4.3
- **Priority:** Must
- **Acceptance Criteria:** After workflow selection, the correct subdirectory structure exists for the selected workflow type.

### FR-PSM-007: Disk Quota Warning (Soft Limit — 80%)
- **Description:** A Celery Beat background task (`check_project_quotas`) SHALL run every 10 minutes, scanning all project folders. When a project exceeds 80% of its 500MB quota (≥400MB used), the system SHALL:
  1. Execute Level 1 Cleanup: Purge the `arlo_cache/` directory entirely.
  2. If still above 80%, set `project_status.warning = True` so the next UI poll receives a warning modal.
- **SRS Trace:** §6.1
- **Priority:** Must
- **Acceptance Criteria:** A project at 410MB triggers `arlo_cache/` purge; if still over threshold, the UI displays: *"Project '{name}' is approaching its disk quota ({X}% used). Ephemeral caches have been cleaned."*

### FR-PSM-008: Disk Quota Hard Limit (100%)
- **Description:** When a project exceeds 100% of its 500MB quota, the system SHALL:
  1. Execute Level 1 Cleanup (purge `arlo_cache/`).
  2. Execute Level 2 Cleanup (rotate `agent_states/` to keep only the absolute last snapshot).
  3. If still over 100%, set `project_status.locked = True` to prevent further writes.
- **SRS Trace:** §6.1
- **Priority:** Must
- **Acceptance Criteria:** A project at 510MB triggers both cleanup levels; if still over budget, the project is locked and further write operations return HTTP `507 Insufficient Storage`.

### FR-PSM-009: Write Endpoint Quota Check (Middleware)
- **Description:** Critical write endpoints (file upload, "Generate" buttons acting as POST) SHALL perform a lightweight size check before processing. If `project_usage >= 500MB`, the endpoint SHALL return HTTP `507 Insufficient Storage` and the UI SHALL display a blocking "Disk Full" modal.
- **SRS Trace:** §6.1
- **Priority:** Must
- **Acceptance Criteria:** A POST to a "Generate" endpoint for a full project returns `507` with message directing user to delete old files.

### FR-PSM-010: History Retention with 5-Version Rotation
- **Description:** The system SHALL retain a maximum of 5 output versions per agent output context (per sub-folder in parallel workflows). When a 6th output is generated, the oldest file (by modification time) within that specific directory SHALL be deleted before the new file is saved.
- **SRS Trace:** §5
- **Priority:** Must
- **Acceptance Criteria:** After generating 6 outputs for `aga_output/llm_alpha/`, only the 5 most recent files remain; the oldest has been deleted.

### FR-PSM-011: Strict Backend Synchronization (F5 Recovery)
- **Description:** On UI initialization or browser refresh, the frontend SHALL query `GET /api/projects/{id}/status`. If the backend reports `status="RUNNING"` with an active `task_id`, the UI SHALL automatically re-mount the Pipeline Progress Overlay and resume listening to the Celery task. The UI SHALL NOT reset to default inputs.
- **SRS Trace:** §5, §1.1
- **Priority:** Must
- **Acceptance Criteria:** After pressing F5 during an active pipeline run, the UI immediately shows the Progress Overlay with the correct percentage, ETA, and current phase.

### FR-PSM-012: Concurrency Control via Redis Locking
- **Description:** The system SHALL implement Redis-based distributed locking scoped to `project_id`. Lock key: `lock:project:{uuid}`. When a user triggers a pipeline run, the system acquires the lock. If the lock already exists (another tab/session), the backend SHALL deny the request with HTTP `423 Locked` and message: *"Project is currently processing a pipeline step in another session."*
- **SRS Trace:** §1.1, §6
- **Priority:** Must
- **Acceptance Criteria:** Triggering a second pipeline run on the same project from a different browser tab returns `423 Locked` within 100ms.

### FR-PSM-013: Strict Checkpointing on Page Navigation
- **Description:** When the user navigates from an active pipeline step to the Projects page, the system SHALL trigger a Strict Checkpoint: unsaved ephemeral state (in-progress edits, uncommitted text area content) is discarded; only completed artifacts (saved outputs, finalized files) are persisted. A confirmation dialog SHALL be displayed: *"You have unsaved work on this step. Returning to Projects will discard unsaved changes. Continue?"*
- **SRS Trace:** §1.1
- **Priority:** Must
- **Acceptance Criteria:** User edits in a text area that have not been "Saved" are lost after navigating to Projects and confirming the dialog; saved artifacts remain on disk.

### FR-PSM-014: TOON/JSON Schema Handoff Validation
- **Description:** All TOON/JSON writes between agents SHALL pass a schema validator that enforces the presence of `arlo_reference` and `Requirement ID` metadata fields at every aggregation step. Missing fields SHALL trigger an immediate `500 Internal Server Error` (Data Integrity Violation).
- **SRS Trace:** §3
- **Priority:** Must
- **Acceptance Criteria:** Writing a TOON file without an `arlo_reference` field raises a `ValidationError` and the file is not persisted.

### FR-PSM-015: User Manual Edit Persistence (AGA Overrides)
- **Description:** When the user modifies generated `.puml` code in the code editor and clicks "Generate" or "Next," the frontend SHALL POST the modified content to `/api/projects/{id}/agents/aga/manual_override`. The backend SHALL save it as `aga_manual_{timestamp}.puml` in the `mcp_aggregator/` folder and update the `primary_artifact` metadata to point to this file for downstream consumption.
- **SRS Trace:** §1.9, §5
- **Priority:** Must
- **Acceptance Criteria:** The SA receives and scores the user-modified `.puml` file (not the original LLM output) as its input.

### FR-PSM-016: Project Export API
- **Description:** The system SHALL provide an API endpoint `GET /api/projects/{id}/export` that creates a downloadable ZIP archive containing `arlo_output/` (TOON files) and `filtered_requirements/` (CSV files). Cache directories and large PDF reports SHALL be excluded.
- **SRS Trace:** §1.7
- **Priority:** Should
- **Acceptance Criteria:** The downloaded ZIP contains valid TOON and CSV files; `arlo_cache/` and `pdf/` are excluded.

### FR-PSM-017: Project Import API
- **Description:** The system SHALL provide an API endpoint `POST /api/projects/import` that accepts a ZIP archive, validates its internal structure, creates a new project with a fresh UUID, and extracts files to the correct mapped directories.
- **SRS Trace:** §1.7
- **Priority:** Should
- **Acceptance Criteria:** Importing a valid ZIP creates a new project with correctly structured directories and files.

---

## 2. Non-Functional Requirements (NFR)

### NFR-PSM-001: Quota Check Performance
- **Description:** The lightweight quota check on write endpoints SHALL complete within 50ms to avoid noticeable latency in user interactions.
- **SRS Trace:** §6.1
- **Metric:** P95 quota check execution time ≤ 50ms.

### NFR-PSM-002: Lock Acquisition Latency
- **Description:** Redis lock acquisition and release operations SHALL complete within 10ms under normal conditions.
- **SRS Trace:** §6
- **Metric:** P99 Redis lock round-trip time ≤ 10ms.

### NFR-PSM-003: Lock Safety TTL
- **Description:** The project lock key `lock:project:{uuid}` SHALL have a hard expiry TTL of 2 hours to prevent permanent project lockout in the event of a worker crash or OOM kill.
- **SRS Trace:** §6
- **Metric:** After a simulated worker crash, the lock auto-expires within 2 hours ± 1 second.

### NFR-PSM-004: Background Quota Scan Efficiency
- **Description:** The Celery Beat `check_project_quotas` task SHALL complete a full scan of all project folders within 30 seconds for up to 50 concurrent projects.
- **SRS Trace:** §6.1
- **Metric:** Quota scan for 50 projects with ~400MB each completes within 30 seconds.

### NFR-PSM-005: Data Integrity on Concurrent Access
- **Description:** The file rotation algorithm SHALL use file-system-level atomic operations (rename-in-place or write-to-temp-then-rename) to prevent data corruption during concurrent read/write operations by multiple agents.
- **SRS Trace:** §5, §6
- **Metric:** Zero file corruption events under simulated concurrent agent writes (100 iterations).

---

## 3. Interface Requirements (IR)

### IR-PSM-001: Project Status API
- **Endpoint:** `GET /api/projects/{id}/status`
- **Response Schema:**
  ```json
  {
    "status": "RUNNING" | "IDLE" | "COMPLETED" | "FAILED",
    "current_step": "RAA" | "AGA" | "SA" | "ARLO" | null,
    "task_id": "celery-uuid-123" | null,
    "locked": true | false,
    "quota_warning": true | false,
    "quota_percent": 85
  }
  ```

### IR-PSM-002: Active Versions API (History Drawer Support)
- **Endpoint:** `GET /api/projects/{id}/active_versions/{agent_name}`
- **Purpose:** Returns user-selected version overrides set via the History Drawer for the MCP Aggregator's input selection.

### IR-PSM-003: Manual Override API
- **Endpoint:** `POST /api/projects/{id}/agents/aga/manual_override`
- **Purpose:** Persists user-edited `.puml` code as the primary artifact for downstream scoring.

### IR-PSM-004: Export/Import APIs
- **Export:** `GET /api/projects/{id}/export` → ZIP download
- **Import:** `POST /api/projects/import` → New project creation from ZIP

---

## 4. Disaster Recovery Requirements (DR)

### DR-PSM-001: Disk Full Recovery
- **Failure Mode:** Project exceeds 500MB hard quota.
- **Recovery Action:** Automatic Level 1 + Level 2 cleanup is executed. If still over budget, the project is locked and user must manually delete files.
- **User-Facing Message:** 🛑 *"Project '{name}' has exceeded its disk quota. Please delete old runs or files to continue."*
- **SRS Trace:** §6.1

### DR-PSM-002: Stale Lock Recovery
- **Failure Mode:** Celery worker crashes during pipeline execution, leaving the Redis lock behind.
- **Recovery Action:** The lock auto-expires after 2 hours (TTL). A manual "Force Unlock" admin endpoint may also be provided for emergencies.
- **SRS Trace:** §6, §13

### DR-PSM-003: Data Corruption Recovery
- **Failure Mode:** File system corruption or incomplete write during agent output save.
- **Recovery Action:** The system maintains the previous version of the file until the new write is fully committed (atomic rename). If corruption is detected via checksum mismatch, the system reverts to the previous version and logs the incident.
- **SRS Trace:** §5, §6

---

*End of Project State Management Requirements Document*
