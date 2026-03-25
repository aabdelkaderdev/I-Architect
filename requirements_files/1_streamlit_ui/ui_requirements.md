# Streamlit UI — Functional & Non-Functional Requirements

> **Version:** 1.0
> **Source Plan:** `requirements_planning/1_streamlit_ui/ui_requirements_plan.md`
> **SRS Reference:** I-Architect SRS v2.3
> **Date:** 2026-03-24

---

## 1. Functional Requirements (FR)

### 1.1 Global Interface Elements

#### FR-UI-001: SPA Routing via Session State
- **Description:** The application SHALL be a single Streamlit script operating as a Single Page Application. Navigation between pipeline steps SHALL be handled by rendering different "Page Containers" based on `st.session_state.current_step`. Streamlit's native Multipage App (MPA) sidebar navigation SHALL be disabled — all routing is managed internally.
- **SRS Trace:** §1.1
- **Priority:** Must
- **Acceptance Criteria:** Changing `st.session_state.current_step` from `4` to `5` renders the ARLO page content; no Streamlit sidebar navigation menu is visible.

#### FR-UI-002: Persistent Topbar Navigation
- **Description:** All pages SHALL display a persistent topbar containing:
  - **[Projects]** link → navigates to Page 1 (triggers Strict Checkpoint if leaving an active step).
  - **[LLM Config ⚙]** button → opens the LLM Configuration Dashboard as a modal overlay.
  - **[☰ History]** button → programmatically expands the native left sidebar.
  - **[⬇ Download Logs]** button → bundles and downloads structured logs as a ZIP archive.
- **SRS Trace:** §1.1
- **Priority:** Must
- **Acceptance Criteria:** All four topbar elements are visible and functional on every page (Pages 1–8).

#### FR-UI-003: History Drawer (Native Left Sidebar)
- **Description:** The history drawer SHALL be hosted inside Streamlit's native left sidebar, collapsed by default. It SHALL be available on RAA, AGA, and SA Pages only. It SHALL use native Python widgets (`st.selectbox`, `st.radio`) for version selection and adhere to the `agentname_LLMname_Timestamp` naming convention. It SHALL retain up to 5 versions per agent instance.
- **SRS Trace:** §1.1
- **Priority:** Must
- **Acceptance Criteria:** On the RAA page, clicking "☰ History" expands the sidebar showing up to 5 version entries for the current agent/LLM instance.

#### FR-UI-004: Single-Agent History Mode
- **Description:** In Workflow 1, the History Drawer SHALL display generation history for the current agent. Users can view previous outputs and mark a specific version as "Active." The system SHALL guarantee that the marked version — not necessarily the most recent — is passed as input to the downstream agent.
- **SRS Trace:** §1.1
- **Priority:** Must
- **Acceptance Criteria:** Marking Version 2 (of 4) as "Active" results in the downstream agent receiving Version 2's output, not the latest Version 4.

#### FR-UI-005: Parallel-Agent History Mode
- **Description:** In Workflows 2 & 3, the History Drawer SHALL expand to show three distinct history lists for Alpha, Beta, and Gamma LLM instances. Users can independently select the output version for each instance. These selections directly determine which files are fed into the MCP Aggregator.
- **SRS Trace:** §1.1
- **Priority:** Must
- **Acceptance Criteria:** Selecting Version 3 for Alpha and Version 5 for Beta results in the MCP Aggregator using those exact file versions as input.

#### FR-UI-006: Component Swap Concurrency Isolation
- **Description:** During pipeline execution (`st.session_state.pipeline_running == True`), the main content container SHALL be unmounted (not merely overlaid) and the entire view replaced by the Pipeline Progress Overlay component. No interactive widgets from the underlying page SHALL remain mounted.
- **SRS Trace:** §1.1
- **Priority:** Must
- **Acceptance Criteria:** During a running pipeline, no "Generate," "Next," or form submission buttons are accessible to the user; only the Progress Overlay is rendered.

#### FR-UI-007: Strict Checkpointing Confirmation Dialog
- **Description:** Leaving an active pipeline step for the Projects page SHALL trigger a confirmation dialog: *"You have unsaved work on this step. Returning to Projects will discard unsaved changes. Continue?"* Only completed artifacts are persisted; ephemeral state is discarded.
- **SRS Trace:** §1.1
- **Priority:** Must
- **Acceptance Criteria:** Navigating to Projects from Page 6 with unsaved edits shows the dialog; confirming discards unsaved state.

### 1.2 Page-Specific Logic

#### FR-UI-008: Projects Page — Project CRUD
- **Description:** Page 1 SHALL allow users to create, view, select, and delete projects. Project creation SHALL validate that the folder name is unique and non-empty. The system SHALL enforce a limit of exactly one document per project.
- **SRS Trace:** §1.2
- **Priority:** Must
- **Acceptance Criteria:** Creating a project with a duplicate name shows an error; creating a valid project generates the full directory structure.

