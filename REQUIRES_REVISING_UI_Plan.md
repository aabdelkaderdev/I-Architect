# I-Architect UI Layer — Specification

## 0) Goal of this Portion

Define the **visual layer** of the I-Architect pipeline application: window structure, navigation architecture, per-view widget specifications, signal/slot contracts with the orchestrator, and error dialog specifications. The UI layer renders data, captures user input, and emits signals — it never invokes LangGraph, instantiates LLM objects, or computes scores.

> **Pipeline position note:** The UI is the outermost shell. It wraps the orchestrator and presents the pipeline as a sequential set of views (Projects → LLM Config → Upload → Editing → ARLO → RAA → AGA → SA). PDF generation (RGA) is triggered from the SA View; it does not have a dedicated view. The full pipeline is: Ingestion → ARLO → RAA → AGA → SA → RGA → PDF file on disk.

---

## 1) Architecture Overview

**Pipeline Page Flow:**
Projects (Page 1) → LLM & Workflow Configuration (Page 2) → Requirements Upload & Extraction (Page 3) → Requirement Editing (Page 4) → ARLO (Page 5) → RAA (Page 6) → AGA (Page 7) → SA (Page 8)

**UI Stack:**

| Component | Technology | Version |
|---|---|---|
| Qt Framework | PySide6 | ≥6.7 |
| Widget Library | PySide6-Fluent-Widgets | ≥1.7 |
| License | GPLv3 (non-commercial); commercial license required for distribution | — |

Install via `pip install PySide6 PySide6-Fluent-Widgets`. All imports use `from qfluentwidgets import ...`.

> **Conflict warning:** Do not install `PyQt-Fluent-Widgets`, `PyQt6-Fluent-Widgets`, `PySide2-Fluent-Widgets`, and `PySide6-Fluent-Widgets` simultaneously — their package names all resolve to `qfluentwidgets` and will conflict.

**Dependency Registration:**

| Package | Version | Dependency Group |
|---|---|---|
| `PySide6` | ≥6.7 | `[ui]` optional |
| `PySide6-Fluent-Widgets` | ≥1.7 | `[ui]` optional |

> **Note:** The `arlo/` codebase's `pyproject.toml` does not yet include these packages. They must be added before the UI layer is integrated.

**Theme:** QFluentWidgets ships with built-in light/dark theme support via `setTheme(Theme.DARK | Theme.LIGHT | Theme.AUTO)`. A single theme call at app startup applies globally to all `qfluentwidgets` components with no per-widget styling required.

**Component Mapping:** Every UI construct in this specification maps to a named `qfluentwidgets` class. Widget names are noted parenthetically as `(qfw: ClassName)` throughout each section.

**Desktop Application Architecture:** The application is a single-window desktop application built on PySide6. The main window uses `FluentWindow` from `qfluentwidgets`, which provides the frameless window chrome, a collapsible left navigation panel, and a title bar out of the box. Navigation between pipeline steps is managed internally by swapping sub-interface panels registered via `FluentWindow.addSubInterface()` — no external routing or web server is involved.

**Navigation Architecture:** The application uses `FluentWindow` with navigation items registered for each pipeline step. The top bar area of `FluentWindow` hosts the global action buttons. The left navigation panel of `FluentWindow` is used as the primary step navigator.

**Top Navigation Bar:** All views share the `FluentWindow` title bar and top action area, which contains:

- **[Projects]** navigation item — registered in `FluentWindow`'s navigation panel. Navigating to it from an active pipeline step triggers a Strict Checkpoint (see §15).
- **[LLM Config]** button `(qfw: TransparentToolButton + FluentIcon)` — opens the LLM Configuration Dashboard as a modal dialog (see §7), preserving the background view.
- **[Download Logs]** button `(qfw: TransparentToolButton + FluentIcon.DOWNLOAD)` — bundles and downloads the latest structured logs from all services.

**Concurrency Isolation (View Swapping):** The system must enforce a single active pipeline execution at a time. When the pipeline is running, the current sub-interface panel is replaced by the Pipeline Progress Overlay widget (see §15.3). This is a programmatic `QStackedWidget` swap — no interactive widgets from the underlying view remain accessible.

> **Rationale:** On a locally hosted machine with limited RAM/CPU, parallel ARLO ILP solvers and parallel RAA instances risk OOM kills. Swapping the entire panel guarantees the UI is in a clean, non-interactive state and prevents competing pipeline triggers.

**State Persistence (Strict Checkpointing):** Leaving an active pipeline step for the Projects view triggers a Strict Checkpoint. Unsaved ephemeral state is discarded; only completed artifacts are persisted. The system must display a confirmation dialog `(qfw: MessageBox)` before discarding:

> *"You have unsaved work on this step. Returning to Projects will discard unsaved changes. Continue?"*

---

## 2) Authoritative Source Register

**Purpose:** Ensure all widget usage, signal/slot wiring, and dialog construction is anchored to authoritative QFluentWidgets and PySide6 sources, with explicit normative constraints rather than ad-hoc widget selection.

### 2A — Source Register Table

| Source | URL | Retrieval Date | Governs |
|--------|-----|----------------|---------|
| QFluentWidgets Repository | https://github.com/zhiyiYo/PyQt-Fluent-Widgets | (set on retrieval) | Widget API, component gallery, theme system |
| QFluentWidgets Documentation | https://qfluentwidgets.com | (set on retrieval) | Class reference, signal signatures, styling |
| PySide6 Qt Documentation | https://doc.qt.io/qtforpython-6 | (set on retrieval) | Core Qt classes, signal/slot mechanism, QThread |
| FluentIcon Enum Reference | QFluentWidgets source: `qfluentwidgets/common/icon.py` | (set on retrieval) | Available icon constants |

### 2B — Normative Widget Constraints

- All interactive widgets must use named `qfluentwidgets` classes, not bare `QWidget` subclasses.
- Every sub-interface widget must call `setObjectName("unique_name")` before `FluentWindow.addSubInterface()`.
- All cross-thread communication must use Qt signals and slots — never direct method calls from worker threads to UI widgets.
- Dialog construction must subclass `MessageBoxBase`; custom content is added to `self.viewLayout`.
- Theme switching must use the global `setTheme()` call — no per-widget stylesheets.

### 2C — Retrieval Policy

- Each widget class is referenced by its `qfluentwidgets` name with a `(qfw: ClassName)` annotation in this specification.
- Full widget API documentation is consulted at implementation time via the registered sources.
- The Source Register is the runtime-ready extraction; direction of authority is **Source Register → This Specification → Implementation**.

---

## 3) Widget Toolkit Constraints

Hard rules governing all widget usage across every view. These consolidate the implementation notes previously scattered across view sections.

1. **InfoBar signatures:** All `InfoBar` classmethods (`info`, `warning`, `success`, `error`) require `title: str` and `content: str` as the first two arguments. `parent` must reference the current view widget. Default `duration=1000` ms; use `duration=-1` for persistent bars.

2. **Slider integer scaling:** `Slider` inherits `QSlider` (integer-only). For Temperature 0.0–1.0 with step 0.05, map internally to range 0–100 with step 5. Scale by ÷100 on read, ×100 on write.

3. **ProgressBar API:** Use `ProgressBar.setVal(v: float)` for animated progress updates — not `setValue()`. The `val` property provides the current value.

4. **Sub-Interface registration:** Every sub-interface widget must call `setObjectName("unique_name")` before `FluentWindow.addSubInterface()`. Failure to set the object name will cause navigation errors.

5. **Custom dialogs:** Subclass `MessageBoxBase`. Add custom widgets to `self.viewLayout` (a `QVBoxLayout`). The base class provides `self.yesButton`, `self.cancelButton`, and `self.buttonLayout` automatically. Override `validate() → bool` to gate the OK action.

6. **SwitchButton signals:** Use `SwitchButton.checkedChanged` signal. State via `isChecked()` / `setChecked(bool)`.

7. **ImageLabel sizing:** `ImageLabel` does not auto-fit to its container. Override the parent widget's `resizeEvent` to call `ImageLabel.scaledToWidth(available_width)` or use `QSizePolicy` constraints. Available scaling methods: `scaledToWidth(width)`, `scaledToHeight(height)`, `setScaledSize(QSize)`.

8. **Error and warning display:** All `[WARNING]` and `[STOP]` messages are exclusively modal-based (`MessageBox`), not transient `InfoBar` notifications. `InfoBar` is reserved for success and informational confirmations only (§3 rule 1 notwithstanding — `InfoBar.error` and `InfoBar.warning` are not used for pipeline errors; see §17).

---

## 4) Orchestrator Boundary & Data Contract