#### FR-UI-009: Workflow Selection Page — LLM Mapping & Validation
- **Description:** Page 2 SHALL allow users to select from three workflows and toggle ARLO engagement. The LLM-to-agent mapping SHALL enforce:
  - Workflow 1: Exactly 1 LLM per agent.
  - Workflow 2: Exactly 3 distinct LLMs for RAA; 1 each for others.
  - Workflow 3: Exactly 3 distinct LLMs for RAA, AGA, SA each; 1 each for Filtering and ARLO.
  - The same LLM instance SHALL NOT be assigned twice within the same parallel group.
- **SRS Trace:** §1.4
- **Priority:** Must
- **Acceptance Criteria:** Assigning "GPT-4" twice to the RAA parallel group shows: *"'GPT-4' is already assigned to this parallel group."*

#### FR-UI-010: Workflow 3 Progressive Expanders
- **Description:** When Workflow 3 is selected, LLM-to-agent mapping controls SHALL be organized into collapsed `st.expander` groups: "Analysis Agents" (RAA), "Generation Agents" (AGA), "Evaluation Agents" (SA). Filtering and ARLO SHALL remain as top-level controls.
- **SRS Trace:** §1.4
- **Priority:** Should
- **Acceptance Criteria:** Selecting Workflow 3 shows 3 collapsed expanders; Filtering/ARLO controls are visible at top level.

#### FR-UI-011: LLM Pre-flight Health Check
- **Description:** Before initiating any workflow, the system SHALL perform a connectivity and model availability check for every LLM assigned to the pipeline. If any endpoint is unreachable or the model is not found, the pipeline SHALL NOT start.
- **SRS Trace:** §1.3
- **Priority:** Must
- **Acceptance Criteria:** An unreachable LLM endpoint blocks pipeline start with: *"Pipeline blocked: LLM '{name}' at endpoint '{url}' is unreachable or model not found."*

#### FR-UI-012: Requirements Upload & Extraction Page
- **Description:** Page 3 SHALL provide a file upload zone accepting `.docx`, `.pdf`, `.xls`, `.xlsx`, and `.csv`. It SHALL include an extraction strategy selector (Line-by-Line, Regex, Grammar-Based, Hybrid) and an "Extract" button with a progress indicator. The CSV Bypass Rule SHALL silently skip extraction for schema-matching CSVs with an info banner.
- **SRS Trace:** §1.5
- **Priority:** Must
- **Acceptance Criteria:** Uploading a schema-matching CSV shows: *"CSV format detected — extraction skipped. Proceeding directly to requirement editing."*

#### FR-UI-013: Disaster Detection Auto-Correction Display
- **Description:** If extraction quality fails thresholds (Coverage < 80% or Semantic Drift), the system SHALL auto-correct on the same page by switching strategies. A full-screen modal SHALL inform the user: *"Extraction coverage was {X}%. The strategy has been automatically upgraded to {new_strategy}. Re-extraction in progress."*
- **SRS Trace:** §1.5
- **Priority:** Must
- **Acceptance Criteria:** An extraction with 65% coverage triggers strategy upgrade and displays the auto-correction modal.

#### FR-UI-014: Requirement Editing Page — Master-Detail Pattern
- **Description:** Page 4 SHALL display extracted requirements as a sortable data grid (Master View) with columns: `Requirement ID`, `Status` (kept/dropped), `Summary`. Clicking a row opens a Modal Dialog (Detail View) with full raw description, extraction metadata, and a "User Override" toggle. The grid SHALL support server-side pagination with a hard cap of 50 rows per page.
- **SRS Trace:** §1.6
- **Priority:** Must
- **Acceptance Criteria:** A dataset of 200 requirements renders 4 pages of 50 rows each; clicking a row opens the modal with full details.

#### FR-UI-015: User Override Precedence
- **Description:** When a user manually un-drops a requirement via the Detail View modal, the `user_override` column SHALL be set to `True`. ARLO SHALL respect `user_override = True` and never re-drop those rows.
- **SRS Trace:** §1.6
- **Priority:** Must
- **Acceptance Criteria:** A dropped requirement with `user_override=True` appears in ARLO's input and is never flagged for removal.

#### FR-UI-016: ARLO Page — Read-Only Report Viewer
- **Description:** Page 5 SHALL provide an optimization strategy selector (ILP/Greedy), a "Run ARLO" button, and a dedicated embedded PDF viewer (e.g., `streamlit-pdf-viewer`) for the auto-generated ARLO report (Template A). The "Next" button SHALL be disabled until ARLO completes. ARLO decisions are read-only. Iframes SHALL NOT be used.
- **SRS Trace:** §1.7
- **Priority:** Must
- **Acceptance Criteria:** After ARLO completes, the PDF report is displayed inline; the "Next" button becomes clickable.