This document defines the **UI layer** — visual rendering, widget state, and user interaction. The **Orchestrator** (`Orchestrator_Spec.md`) owns pipeline execution, LLM management, file/project management, timing, progress estimation, checkpoints, pre-flight checks, and state threading between subgraphs.

**Communication is via Qt signals and slots only.** The UI emits signals when the user acts; the orchestrator connects slots and emits signals back with results. The UI never invokes LangGraph, never instantiates LLM objects, never reads/writes checkpoint databases, never calculates scores or ETA.

> **Boundary enforcement:** Where earlier versions of this document described orchestrator logic (LLM instantiation, pipeline invocation, checkpoint management, progress calculation, pre-flight checks), those descriptions have been removed. The UI persists configuration only and signals intent. The orchestrator owns execution.

### 4A — Data Display Contract

The UI renders data it receives from orchestrator signals. It does **not** traverse `arch_model`, compute traceability matrices, or inspect checkpoint state.

| View | Data Source (from orchestrator signal payload) |
|------|----------------------------------------------|
| Requirement Editing (§10) | `filter_report` entries with `FilteredRequirement` metadata, received via `extraction_complete` |
| ARLO Results (§11) | `asrs` list, `quality_weights` dict, concerns with decision counts, received via `arlo_complete` |
| RAA Results (§12) | Model stats (system/container/component counts), open questions list, received via `raa_complete` |
| AGA Gallery (§13) | `completed_diagrams` (PNG bytes + metadata), `failed_diagrams`, `session_report`, received via `aga_complete` |
| SA Results (§14) | Full `SARReport` structure: summary, axis scores, gap analysis, executive summary, feedback summary, adjustment log, received via `sa_complete` |

---

## 5) General Requirements

**Single-Window Desktop Application:** The application is a single-window desktop application. The main window uses `FluentWindow` from `qfluentwidgets`. Navigation between pipeline steps is managed internally by swapping sub-interface panels — no external routing or web server is involved.

**Concurrency Isolation:** The system must enforce a single active pipeline execution at a time. When the pipeline is running, the current sub-interface panel is replaced by the Pipeline Progress Overlay widget (see §15.3). This is a programmatic `QStackedWidget` swap — no interactive widgets from the underlying view remain accessible.

> **Rationale:** On a locally hosted machine with limited RAM/CPU, parallel ARLO ILP solvers and parallel RAA instances risk OOM kills. Swapping the entire panel guarantees the UI is in a clean, non-interactive state and prevents competing pipeline triggers.

**State Persistence (Strict Checkpointing):** Leaving an active pipeline step for the Projects view triggers a Strict Checkpoint. Unsaved ephemeral state is discarded; only completed artifacts are persisted. The system must display a confirmation dialog `(qfw: MessageBox)` before discarding:

> *"You have unsaved work on this step. Returning to Projects will discard unsaved changes. Continue?"*

**Deterministic vs Signal-Driven Behaviour:**

| Category | Examples | Mechanism |
|---|---|---|
| Deterministic | Widget visibility toggles, field validation, button enable/disable, ComboBox population | Local widget state, no signal emit |
| Signal-Driven | Pipeline start, extraction, agent runs, file export, model fetch | Qt signal emitted → orchestrator handler → response signal received |

Deterministic behaviour is computed synchronously in the UI thread. Signal-driven behaviour is always asynchronous — the UI emits, then awaits a response signal.

---

## 6) Projects View

### Pipeline Position

Page 1 (entry point). Registered as a sub-interface in `FluentWindow`.

### Purpose

Create, select, and manage projects. Each project is an isolated folder on disk. This is the launch point for all pipeline work.

### Layout Specification

| Area | Widget | Behaviour |
|---|---|---|
| Project list | `(qfw: SingleDirectionScrollArea)` containing `(qfw: ElevatedCardWidget)` per project | Each card shows project name, creation date, status chip. Click emits `project_selected`. |
| Create button | `(qfw: PrimaryPushButton)` labelled "New Project" | Opens creation dialog |
| Creation dialog | `(qfw: MessageBoxBase subclass)` with `(qfw: LineEdit)` for folder name | Validates uniqueness; inline `(qfw: CaptionLabel)` in warning colour on duplicate |

### Signal Contract

| Direction | Signal | Payload | Trigger |
|---|---|---|---|
| UI → Orch | `project_create_requested` | `{name: str}` | "New Project" button confirm |
| UI → Orch | `project_selected` | `{project_id: str}` | Project card click |
| Orch → UI | `project_created` | `{project_id, name, path}` | Add card to list |
| Orch → UI | `project_list_loaded` | `{projects: list[dict]}` | Populate card list on startup |

### Constraints & Rules

- Each project is allocated its own unique folder on disk.
- The system must verify the requested folder name is unique before creation.
- Exactly one document may be uploaded per project.

---

## 7) LLM Configuration Dashboard

### Pipeline Position

Global settings modal — not a sequential pipeline step. Accessible from the **[LLM Config]** top bar button at any time. Opens as a `(qfw: MessageBoxBase subclass)` dialog, preserving the background view.

### Purpose

Create, edit, delete, and test named LLM instances stored in a global, project-agnostic registry. All pipeline agent assignments (§8) draw from this registry.

### Layout Specification

| Area | Widget | Behaviour |
|---|---|---|
| Instance list | `(qfw: TableWidget)` with columns: Instance Name, Provider, Model Name, Base URL, Temperature, Status | Rows selectable for edit/delete. Status column shows connectivity badge. |
| Creation panel | `(qfw: ExpandGroupSettingCard, icon=FluentIcon.ADD)` containing the fields below | Expands inline within the dialog |
| Delete button | `(qfw: TransparentToolButton + FluentIcon.DELETE)` per row | Emits `llm_instance_deleted`; warns if instance is assigned to agents |
| Fetch Models | `(qfw: PushButton)` next to Model Name ComboBox | Emits `llm_fetch_models_requested` |
| Check Connectivity | `(qfw: PushButton)` | Emits `llm_check_connectivity_requested` |

### Configuration Fields

| Field | Widget Type | Required | Constraint |
|---|---|---|---|
| Instance Name | `(qfw: LineEdit)` | Yes | Must be unique across all instances; user-defined label (e.g., "Fast DeepSeek") |
| Provider | `(qfw: ComboBox)` — OpenRouter, ChatGPT, Anthropic, DeepSeek, Ollama | Yes | — |
| Model Name | `(qfw: ComboBox)` — editable | Yes | Actual model identifier passed to provider API; distinct from Instance Name |
| API Key | `(qfw: PasswordLineEdit)` | Yes (no for Ollama) | Field greyed out when Ollama selected |
| Base URL | `(qfw: LineEdit)` | No | Overrides provider default |
| Temperature | `(qfw: Slider)` range 0.0–1.0 + `(qfw: DoubleSpinBox)` | Yes | Internal range 0–100, step 5; displayed ÷100 |

> **Model Name ComboBox:** Remains editable — users can type a model name directly without fetching. This supports models not yet listed by the provider API or custom fine-tuned deployments.

### Model List Retrieval

The **[Fetch Models]** button emits `llm_fetch_models_requested`. The orchestrator executes the HTTP request and emits `llm_models_fetched` with the model list. Supported endpoints:

| Provider | Endpoint | Auth Header |
|---|---|---|
| OpenRouter | `{base_url}/models` | `Authorization: Bearer {api_key}` |
| ChatGPT | `{base_url}/models` | `Authorization: Bearer {api_key}` |
| Anthropic | `{base_url}/models` | `x-api-key: {api_key}` |
| DeepSeek | `{base_url}/models` | `Authorization: Bearer {api_key}` |
| Ollama | `{base_url}/api/tags` | None |

> **Note:** Provider-to-LangChain mapping and LLM instantiation are handled by the orchestrator (`Orchestrator_Spec.md` §3). The UI persists instance configuration only. The orchestrator resolves instance names to LangChain `ChatModel` objects at runtime.

### Instance Name Uniqueness

If the user attempts to save an instance with a name already in use, an inline `(qfw: CaptionLabel)` in error colour is shown:

> *"An LLM instance named '{name}' already exists. Please choose a unique name."*

### Deleting Instances

Deleting an instance assigned to an agent in any project triggers a `(qfw: MessageBox)` confirmation:

> *"'{name}' is assigned to one or more pipeline agents. Removing it will clear those assignments. Continue?"*

### Pre-flight Health Check

The orchestrator performs connectivity checks for every LLM instance assigned to the current pipeline before any pipeline run. If any instance fails, the pipeline is blocked. Error handling per §17, row 12.