#### FR-UI-017: ARLO Export/Import
- **Description:** The ARLO page SHALL provide Export/Import functionality for ARLO ASRs and user decisions as portable TOON files.
- **SRS Trace:** §1.7
- **Priority:** Should
- **Acceptance Criteria:** Exporting and re-importing ARLO data into a new project preserves all ASR records and decision metadata.

#### FR-UI-018: RAA Page — Framework Selection
- **Description:** Page 6 SHALL allow the user to select which Architectural Diagram Framework to use (e.g., C4 Component or UML Component) before executing the RAA.
- **SRS Trace:** §1.8
- **Priority:** Must
- **Acceptance Criteria:** Selecting "C4 Container" sets `target_framework: C4_Container` in the RAA prompt context.

#### FR-UI-019: AGA Page — Code Editor & Tabbed Parallel View
- **Description:** Page 7 SHALL provide a dedicated code editor component with syntax highlighting and line numbers (e.g., `streamlit-code-editor`). Standard `st.text_area` SHALL NOT be used. In Workflows 2/3, outputs SHALL be separated by tabs: [Alpha], [Beta], [Gamma], [Aggregated]. Manual edits in the editor are saved and rendered on "Generate."
- **SRS Trace:** §1.9
- **Priority:** Must
- **Acceptance Criteria:** The code editor displays `.puml` code with syntax highlighting; modified code is sent for rendering on "Generate."

#### FR-UI-020: AGA Page — Rendered Diagram Preview
- **Description:** After the "Generate" action, the AGA page SHALL display the SVG/PNG output returned by the PlantUML Rendering Service.
- **SRS Trace:** §1.9
- **Priority:** Must
- **Acceptance Criteria:** A valid `.puml` file generates a rendered diagram visible inline on the page.

#### FR-UI-021: SA Page — Score Display & Actions
- **Description:** Page 8 SHALL render the SA's JSON output as structured markup including: evaluation metadata, score breakdown by pillar, drawback cards (severity, category, description, affected entities), adjustments checklist, and divergence warnings (Workflow 3 only). It SHALL provide "⬇ Download Full PDF Report" (Template B) and "↺ Regenerate Diagram" buttons, and a "Notes for AGA" textarea.
- **SRS Trace:** §1.10
- **Priority:** Must
- **Acceptance Criteria:** SA output with a `recommend_regeneration: true` flag enables the "Regenerate Diagram" button; clicking it redirects to the AGA page.

#### FR-UI-022: SA Tabbed View (Workflow 3)
- **Description:** In Workflow 3, SA evaluation results SHALL be separated by tabs: [Alpha], [Beta], [Gamma], [Aggregated]. Divergence warnings (>30% score difference on any pillar) SHALL be prominently displayed.
- **SRS Trace:** §1.10
- **Priority:** Must
- **Acceptance Criteria:** A 35% divergence on "SAAM Alignment" displays a warning with the median score and outlier details.

### 1.3 Component Specifications

#### FR-UI-023: Pipeline Progress Overlay
- **Description:** The Progress Overlay SHALL display: a progress bar with percentage, an ETA indicator (rolling average of last 5 batches for ARLO; step-based for others), a current phase label, and a "Cancel Run" button. This overlay replaces the main content container entirely during pipeline execution.
- **SRS Trace:** §1.11
- **Priority:** Must
- **Acceptance Criteria:** During ARLO execution, the progress bar shows batch progress with a decreasing ETA; pressing "Cancel" gracefully stops the run.

#### FR-UI-024: Full-Screen Modal System
- **Description:** All disaster recovery messages (§13) — both warnings and blocking errors — SHALL use full-screen modals (`st.dialog`) that block user interaction until dismissed. Each modal SHALL display a severity icon, user-facing message, and recommended action. No toast notifications are used.
- **SRS Trace:** §1.11
- **Priority:** Must
- **Acceptance Criteria:** An LLM timeout triggers a full-screen warning modal; the user cannot interact with the background page until dismissing it.

#### FR-UI-025: Modal Interaction Safety
- **Description:** LLM Config and Settings modals SHALL be set to `dismissable=False` (backdrop click does not close). Users MUST explicitly click "Cancel" or "Save." Disaster Recovery modals SHALL be strictly unclosable until the underlying condition is resolved.
- **SRS Trace:** §1.11
- **Priority:** Must
- **Acceptance Criteria:** Clicking outside the LLM Config modal does not close it; a Disk Full modal cannot be closed until the user deletes files.