Each instance row in the `TableWidget` displays a connectivity status badge: **Reachable** `(qfw: InfoBadge.success)` or **Unreachable** `(qfw: InfoBadge.error)`. Badges are automatically refreshed on every pipeline start attempt.

### Signal Contract

| Direction | Signal | Payload | Trigger |
|---|---|---|---|
| UI → Orch | `llm_instance_saved` | `{instance_config: dict}` | Save button |
| UI → Orch | `llm_instance_deleted` | `{instance_name: str}` | Delete button |
| UI → Orch | `llm_fetch_models_requested` | `{provider, api_key, base_url}` | "Fetch Models" button |
| UI → Orch | `llm_check_connectivity_requested` | `{}` | "Check Connectivity" button |
| Orch → UI | `llm_models_fetched` | `{models: list[str]}` | Populate Model Name ComboBox |
| Orch → UI | `llm_connectivity_result` | `{instance_name: str, reachable: bool}` | Update status badge per row |

---

## 8) LLM & Workflow Assignment View

### Pipeline Position

Page 2. Registered as a sub-interface in `FluentWindow`.

### Purpose

Assign LLM instances (from the global registry, §7) to pipeline agents. All selectable instances are drawn from the registry configured in §7.

### Layout Specification

| Area | Widget | Behaviour |
|---|---|---|
| RFA + ARLO card | `(qfw: CardWidget)` containing 2 `(qfw: ComboBox)` rows | Requirement Filtering and ARLO assignment at top |
| RAA Configuration card | `(qfw: HeaderCardWidget)` labelled "RAA Configuration" with 4 `(qfw: ComboBox)` rows | RAA-A, RAA-B, RAA-C subgraph selectors + Judge selector |
| AGA + SA card | `(qfw: CardWidget)` containing 2 `(qfw: ComboBox)` rows | AGA and SA assignment below RAA |

### Assignment Rules

| Agent | Widget | Requirement |
|---|---|---|
| Requirement Filtering (RFA) | `(qfw: ComboBox)` | Exactly 1 LLM instance |
| ARLO | `(qfw: ComboBox)` | Exactly 1 LLM instance |
| RAA-A (SAAM-first) | `(qfw: ComboBox)` | Exactly 1 LLM instance |
| RAA-B (Pattern-driven) | `(qfw: ComboBox)` | Exactly 1 LLM instance |
| RAA-C (Entity-driven) | `(qfw: ComboBox)` | Exactly 1 LLM instance |
| RAA Judge | `(qfw: ComboBox)` | Exactly 1 LLM instance |
| AGA | `(qfw: ComboBox)` | Exactly 1 LLM instance |
| SA | `(qfw: ComboBox)` | Exactly 1 LLM instance |

> **RAA LLM Assignment:** RAA requires 4 LLM instances — one per parallel strategy subgraph and one for the Judge node. No uniqueness constraint is enforced; the user may assign the same LLM instance to all four slots or use different models.

### Signal Contract

| Direction | Signal | Payload | Trigger |
|---|---|---|---|
| UI → Orch | (part of pipeline start config) | Per-agent instance name selections | Collected with pipeline start; not a standalone signal |

ComboBox selections are saved per-project and emitted to the orchestrator as part of the pipeline start configuration. The orchestrator (`Orchestrator_Spec.md` §3C) resolves instance names to LangChain `ChatModel` objects and passes them to subgraphs via `context={}`.

---

## 9) Requirements Upload & Extraction View

### Pipeline Position

Page 3. Registered as a sub-interface in `FluentWindow`.

### Purpose

Upload a requirements document, configure filtering parameters, and trigger extraction. One document per project (enforced by §6).

### Layout Specification

| Area | Widget | Behaviour |
|---|---|---|
| File selector | `(qfw: PushButton + FluentIcon.DOCUMENT)` labelled "Select File" + read-only `(qfw: LineEdit)` | Opens native `QFileDialog` filtered to `.pdf`, `.docx`, `.txt`, `.json`. Displays selected filename. |
| Batch Size | `(qfw: SpinBox)` | Default 20, minimum 1 |
| Confidence Threshold | `(qfw: DoubleSpinBox)` range 0.00–1.00, step 0.05 | Default 0.70 |
| Filtering Toggle | `(qfw: SwitchButton)` labelled "Enable Requirement Filtering" | Default ON. When OFF, filtering agent skipped. Greys out Batch Size and Confidence Threshold. |
| Filter JSON Inputs | `(qfw: SwitchButton)` labelled "Filter JSON Inputs" | Default OFF. Visible only when `.json` file selected. |
| Extract button | `(qfw: PrimaryPushButton)` labelled "Extract" | Emits `extraction_requested` |

### Configuration Fields

| Field | Widget Type | Default | Constraint |
|---|---|---|---|
| Batch Size | `(qfw: SpinBox)` | 20 | Min 1 |
| Confidence Threshold | `(qfw: DoubleSpinBox)` | 0.70 | Range 0.00–1.00, step 0.05 |
| Enable Filtering | `(qfw: SwitchButton)` | ON | When OFF, skips RFA entirely |
| Filter JSON Inputs | `(qfw: SwitchButton)` | OFF | Visible only for `.json` files |

### JSON Passthrough Rule

The orchestrator detects compliant JSON and may bypass extraction. On bypass, the UI shows an info banner `(qfw: InfoBar.info())`:

> *"Compliant JSON detected — extraction skipped. Proceeding directly to requirement editing."*

> **Note:** FilterConfig assembly, extraction pipeline invocation, and JSON passthrough logic are handled by the orchestrator (`Orchestrator_Spec.md` §4B). The UI only collects configuration and emits the signal.

### Signal Contract

| Direction | Signal | Payload | Trigger |
|---|---|---|---|
| UI → Orch | `file_uploaded` | `{file_path: str}` | File dialog selection |
| UI → Orch | `extraction_requested` | `{filter_config: dict}` | "Extract" button |
| Orch → UI | `extraction_progress` | `{stage: str, batch: int, total: int, eta_seconds: float}` | Update ProgressBar + label |
| Orch → UI | `extraction_complete` | `{filter_report: dict, requirements: dict}` | Populate Requirement Editing table |

### Error Handling

Error handling per §17, rows 1–5.

---

## 10) Requirement Editing View

### Pipeline Position

Page 4. Registered as a sub-interface in `FluentWindow`.

### Purpose

Review, reclassify, and finalise requirements before they proceed to ARLO. The master-detail pattern enables inspection of individual requirement metadata with user override capability.

### Layout Specification

| Area | Widget | Behaviour |
|---|---|---|
| Master grid | `(qfw: TableWidget)` with columns: Requirement ID, Status, Summary | Column sorting via header click. Row colour: green (SIGNAL/kept), red (NOISE/dropped), amber (user-overridden). Rows clickable. |
| Detail dialog | `(qfw: MessageBoxBase subclass)` | Opens on row click. Contains fields below. |
| Bulk toolbar | Row of `(qfw: PushButton)` above TableWidget | "Restore All Dropped", "Drop Selected", "Keep Selected" |

### Detail View Fields

| Field | Widget | Content |
|---|---|---|
| Raw Description | `(qfw: TextEdit)` read-only | Full requirement text |
| Classification | `(qfw: InfoBadge.success)` — SIGNAL or `(qfw: InfoBadge.error)` — NOISE | RFA classification |
| Confidence | `(qfw: CaptionLabel)` | RFA confidence score 0.00–1.00 |
| Reason | `(qfw: CaptionLabel)` | RFA one-sentence justification |
| Source Page | `(qfw: CaptionLabel)` | From extraction metadata; "N/A" when unavailable |
| Source Section | `(qfw: CaptionLabel)` | From extraction metadata; "N/A" when unavailable |
| User Override | `(qfw: SwitchButton)` | Toggle to override RFA classification |
| Save & Close | `(qfw: PrimaryPushButton)` | Applies changes, closes dialog |

### User Override Precedence

When a user restores a dropped requirement via the toggle, `user_override = True` is set. Strict precedence applies: `user_override > classification`. A requirement with `user_override = True` is always included in the final set passed to ARLO, regardless of its NOISE classification.

> **Architectural Note:** The ingestion plan's final output is a clean `dict[str, str]` (`extracted_requirements`). However, the Requirement Editing view needs the **intermediate** data — all requirements with `FilteredRequirement` metadata — to populate the detail view. The orchestrator provides this via the `extraction_complete` signal payload. User overrides are emitted via `requirement_overrides_submitted` before ARLO runs. The orchestrator (`Orchestrator_Spec.md` §4B) merges overrides into the final requirement set.

### Validation

If zero requirements remain in the kept state, the "Next" navigation control is programmatically disabled and an `(qfw: InfoBar.warning())` banner is shown:

> *"At least one requirement must be kept before proceeding."*

### Signal Contract

| Direction | Signal | Payload | Trigger |
|---|---|---|---|
| UI → Orch | `requirement_overrides_submitted` | `{overrides: list[{req_id, user_override}]}` | Save in detail dialog or bulk action |

### Constraints & Rules

- Bulk "Restore All Dropped" resets all user overrides to `True`.
- Bulk "Drop Selected" / "Keep Selected" operate on current `TableWidget` selection.
- Override state must be visually distinguishable (amber row tint) from original classification.

---

## 11) ARLO View

### Pipeline Position

Page 5. Registered as a sub-interface in `FluentWindow`.

### Purpose

Configure and run ARLO analysis on the finalised requirement set. Review results inline before proceeding to RAA.

> **Important:** ARLO's output decisions are read-only. The orchestrator invokes the compiled ARLO graph which runs from `START` to `END` without internal interrupts. User review occurs after the graph invoke returns — not during node execution.

### Layout Specification

| Area | Widget | Behaviour |
|---|---|---|
| Experiment Type | `(qfw: ComboBox)` — BasicArlo, InfluentialSets, VaryingRequirements | Selection collected for `arlo_run_requested` |
| Parsing Mode | `(qfw: ComboBox)` — Stringent, Lax | With `(qfw: CaptionLabel)` tooltip explaining each mode |
| Optimization Strategy | `(qfw: ComboBox)` — ILP, Greedy | — |
| Batch Size | `(qfw: SpinBox)` | Default 10, minimum 1 |
| Run button | `(qfw: PrimaryPushButton)` labelled "Run ARLO" | Emits `arlo_run_requested`. "Next" disabled until `arlo_complete`. |
| Results panel | Inline after completion | ASR list, quality weight bars, concern decisions table |

### Configuration Fields

| Field | Widget Type | Default | Options |
|---|---|---|---|
| Experiment Type | `(qfw: ComboBox)` | BasicArlo | BasicArlo, InfluentialSets, VaryingRequirements |
| Parsing Mode | `(qfw: ComboBox)` | Stringent | Stringent (both criteria), Lax (quality attributes only) |
| Optimization Strategy | `(qfw: ComboBox)` | ILP | ILP (optimal), Greedy (heuristic) |
| Batch Size | `(qfw: SpinBox)` | 10 | Min 1 |

### Parsing Mode Detail

- **Stringent** (default): A requirement is classified as an ASR only when it satisfies **both** the "architecturally-significant" criterion and describes quality attributes.
- **Lax**: A requirement is classified as an ASR when it describes quality attributes alone, without requiring the architectural-significance check.

### VaryingRequirements Configuration (Conditional)

This panel is **only visible** when Experiment Type is set to `VaryingRequirements`. When any other experiment type is selected, the panel is hidden.

| Field | Widget Type | Default | Constraint |
|---|---|---|---|
| Removal Step | `(qfw: DoubleSpinBox)` | 0.20 | Range 0.05–0.50, step 0.05 |
| Removal Strategy | `(qfw: ComboBox)` — Random, Targeted | Random | — |
| Desired QAs | `(qfw: DropDownPushButton + RoundMenu)` with checkable `Action` items | empty | Only visible when Targeted |
| Undesired QAs | `(qfw: DropDownPushButton + RoundMenu)` with checkable `Action` items | empty | Only visible when Targeted |
| Removal Seed | `(qfw: SpinBox)` | 0 | Range 0–65535; 0 = no fixed seed |

**Multi-Select Implementation:** Quality attribute multi-select uses a `DropDownPushButton` hosting a `RoundMenu` with checkable `Action` items per quality attribute. The button label updates to display the selected count. A `(qfw: CaptionLabel)` below the fields reads: *"Targeted removal prioritises ASRs tagged with Desired QAs for removal, and preserves ASRs tagged with Undesired QAs."*

- **Removal Step:** Fraction of the current ASR pool removed per round.
- **Removal Strategy:** `Random` drops ASRs uniformly. `Targeted` drops ASRs matching the configured quality attribute filters.
- **Removal Seed:** RNG seed for reproducible removal order. A value of `0` means no fixed seed.

### ARLO Results Summary

After ARLO completes, an inline results panel is displayed. No mid-pipeline PDF is generated — the RGA produces the full pipeline PDF after the final SA pass. The inline summary includes:

| Result Area | Widget | Content |
|---|---|---|
| Identified ASRs | `(qfw: CaptionLabel)` list | ASR ID and summary text per item |
| Quality Weight Distribution | `(qfw: ProgressBar)` per QA | Accumulated weight per quality attribute |
| Concern Decisions | `(qfw: TableWidget)` | Columns: Concern ID, Satisfiable Group, Decision Count, Top Decision |
| InfluentialSets results | Conditional | Influential requirement rankings (when applicable) |
| VaryingRequirements results | Conditional | Round-by-round ASR retention summary (when applicable) |

> **Note:** The full PDF report including ARLO results is generated by the RGA after SA completes. No separate "Save ARLO Report" button is provided — ARLO results are included in the final comprehensive PDF saved from the SA View (§14).

### Signal Contract

| Direction | Signal | Payload | Trigger |
|---|---|---|---|
| UI → Orch | `arlo_run_requested` | `{experiment_config: dict}` | "Run ARLO" button |
| Orch → UI | `arlo_progress` | `{batch: int, total: int, eta_seconds: float}` | Update ProgressBar |
| Orch → UI | `arlo_complete` | `{asrs, quality_weights, concerns, stats}` | Populate results summary |

---

## 12) RAA View

### Pipeline Position

Page 6. Registered as a sub-interface in `FluentWindow`.

### Purpose

Configure and trigger RAA batch processing. Monitor batch-by-batch execution with phase labels. Review the merged C4 model results after completion.

RAA is a **single LangGraph StateGraph** that internally processes sequential batches. Within each batch, three strategy subgraphs (RAA-A, RAA-B, RAA-C) run in parallel via the LangGraph **Send API**. A Judge node evaluates and merges outputs per batch. The final output is a single merged C4-compliant JSON model. The orchestrator invokes the RAA graph once; all parallelism is internal to LangGraph.

> **Implementation note:** The UI emits `raa_run_requested` with the batch ordering strategy. The orchestrator (`Orchestrator_Spec.md` §4C) invokes the RAA graph and emits `raa_progress` and `raa_complete` signals. The UI only displays progress and results.

### Layout Specification

| Area | Widget | Behaviour |
|---|---|---|
| Framework label | `(qfw: CaptionLabel)` static | *"Framework: C4 Model (Context · Container · Component)"* |
| Batch Ordering | `(qfw: ComboBox)` — Risk-First, ASR Count, Quality Weight | With `(qfw: CaptionLabel)` tooltip per option |
| Execution status | `(qfw: CardWidget)` with `(qfw: ProgressBar)`, phase label, expandable detail panel | Shows "Batch N of M", current phase, per-batch subgraph statuses |
| Run button | `(qfw: PrimaryPushButton)` labelled "Run RAA" | Emits `raa_run_requested` |
| Results summary | Read-only panel (post-execution) | Batch count, entity counts, open questions list |

### Configuration Fields

| Field | Widget Type | Default | Options |
|---|---|---|---|
| Batch Ordering Strategy | `(qfw: ComboBox)` | Risk-First | Risk-First, ASR Count, Quality Weight |

- **Risk-First:** Prioritise requirements flagged as high-risk by ARLO.
- **ASR Count:** Order by number of ASRs per requirement (descending).
- **Quality Weight:** Order by accumulated quality attribute weight (descending).

### Execution Status Panel

| Element | Widget | Content |
|---|---|---|
| Batch progress | `(qfw: ProgressBar)` | Batch N of M |
| Phase label | `(qfw: CaptionLabel)` | Cycles: Preparation → Batch Construction → Executing Batch N → Judge Evaluation → Final Merge |
| Detail panel | `(qfw: ExpandGroupSettingCard, icon=FluentIcon.INFO)` | Per-batch subgraph statuses (RAA-A, RAA-B, RAA-C) — read-only |

### RAA Results Summary (Post-Execution)

After the RAA graph completes, the status panel is replaced by a read-only results summary:

| Element | Content |
|---|---|
| Total batches | Count processed |
| Entity counts | Systems (N), Containers (N), Components (N) |
| Open questions | Count + scrollable `(qfw: CaptionLabel)` list showing question text and affected entity ID |
| Navigation | "Next" control to proceed to AGA |

### Signal Contract