#### FR-UI-026: LLM Configuration Dashboard (Modal)
- **Description:** The LLM Config modal SHALL allow: entering API endpoints, selecting models, assigning LLM names, providing API keys, and adjusting temperature (0–1). Supported types: Ollama, Deepseek, Google Gemini, Groq. The preflight health check (FR-UI-011) SHALL trigger before pipeline runs.
- **SRS Trace:** §1.3
- **Priority:** Must
- **Acceptance Criteria:** Configuring an Ollama endpoint with model name saves the configuration persistently; temperature slider adjusts between 0.0 and 1.0.

#### FR-UI-027: Disk Quota Alert Display
- **Description:** When a project exceeds 80% disk quota, a full-screen modal SHALL display: *"Project '{name}' is approaching its disk quota ({X}% used). Ephemeral caches have been cleaned."*
- **SRS Trace:** §1.11
- **Priority:** Must
- **Acceptance Criteria:** A project at 85% quota triggers the alert modal upon the next UI poll.

---

## 2. Non-Functional Requirements (NFR)

### NFR-UI-001: Backend State Synchronization on Refresh
- **Description:** On browser refresh or reconnection, the UI SHALL query the backend for the current project state and automatically re-mount the correct page/overlay. If a pipeline is running, the Progress Overlay SHALL be shown immediately.
- **SRS Trace:** §1.1
- **Metric:** State recovery completes within 2 seconds of page load.

### NFR-UI-002: Data Grid Render Performance
- **Description:** The requirement editing grid SHALL render 50 rows within 500ms with no visible lag when sorting, pagination, or row clicks occur.
- **SRS Trace:** §1.6
- **Metric:** P95 grid render time ≤ 500ms for 50 rows.

### NFR-UI-003: File Upload Size Limit
- **Description:** The file upload component SHALL support files up to 256MB with a chunked upload strategy to prevent browser memory issues.
- **SRS Trace:** §1.5
- **Metric:** A 200MB PDF uploads successfully without browser hang.

### NFR-UI-004: Desktop-Only Viewport
- **Description:** The UI SHALL target desktop viewports only with a minimum width of 1024px. No mobile responsive design is required.
- **SRS Trace:** §1.1
- **Metric:** UI renders correctly at 1024px×768px and above.

### NFR-UI-005: API Key Security
- **Description:** API keys entered in the UI SHALL be masked in display, never logged to the browser console, and transmitted only to the backend via HTTPS.
- **SRS Trace:** §1.3
- **Metric:** Browser DevTools console and network tab show no plaintext API keys.

### NFR-UI-006: Caching for Performance
- **Description:** Heavy computations (re-rendering the Requirement Grid, formatting SA results) SHALL use `st.cache_data` to avoid redundant processing on reruns.
- **SRS Trace:** §1.1
- **Metric:** Switching tabs and returning to the same page does not re-fetch data already in cache.

### NFR-UI-007: Input Sanitization
- **Description:** Project name fields SHALL sanitize input to prevent injection triggers (SQL, XSS, path traversal). Only alphanumeric characters, hyphens, and underscores shall be accepted.
- **SRS Trace:** §1.2
- **Metric:** Input `"../../../etc/passwd"` is rejected with a validation error.

---

## 3. Interface Requirements (IR)

### IR-UI-001: UI → Backend Communication
- **Protocol:** HTTP REST (Request-Response)
- **Target:** Django API Gateway at `http://orchestrator:8000`
- **Key Endpoints Consumed:**
  | Method | Endpoint | Purpose |
  |:--|:--|:--|
  | `GET` | `/api/projects/{id}/status` | State sync on page load |
  | `POST` | `/api/run/{workflow_type}/` | Pipeline dispatch |
  | `GET` | `/api/tasks/{task_id}/progress/` | SSE progress stream |
  | `POST` | `/api/cancel/{task_id}/` | Pipeline cancellation |
  | `POST` | `/api/projects/{id}/agents/aga/manual_override` | User edit persistence |

### IR-UI-002: Docker Configuration
- **Container:** `streamlit-ui`
- **Port:** `8501`
- **Network:** `i-architect-net` (bridge)
- **Memory Limit:** 512MB

---

## 4. Disaster Recovery Requirements (DR)

### DR-UI-001: Backend Unreachable
- **Failure Mode:** Streamlit cannot connect to the Django backend.
- **Recovery Action:** Display a full-screen modal: *"Cannot connect to the backend service. Please ensure all Docker containers are running."* Retry connection every 10 seconds.
- **SRS Trace:** §13

### DR-UI-002: Browser Session Loss
- **Failure Mode:** User closes browser tab during pipeline execution.
- **Recovery Action:** Backend continues execution independently. On re-open, the UI state recovery mechanism (FR-UI-001 + NFR-UI-001) restores the correct state.
- **SRS Trace:** §1.1

---

*End of Streamlit UI Requirements Document*