| Direction | Signal | Payload | Trigger |
|---|---|---|---|
| UI → Orch | `raa_run_requested` | `{batch_ordering: str}` | "Run RAA" button |
| Orch → UI | `raa_progress` | `{batch: int, total: int, phase: str}` | Update ProgressBar + phase label |
| Orch → UI | `raa_complete` | `{model_stats: dict, open_questions: list}` | Populate results summary |

---

## 13) AGA View

### Pipeline Position

Page 7. Registered as a sub-interface in `FluentWindow`.

### Purpose

Configure and run AGA to generate architectural diagrams from the RAA C4 model. Browse rendered diagrams in a gallery with PlantUML source inspection.

AGA is a **single ReAct agent** that receives the merged C4 JSON model from RAA and autonomously generates diagrams for every entry in the `diagram_manifest`. It uses a local `planturl` binary to encode PlantUML code into server URLs, submits them to the PlantUML server for PNG rendering, and self-corrects on syntax errors via a ReAct correction loop.

### Layout Specification

| Area | Widget | Behaviour |
|---|---|---|
| Summary header | `(qfw: CardWidget)` | Render status, execution time, visible patterns |
| Diagram selector | `(qfw: ComboBox)` listing `diagram_manifest` entries by label | Selecting updates preview pane + code view |
| Preview pane | `(qfw: ImageLabel)` | Scaled to fit, preserving aspect ratio. Dimensions + render timestamp below. |
| Code view | `(qfw: ExpandGroupSettingCard, icon=FluentIcon.CODE)` with read-only `(qfw: TextEdit)` | PlantUML source for selected diagram |
| Run button | `(qfw: PrimaryPushButton)` labelled "Run AGA" | Emits `aga_run_requested` |
| Error display | `(qfw: CardWidget)` per failed diagram | Error type badge, retry count, message, last PlantUML source |

### Configuration Fields

| Field | Widget Type | Default | Constraint |
|---|---|---|---|
| Max Retries | `(qfw: SpinBox)` | 5 | Range 1–10 |
| PlantUML Server URL | `(qfw: LineEdit)` | `http://www.plantuml.com/plantuml` | Overridable for self-hosted |

### Diagram Gallery Detail

| Element | Content |
|---|---|
| Render status | *"N of M diagrams rendered successfully. K failed."* |
| Execution time | *"Completed in {wall_clock_seconds}s"* |
| Visible patterns | Comma-separated architectural pattern names (traceability from RAA) |
| Diagram selector label | *"Diagram list is determined by RAA's diagram manifest. AGA does not add or remove diagram entries."* |

> **Unverified entities:** Entities with reduced confidence (from incoherent RAA batches) appear with `[unverified]` appended to their description in the rendered diagram. A `(qfw: InfoBadge.warning)` is shown on diagrams containing at least one `[unverified]` entity.

### Failed Diagram Display

Per failed diagram:

| Field | Widget | Content |
|---|---|---|
| Diagram ID + Type | `(qfw: CaptionLabel)` | Identifier and diagram type |
| Error type | `(qfw: InfoBadge.error)` | `encoding_error`, `http_error`, or `syntax_error` |
| Retry count | `(qfw: CaptionLabel)` | *"Failed after N attempts"* |
| Error detail | `(qfw: CaptionLabel)` | `raw_message` or `svg_error_text` |
| Last source | `(qfw: TextEdit)` expandable | Final PlantUML source that caused failure |

### Output Artifacts on Disk

The orchestrator manages artifact storage at `projects/{name}/output/aga/`. AGA writes three types of artifacts:

1. **PNG files** — named `{diagram_id}.png`.
2. **Metadata sidecars** — JSON files alongside each PNG.
3. **Session report** — `aga_report.json` with full `SessionReport` fields.

These artifacts are consumed by the Scoring Agent (SA) and the Report Generation Agent (RGA). No in-app file browser is needed — this is informational for implementers. The orchestrator (`Orchestrator_Spec.md` §2C) handles output directory creation and artifact paths.

### Signal Contract

| Direction | Signal | Payload | Trigger |
|---|---|---|---|
| UI → Orch | `aga_run_requested` | `{aga_config: dict}` | "Run AGA" button |
| Orch → UI | `aga_progress` | `{diagram: int, total: int, current_label: str}` | Update ProgressBar |
| Orch → UI | `aga_complete` | `{completed: list, failed: list, session_report: dict}` | Populate diagram gallery |

### Error Handling

Error handling per §17, rows 6–7.

---

## 14) SA View

### Pipeline Position

Page 8 (final step). Registered as a sub-interface in `FluentWindow`.

### Purpose

Display the SA scoring report with full axis breakdown, gap analysis, and executive summary. Trigger targeted regeneration, RAA re-run, SA artifact export, and PDF report generation.

The SA always operates as a single instance, evaluating the AGA output.

### Layout Specification

| Area | Widget | Behaviour |
|---|---|---|
| Evaluation metadata | `(qfw: CardWidget)` | Run ID, timestamp, grade + score, summary stats |
| Score breakdown | Three `(qfw: ExpandGroupSettingCard, icon=FluentIcon.ALBUM)` per axis | Aggregate `(qfw: ProgressBar)` collapsed; sub-rubric detail expanded |
| Executive summary | `(qfw: CardWidget)` + `(qfw: ExpandGroupSettingCard, icon=FluentIcon.DOCUMENT)` | Key findings bullets; full markdown in expandable `(qfw: TextEdit)` |
| Gap analysis | Five sub-sections in `(qfw: SingleDirectionScrollArea)` | Orphaned reqs, failed diagrams, incomplete diagrams, open questions, contradictions |
| Feedback summary | `(qfw: CardWidget)` | Adjustment count, targeted diagrams, structural gaps |
| Adjustment log | `(qfw: TableWidget)` read-only | 10-column table of `AdjustmentRecord` fields |
| Recommended action | `(qfw: CardWidget)` | accept / regenerate_diagrams / rerun_raa with trigger axes |
| Advanced config | `(qfw: ExpandGroupSettingCard, icon=FluentIcon.SETTING)` | Regeneration threshold, diagram accuracy threshold |
| PDF config | `(qfw: ExpandGroupSettingCard, icon=FluentIcon.SAVE)` | 8 config fields for PDF generation |
| Action buttons | `(qfw: PrimaryPushButton)` × 3 + export button | Save PDF, Regenerate, Re-run RAA, Export SA Artifacts |

### Evaluation Metadata

| Field | Widget | Content |
|---|---|---|
| Pipeline Run ID | `(qfw: CaptionLabel)` | `pipeline_run_id` |
| Report Generated At | `(qfw: CaptionLabel)` | `generated_at` |
| SA Grade | `(qfw: TitleLabel)` | Letter grade (A/B/C/D/F) + numeric score (0–100) |
| Summary Stats | `(qfw: CaptionLabel)` | Requirements: total, ASR, functional, orphaned. Diagrams: completed of manifest, failed. |

### Score Breakdown by Axis

**Axis 1 — Functional Traceability & Coverage (max 40):**

| Sub-Rubric | Widget | Content |
|---|---|---|
| Explicit Mapping | `(qfw: ProgressBar)` + `(qfw: CaptionLabel)` | Score / 25 (N of M mapped) |
| Depth of Resolution | `(qfw: ProgressBar)` | Score / 15 |
| Orphan Penalty | `(qfw: CaptionLabel)` warning colour | Penalty (N orphaned) |
| LLM Reasoning (Depth) | `(qfw: TextEdit)` read-only | `depth_llm_reasoning` |

**Axis 2 — Quality Attribute & ASR Satisfaction (max 40):**

| Sub-Rubric | Widget | Content |
|---|---|---|
| ASR Traceability | `(qfw: ProgressBar)` + `(qfw: CaptionLabel)` | Score / 15 (N of M mapped) |
| High-Risk QA Mitigation | `(qfw: ProgressBar)` + `(qfw: CaptionLabel)` | Score / 20 (top risks listed) |
| Technology Confidence | `(qfw: ProgressBar)` | Score / 5 |
| Contradiction Penalty | `(qfw: CaptionLabel)` error colour | Visible only when non-zero |
| LLM Reasoning (Mitigation) | `(qfw: TextEdit)` read-only | `mitigation_llm_reasoning` |
| LLM Reasoning (Tech Confidence) | `(qfw: TextEdit)` read-only | `technology_confidence_llm_reasoning` |

**Axis 3 — Diagram Accuracy & Hygiene (max 20):**

| Sub-Rubric | Widget | Content |
|---|---|---|
| Per-diagram scores | `(qfw: TableWidget)` | Columns: Diagram ID, Type, Score, Render OK, Sub-tree OK, Unverified Count |

### Gap Analysis Sections

Five sub-sections, each with a count header and per-item `(qfw: ElevatedCardWidget)`:

1. **Orphaned Requirements** — req_id, is_asr badge, quality_attributes, text_snippet.
2. **Failed Diagrams** — diagram_id, diagram_type, final_error_type badge, retry_count.
3. **Incomplete Diagrams** — diagram_id, focus_entity_id, missing_entity_ids.
4. **Open Questions** — entity_id, type badge (`(qfw: InfoBadge.error)` for `hierarchy_conflict`/`scope_conflict`, `(qfw: InfoBadge.warning)` for others), description, affected_diagram_ids.
5. **Technology Contradictions** — description. Visible only when non-empty. Count header: *"N contradictions identified (−{penalty} pts)"*.

### Feedback Summary & Adjustment Log

| Element | Widget | Content |
|---|---|---|
| Feedback summary | `(qfw: CaptionLabel)` | *"Feedback: N adjustments (types), M diagrams targeted, K structural gaps"* |
| FeedbackState notes | `(qfw: InfoBar.warning())` | Shown when `FeedbackState.notes` non-null |
| Adjustment log | `(qfw: TableWidget)` read-only | 10 columns: Adjustment ID, Type, Source Axis, Target Entity, Target Diagram, Field, Before, After, Rationale, Est. Score Delta |

> **Note:** SA's Node 6 automatically applies adjustments to a deep copy of the architectural model — the adjustment log is informational, not a manual checklist.

### Recommended Action Panel

| Action | Badge | Description |
|---|---|---|
| `accept` | `(qfw: InfoBadge.success)` | *"Architecture accepted. No regeneration needed."* |
| `regenerate_diagrams` | `(qfw: InfoBadge.warning)` | *"Targeted diagram regeneration recommended."* with targeted count, "Regenerate" button, trigger axes |
| `rerun_raa` | `(qfw: InfoBadge.error)` | *"Structural gaps detected. RAA re-run recommended."* with requirement IDs, "Re-run RAA" button, trigger axes |

### Advanced Scoring Configuration

| Field | Widget Type | Default | Constraint |
|---|---|---|---|
| Regeneration Threshold | `(qfw: DoubleSpinBox)` | 80.0 | Range 0–100 |
| Diagram Accuracy Threshold | `(qfw: DoubleSpinBox)` | 14.0 | Range 0–20 |

### PDF Report Configuration

| Field | Widget Type | Default | Maps To |
|---|---|---|---|
| Page Size | `(qfw: ComboBox)` — A4, LETTER | A4 | `ReportConfig.page_size` |
| Colour Theme | `(qfw: ComboBox)` — Default, Monochrome, Dark | Default | `ReportConfig.colour_theme` |
| Include Appendices | `(qfw: SwitchButton)` | ON | `ReportConfig.include_appendices` |
| Include PlantUML Source | `(qfw: SwitchButton)` | OFF | `ReportConfig.include_plantuml_source` |
| Max Diagram Width | `(qfw: DoubleSpinBox)` range 0.50–1.00, step 0.05 | 0.85 | `ReportConfig.max_diagram_width_ratio` |
| Logo Path | `(qfw: PushButton + FluentIcon.IMAGE_EXPORT)` "Select Logo" + read-only `(qfw: LineEdit)` | empty | `ReportConfig.logo_path` |
| Custom Filename | `(qfw: LineEdit)` placeholder: `i-architect-report-{run_id}.pdf` | empty | `ReportConfig.output_filename` |
| Watermark Text | `(qfw: LineEdit)` placeholder: `"Leave empty for no watermark"` | empty | `ReportConfig.watermark_text` |

Toggle-description text for Include Appendices:
- OFF: *"Report will include 10 core sections. Appendices (Filtering Report, Open Questions, Full Requirement Listing, Pattern Rationales) will be excluded."*
- ON: *"Report will include up to 14 sections. Appendices are included when their source data is available."*

### PDF Generation Behaviour

The "Save Full PDF Report" button `(qfw: PrimaryPushButton + FluentIcon.SAVE)` opens a native `QFileDialog.getExistingDirectory()` picker, then emits `pdf_report_requested`. During generation, the button is replaced by an `(qfw: IndeterminateProgressBar)` + `(qfw: CaptionLabel)` cycling through RGA phases. The button is restored on completion or failure.

On success, an `(qfw: InfoBar.success())` banner:

> *"Full report saved to {pdf_path}. {page_count} pages, {pdf_size_bytes_formatted}, {diagrams_embedded} diagrams embedded. Generated in {generation_wall_clock_seconds}s."*

If any diagrams were omitted: append *"({diagrams_failed_omitted} failed diagrams noted but not embedded.)"*

No in-app preview is shown. The saved file is the deliverable.

> **Note:** The RGA runs once after the final SA pass. It is not invoked separately per pipeline stage. The orchestrator (`Orchestrator_Spec.md` §4A) invokes the RGA graph.

**Retry Behaviour:** If PDF generation fails, the "Save Full PDF Report" button is re-enabled after the error dialog is dismissed. Retrying emits `pdf_report_requested` again; if a checkpoint exists from a partial previous run, the RGA resumes automatically (see `PDF_Reporting.md §8D`).

**PipelineMetadata in PDF Report:** The orchestrator records per-subgraph LLM model names and wall-clock execution times during the pipeline run. These are passed to the RGA as `PipelineMetadata` and appear in the PDF report's LLM Configuration Overview and Subgraph Execution Timing sections. No UI surface is required for this data.

### Export SA Artifacts

The "Export SA Artifacts" button `(qfw: TransparentToolButton + FluentIcon.FOLDER_ADD)` opens a native `QFileDialog.getExistingDirectory()` picker and emits `sa_export_requested`. The orchestrator copies the three SA output files (`scoring_report.json`, `scoring_report.md`, `feedback_state.json`) to the selected directory.

> *"'Export SA Artifacts' exports only the three SA output files. The PDF report is generated and saved separately via the 'Save Full PDF Report' button. These are independent actions."*

### Signal Contract

| Direction | Signal | Payload | Trigger |
|---|---|---|---|
| UI → Orch | `sa_export_requested` | `{export_dir: str}` | "Export SA Artifacts" button |
| UI → Orch | `pdf_report_requested` | `{report_config: dict}` | "Save Full PDF Report" button |
| UI → Orch | `regenerate_diagrams_requested` | `{}` | "Regenerate Affected Diagrams" button |
| UI → Orch | `rerun_raa_requested` | `{}` | "Re-run RAA" button |
| Orch → UI | `sa_progress` | `{node: int, total: int, node_name: str}` | Update SA ProgressBar |
| Orch → UI | `sa_complete` | `{sa_report: dict, feedback_state: dict}` | Populate SA results |
| Orch → UI | `rga_progress` | `{phase: str}` | Update PDF generation ProgressBar + label |
| Orch → UI | `rga_complete` | `{pdf_path, page_count, size_bytes, diagrams_embedded}` | Show success InfoBar |

### Error Handling

Error handling per §17, rows 8–11.

---

## 15) Global UI Elements

### 15.1 Full-Screen Warning & Error Modal System

All disaster recovery messages (§17) use blocking `(qfw: MessageBox)` dialogs that prevent interaction until dismissed. Each dialog displays a severity icon, user-facing message, and recommended action. No transient `InfoBar` notifications are used for errors or warnings — those are reserved for success and informational confirmations only. All `[WARNING]` and `[STOP]` messages are exclusively modal-based.

### 15.2 Stage Progress Bars

Each pipeline stage that involves agent execution displays a dedicated `(qfw: ProgressBar)` within its view. Progress values are pushed in real time from orchestrator `QThread` workers via Qt signals — the UI never polls and does not estimate progress independently.

Each `ProgressBar` is accompanied by:
- A stage label `(qfw: BodyLabel)` showing current batch position (e.g., *"Filtering — Batch 3 of 12"*).
- A rolling ETA `(qfw: CaptionLabel)` — value received from orchestrator via stage progress signals. The orchestrator (`Orchestrator_Spec.md` §5C) calculates ETA from a sliding window of batch durations.

Stages with dedicated progress bars:

| View | Stage Labels |
|---|---|
| Requirements Upload & Extraction (§9) | Extraction · Normalizing · Filtering |
| ARLO (§11) | ARLO Analysis |
| RAA (§12) | RAA — Batch N of M (single `ProgressBar`) |
| AGA (§13) | Diagram Rendering — N of M |
| SA (§14) | Scoring — Node N of 6 (Data Prep · Functional · QA · Diagrams · Report · Feedback) |
| SA (§14) — PDF Generation | PDF Report — Validating · Assembling · Rendering · Writing |

### 15.3 Pipeline Progress Overlay (View Swap)

During full pipeline execution the current sub-interface panel is unmounted and replaced by the Pipeline Progress Overlay widget via a `QStackedWidget` swap. No interactive widgets from the underlying view remain rendered or accessible.

The overlay widget contains:

| Element | Widget | Content |
|---|---|---|
| Overall progress | `(qfw: ProgressBar)` | Full pipeline completion percentage |
| Per-agent progress | Individual `(qfw: ProgressBar)` per executing agent | Including batch-level RAA bar |
| Rolling ETA | `(qfw: CaptionLabel)` | Overall pipeline completion ETA |
| Current phase | `(qfw: SubtitleLabel)` | Active agent name |
| Cancel button | `(qfw: PushButton + FluentIcon.CANCEL)` | Emits `pipeline_cancel_requested` |

On cancel confirmation via `(qfw: MessageBox)`:

> *"Pipeline cancelled. Returning to the current step."*

The overlay is then replaced by the original step view.

### 15.4 First-Run Embedding Model Download

ARLO uses FastEmbed with the `mixedbread-ai/mxbai-embed-large-v1` model (~670 MB). On first pipeline run, FastEmbed downloads model files to the local `arlo/models/` cache directory.

- **Pre-download scripts:** `download_model.sh` (Linux/macOS) and `download_model.bat` (Windows) are provided. Users should run the appropriate script before starting the application.
- **In-app fallback:** If the model is not pre-downloaded, the orchestrator emits `embedding_download_needed`. The UI displays a `(qfw: MessageBox)`:

  > *"Embedding model not found. FastEmbed will download ~670 MB on first run. This may take several minutes depending on your connection. Continue?"*

  With **[Download & Continue]** and **[Cancel]** buttons. If the user proceeds, the UI emits `embedding_download_confirmed`. An `(qfw: IndeterminateProgressBar)` is shown during download. On `embedding_download_complete`, an `(qfw: InfoBar.success())` banner confirms download.

- **Download failure:** Error handling per §17, row 13.

### 15.5 WeasyPrint System Library Check

Before the first RGA invocation, the orchestrator (`Orchestrator_Spec.md` §7E) verifies that WeasyPrint can be imported and its rendering backend is functional. Error handling per §17, row 11.

---

## 16) Signal/Slot Contract Reference

This section is the authoritative source for all UI↔Orchestrator communication. Every signal listed here has a corresponding handler in the orchestrator. Both documents are symmetric.

> **Symmetry note:** Every signal listed here has a corresponding handler in the orchestrator (`Orchestrator_Spec.md` §8B–§8C). Both documents must be updated in tandem when signals are added, removed, or changed.

### 16.1 Signals Emitted by UI (→ Orchestrator)

| Signal | Payload | Triggered By |
|--------|---------|-------------|
| `project_create_requested` | `{name: str}` | "New Project" button |
| `project_selected` | `{project_id: str}` | Project card click |
| `llm_instance_saved` | `{instance_config: dict}` | LLM dialog "Save" |
| `llm_instance_deleted` | `{instance_name: str}` | LLM dialog delete button |
| `llm_fetch_models_requested` | `{provider, api_key, base_url}` | "Fetch Models" button |
| `llm_check_connectivity_requested` | `{}` | "Check Connectivity" button |
| `file_uploaded` | `{file_path: str}` | File dialog selection |
| `extraction_requested` | `{filter_config: dict}` | "Extract" button |
| `requirement_overrides_submitted` | `{overrides: list[{req_id, user_override}]}` | Requirement Editing save |
| `arlo_run_requested` | `{experiment_config: dict}` | "Run ARLO" button |
| `raa_run_requested` | `{batch_ordering: str}` | "Run RAA" button |
| `aga_run_requested` | `{aga_config: dict}` | "Run AGA" button |
| `sa_export_requested` | `{export_dir: str}` | "Export SA Artifacts" button |
| `pdf_report_requested` | `{report_config: dict}` | "Save Full PDF Report" button |
| `regenerate_diagrams_requested` | `{}` | "Regenerate Affected Diagrams" button |
| `rerun_raa_requested` | `{}` | "Re-run RAA" button |
| `pipeline_cancel_requested` | `{}` | "Cancel Run" button |
| `download_logs_requested` | `{}` | "Download Logs" button |
| `embedding_download_confirmed` | `{}` | Download dialog "Download & Continue" |

### 16.2 Signals Received by UI (← Orchestrator)

| Signal | Payload | UI Action |
|--------|---------|-----------|
| `project_created` | `{project_id, name, path}` | Add card to Projects View |
| `project_list_loaded` | `{projects: list[dict]}` | Populate project card list |
| `llm_models_fetched` | `{models: list[str]}` | Populate Model Name ComboBox |
| `llm_connectivity_result` | `{instance_name: str, reachable: bool}` | Update status badge per row |
| `extraction_progress` | `{stage: str, batch: int, total: int, eta_seconds: float}` | Update extraction ProgressBar + label |
| `extraction_complete` | `{filter_report: dict, requirements: dict}` | Populate Requirement Editing TableWidget |
| `arlo_progress` | `{batch: int, total: int, eta_seconds: float}` | Update ARLO ProgressBar |
| `arlo_complete` | `{asrs, quality_weights, concerns, stats}` | Populate ARLO Results Summary |
| `raa_progress` | `{batch: int, total: int, phase: str}` | Update RAA ProgressBar + phase label |
| `raa_complete` | `{model_stats: dict, open_questions: list}` | Populate RAA Results Summary |
| `aga_progress` | `{diagram: int, total: int, current_label: str}` | Update AGA ProgressBar |
| `aga_complete` | `{completed: list, failed: list, session_report: dict}` | Populate Diagram Gallery |
| `sa_progress` | `{node: int, total: int, node_name: str}` | Update SA ProgressBar |
| `sa_complete` | `{sa_report: dict, feedback_state: dict}` | Populate SA Results Display |
| `rga_progress` | `{phase: str}` | Update PDF generation ProgressBar + label |
| `rga_complete` | `{pdf_path, page_count, size_bytes, diagrams_embedded}` | Show success InfoBar |
| `pipeline_progress` | `{overall_pct: float, current_agent: str, eta_seconds: float}` | Update Pipeline Progress Overlay |
| `pipeline_error` | `{severity, source_agent, error_type, message, recoverable}` | Show MessageBox (blocking) or InfoBar |
| `pipeline_cancelled` | `{}` | Restore underlying view from overlay |
| `preflight_result` | `{checks: list[{name, passed, message}]}` | Show blocking MessageBox if any check failed |
| `embedding_download_needed` | `{size_mb: int}` | Show embedding download MessageBox |
| `embedding_download_complete` | `{}` | Show success InfoBar, continue pipeline |
| `pipeline_resume_available` | `{stage: str, run_id: str}` | Show resume confirmation dialog |

### 16.3 User Override Signals

| Override | UI Sends to Orchestrator | Orchestrator Action |
|----------|--------------------------|-------------------|
| Requirement keep/drop toggle | `{req_id, user_override: bool}` (via `requirement_overrides_submitted`) | Merge user overrides into final requirement set before ARLO |
| Bulk "Restore All Dropped" | `{action: "restore_all"}` | Reset all user overrides |
| Bulk "Drop Selected" / "Keep Selected" | `{req_ids: list, action: "drop"\|"keep"}` | Batch override update |

---

## 17) Failure Modes & Mitigations

All errors use blocking `(qfw: MessageBox)` dialogs (§15.1). `InfoBar` is reserved for success and informational confirmations.

| # | Error | Source Agent | Source View | Dialog Type | Blocking | Message Template |
|---|---|---|---|---|---|---|
| 1 | `EmptyFileError` | Ingestion | §9 | MessageBox | Yes | *"The selected file is empty or could not be read. Upload a valid document."* |
| 2 | `ExtractionError` | Ingestion | §9 | MessageBox | Yes | *"Requirement extraction failed. The document may be malformed or contain no extractable text."* |
| 3 | `NonStandardJSONError` | Ingestion | §9 | MessageBox | Yes | *"The JSON file does not match the expected schema. Upload a compliant file or enable 'Filter JSON Inputs'."* |
| 4 | `FormatMismatchError` | Ingestion | §9 | MessageBox | Yes | *"File format does not match its extension. Verify the file and re-upload."* |
| 5 | `UnsupportedFormatError` | Ingestion | §9 | MessageBox | Yes | *"Unsupported file format. Accepted formats: .pdf, .docx, .txt, .json."* |
| 6 | `ServerUnavailableException` | AGA | §13 | MessageBox | Yes | *"AGA halted: PlantUML server at '{url}' is unreachable. No diagrams were rendered. Check your network connection or configure a self-hosted server URL."* |
| 7 | `BinaryNotExecutableException` | AGA | §13 | MessageBox | Yes | *"AGA halted: PlantUML encoding binary not found or not executable at '{path}'. Ensure the planturl binaries are present in tools/planturl/Bin/."* |
| 8 | `ReportInputError` | RGA | §14 | MessageBox | Yes | *"PDF report generation failed: required pipeline data is missing or invalid. Detail: {error_message}. Ensure all pipeline stages completed successfully before generating the report."* |
| 9 | WeasyPrint render failure | RGA | §14 | MessageBox | Yes | *"PDF rendering failed. A section could not be converted to PDF. Detail: {error_message}. The report has been saved without the problematic section(s): {skipped_sections}."* |
| 10 | Disk write failure (IOError) | RGA | §14 | MessageBox | Yes | *"Failed to write PDF to disk. The target directory may be full or read-only. Detail: {error_message}."* |
| 11 | WeasyPrint system library missing | RGA | §15 | MessageBox | Yes | *"PDF generation requires system libraries that are not installed: WeasyPrint depends on libpango, libcairo, and libgdk-pixbuf. Install them with: Ubuntu/Debian: `sudo apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libcairo2 libffi-dev` / macOS: `brew install pango cairo gdk-pixbuf libffi`. Restart the application after installing."* |
| 12 | LLM unreachable | Orchestrator | §7 | MessageBox | Yes | *"Pipeline blocked: LLM instance '{name}' ({provider} at '{url}') is unreachable or model not found."* |
| 13 | Embedding download fail | Orchestrator | §15 | MessageBox | Yes | *"Failed to download embedding model from Hugging Face Hub. Check your network connection and proxy settings, then re-run the download script or restart the application."* |

> **Recovery policy:** All errors in rows 1–13 are blocking — the MessageBox must be dismissed before any further UI interaction. After dismissal, the view remains in its pre-error state; the user may correct inputs and retry.

---

## 18) Validation & Testing Criteria

### 18.1 Unit Tests

| # | Test | Expected Behaviour |
|---|---|---|
| 1 | Each view emits correct signal with correct payload schema on user action | Signal spy records matching signal name + payload keys |
| 2 | ProgressBar updates via `setVal()` not `setValue()` | Mock progress signal → `setVal` called with correct float |
| 3 | Sub-interface registration includes `setObjectName()` | Each registered panel has non-empty `objectName()` |
| 4 | Slider scaling: internal value 50 → displayed value 0.50 | Temperature slider readback matches ÷100 |
| 5 | Conditional panel visibility: VaryingRequirements panel hidden when BasicArlo selected | `isVisible()` returns `False` for the panel |
| 6 | Zero-requirement validation: all requirements dropped → "Next" disabled + InfoBar.warning | Navigation button `isEnabled() == False`; InfoBar shown |
| 7 | LLM instance name uniqueness: duplicate name → inline error label visible | `CaptionLabel` in error colour is visible |
| 8 | Filter JSON Inputs toggle hidden when non-JSON file selected | `isVisible() == False` |
| 9 | Ollama provider → API Key field greyed out and non-mandatory | `isEnabled() == False` on PasswordLineEdit |

### 18.2 Integration Tests

| # | Test | Expected Behaviour |
|---|---|---|
| 1 | Signal round-trip: UI emits `arlo_run_requested` → orchestrator responds with `arlo_progress` → ProgressBar updates | ProgressBar value changes on signal receipt |
| 2 | View swap: pipeline start → overlay replaces current view → cancel → original view restored | QStackedWidget index toggles correctly |
| 3 | Error dialog: orchestrator emits `pipeline_error(fatal)` → MessageBox appears and blocks | MessageBox is modal and contains correct message |
| 4 | Model fetch: UI emits `llm_fetch_models_requested` → orchestrator responds with `llm_models_fetched` → ComboBox populated | ComboBox items match returned model list |
| 5 | Pre-flight: pipeline start blocked when `preflight_result` contains failed check | MessageBox shown; pipeline does not start |
| 6 | Embedding download flow: `embedding_download_needed` → user confirms → `embedding_download_complete` → pipeline proceeds | IndeterminateProgressBar shown during download; success InfoBar after |

### 18.3 Functional Tests

| # | Test | Expected Behaviour |
|---|---|---|
| 1 | Single active run: second pipeline start attempt rejected while overlay active | Second start signal not emitted; no state corruption |
| 2 | Strict Checkpoint: navigating to Projects during active step → confirmation dialog | Dialog shown; on confirm, ephemeral state discarded |
| 3 | Full pipeline walkthrough: Projects → Config → Upload → Edit → ARLO → RAA → AGA → SA → PDF | All views render; all signals emit; PDF saved to disk |
| 4 | Regeneration loop: SA recommends regenerate → AGA re-runs on targeted subset → SA re-scores | Targeted diagrams only; SA score updates |
| 5 | RAA re-run: SA recommends rerun_raa → RAA → AGA → SA sequence completes | Full sub-loop executes; results update |
| 6 | Dark/light theme toggle: `setTheme(Theme.DARK)` → all widgets reflect theme | No unstyled widgets; all text readable |

---

## 19) Deliverables for Spec Kit

1. **Main window scaffold** — `FluentWindow` with sub-interface registration, navigation wiring, top bar actions (§1, §5)
2. **Projects View** — card list, creation dialog with uniqueness validation, project selection (§6)
3. **LLM Configuration Dashboard** — instance CRUD dialog, model fetch per provider, connectivity check with status badges (§7)
4. **LLM & Workflow Assignment View** — per-agent ComboBox assignment, RAA 4-slot configuration, per-project persistence (§8)
5. **Requirements Upload & Extraction View** — file picker with format filter, filter config controls (batch size, confidence, toggles), conditional JSON filtering toggle (§9)
6. **Requirement Editing View** — master-detail TableWidget with colour-coded rows, detail dialog with override toggle, bulk action toolbar, zero-requirement validation (§10)
7. **ARLO View** — experiment type/parsing mode/optimization selectors, VaryingRequirements conditional panel with multi-select quality attributes, inline results summary (§11)
8. **RAA View** — batch ordering selector, execution status panel with phase label cycling, per-batch detail expander, results summary with entity counts and open questions (§12)
9. **AGA View** — diagram gallery with selector, ImageLabel preview pane, expandable PlantUML code view, failed diagram error cards, advanced configuration (§13)
10. **SA View** — three-axis score breakdown with expandable sub-rubrics, gap analysis (5 sub-sections), feedback summary and adjustment log, recommended action panel with regenerate/rerun triggers, PDF report configuration, SA artifact export (§14)
11. **Global UI elements** — stage progress bars with ETA labels, pipeline progress overlay with cancel, embedding download dialog, WeasyPrint library check dialog (§15)
12. **Signal/slot contracts** — all UI→Orchestrator and Orchestrator→UI signals with payload schemas, user override signal table (§16)
13. **Error dialog system** — 13 failure modes with blocking MessageBox templates, severity classification, source view mapping (§17)

---

## 20) Dependencies

### 20.1 Python Packages

| Package | Version | Purpose |
|---|---|---|
| `PySide6` | ≥6.7 | Qt framework for Python |
| `PySide6-Fluent-Widgets` | ≥1.7 | Fluent Design widget library |

Registered under `[project.optional-dependencies]` group `ui` in `pyproject.toml`.

### 20.2 Internal Dependencies

| Dependency | Document | Governs |
|---|---|---|
| Orchestrator signal handlers | `Orchestrator_Spec.md` §8B–§8C | All UI-emitted signals must have corresponding orchestrator handlers |
| Pipeline state schema | `Orchestrator_Spec.md` §5 | Payload schemas for `extraction_complete`, `arlo_complete`, `raa_complete`, `aga_complete`, `sa_complete` |
| Ingestion error taxonomy | Ingestion plan §7H | Error types for §17 rows 1–5 |
| PDF reporting | `PDF_Reporting.md` | RGA invocation, PDF config fields, retry behaviour |
| Scoring report structure | Scoring Agent plan | `SARReport` fields rendered in §14 |

### 20.3 System Dependencies

| Dependency | Required By | Check |
|---|---|---|
| WeasyPrint system libraries (libpango, libcairo, libgdk-pixbuf) | PDF generation (§14) | Orchestrator pre-flight (§15.5) |
| PlantUML server (default or self-hosted) | AGA diagram rendering (§13) | AGA availability HEAD check |
| `planturl` encoding binary | AGA PlantUML encoding (§13) | AGA pre-flight binary check |
| FastEmbed model cache (`mixedbread-ai/mxbai-embed-large-v1`) | ARLO embeddings (§11) | First-run download (§15.4) |
