# PDF Report Service — Functional & Non-Functional Requirements

> **Version:** 1.0
> **Source Plan:** `requirements_planning/4_orchestrator/pdf_report_service_plan.md`
> **SRS Reference:** I-Architect SRS v2.3
> **Date:** 2026-03-24

---

## 1. Functional Requirements (FR)

### 1.1 Core Engine

#### FR-PDF-001: HTML-to-PDF Conversion Engine
- **Description:** The service SHALL use WeasyPrint as the core PDF rendering engine. All report content SHALL be authored as HTML using Jinja2 templates and converted to PDF via `weasyprint.HTML(string=html).write_pdf()`.
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** WeasyPrint produces valid PDF/A output from Jinja2-rendered HTML strings.

#### FR-PDF-002: Jinja2 Template System
- **Description:** The service SHALL use Jinja2 templates for data injection into HTML structures. Templates SHALL be stored in `templates/pdf/` within the Orchestrator container.
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** Template files exist and render valid HTML when populated with sample data.

#### FR-PDF-003: PDF Merge Capability
- **Description:** The service SHALL use `pypdf` for document assembly — specifically to merge Template A and Template B PDFs into a single document without re-rendering either.
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** Two separate PDFs are merged into a single document with correct page ordering.

### 1.2 Template A: ARLO Architectural Decision Report

#### FR-PDF-004: Template A Generation Trigger
- **Description:** Template A SHALL be auto-generated at the end of the ARLO pipeline step (Page 5). The trigger is the completion of the `arlo_user_review_node` in LangGraph — auto-generation occurs before the `interrupt_before` pause.
- **SRS Trace:** §1.7, §12
- **Priority:** Must
- **Acceptance Criteria:** ARLO completion automatically produces a PDF report without user action.

#### FR-PDF-005: Template A — Document Header
- **Description:** Template A SHALL include a header section with:
  - Title: "ARLO Architectural Decision Report"
  - Metadata: Generation Date, Tool Implementation ("ARLO v2.3"), Project Name.
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** The header renders with correct metadata values.

#### FR-PDF-006: Template A — Requirements Summary Table
- **Description:** Template A SHALL render a summary table with 3 metrics:
  1. Total Input Requirements (from filtered CSV).
  2. Total ASRs Identified.
  3. Total Condition Groups Generated.
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** Given 100 input requirements with 40 ASRs and 12 condition groups, all three values render correctly.

#### FR-PDF-007: Template A — ASR Registry Section
- **Description:** Template A SHALL:
  - If ASRs exist: Render a full table with columns: ASR ID, Description, Quality Attributes.
  - If no ASRs: Render fallback message: *"No Architecturally Significant Requirements were identified."*
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** A project with 0 ASRs shows the fallback message; a project with 15 ASRs shows a 15-row table.

#### FR-PDF-008: Template A — Architectural Decisions Section
- **Description:** Template A SHALL render a repeating section for every identified Concern, including:
  - **Concern Header:** Index #, Associated Conditions.
  - **Metrics:** Average Score, Desired Qualities + Weights.
  - **Decision Table:** Category, Selected Pattern Name, Score, Qualities Satisfied, Trade-offs (Negative Impacts).
  - **Fallback:** If no decisions generated, display: *"No architectural decisions were generated for this concern."*
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** A project with 3 concerns produces 3 repeated sections, each with metrics and decision tables.

#### FR-PDF-009: Template A — Full ASR Table Rendering (No Truncation)
- **Description:** Long ASR tables SHALL span multiple PDF pages rather than being truncated. WeasyPrint's CSS `page-break` properties SHALL be used to allow tables to flow across pages.
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** A 100-row ASR table renders across multiple pages without any rows being cut off.

### 1.3 Template B: Full Pipeline Report

#### FR-PDF-010: Template B Generation Trigger
- **Description:** Template B SHALL be generated on user request via the "⬇ Download Full PDF Report" button on the SA Page (Page 8).
- **SRS Trace:** §1.10, §12
- **Priority:** Must
- **Acceptance Criteria:** Clicking "Download Full PDF Report" triggers PDF generation and browser download.

#### FR-PDF-011: Template B — Physical Merge Strategy
- **Description:** Template B SHALL be constructed by physically appending "Part 2" to the existing Template A PDF:
  1. Locate the latest `Template_A_*.pdf` for the current project.
  2. Generate "Part 2" PDF containing RAA, AGA, and SA sections.
  3. Merge Template A + Part 2 → `Template_B_{timestamp}.pdf` using `pypdf`.
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** Template B starts with Template A's content, followed by Part 2's content; no pages are duplicated or lost.

#### FR-PDF-012: Template B — RAA Section
- **Description:** Part 2 SHALL include a section rendering the RAA's contribution: user instructions and a TOON Summary (key entities and relationships in tabular format).
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** The RAA section renders entity and relationship data from the TOON IR.

#### FR-PDF-013: Template B — AGA Section
- **Description:** Part 2 SHALL include a section rendering: the PlantUML code block (monospaced, syntax-highlighted) and the **rendered diagram** as a full-page image (PNG sourced from the PlantUML server).
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** The AGA section shows both the `.puml` source code and the rendered diagram image.

#### FR-PDF-014: Template B — SA Section
- **Description:** Part 2 SHALL include a section rendering: Score Breakdown (total and per-pillar), Drawback Cards (severity, category, description, affected entities), and Adjustments Needed checklist.
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** All SA output data is present in the PDF — no fields are omitted.

### 1.4 Smart Layout

#### FR-PDF-015: Automatic Landscape Rotation for Diagrams
- **Description:** The diagram page in the AGA Section SHALL be rendered in landscape orientation (A4 Landscape) using CSS `@page` rules:
  ```css
  @page landscape-page { size: A4 landscape; margin: 1cm; }
  .diagram-container { page: landscape-page; }
  ```
  This ensures wide diagrams are viewable without shrinking.
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** The diagram page is rotated 90° in the PDF viewer while all other pages remain portrait.

### 1.5 File Management

#### FR-PDF-016: Output Naming Convention
- **Description:** PDF files SHALL be named: `Report_{Type}_{Agent}_{Timestamp}.pdf` where Type is `A` or `B`, Agent is the source agent identifier, and Timestamp follows `YYYYMMDD_HHMMSS` format.
- **SRS Trace:** §12, §3
- **Priority:** Must
- **Acceptance Criteria:** Generated filenames match the pattern.

#### FR-PDF-017: Retention Policy (5 Versions)
- **Description:** Before saving a new PDF, the service SHALL list existing files matching the naming pattern in `/{project}/pdf/`. If count ≥ 5, the oldest file (by `os.path.getmtime`) SHALL be deleted before the new file is saved.
- **SRS Trace:** §12
- **Priority:** Must
- **Acceptance Criteria:** After generating 6 Template A reports, only the 5 most recent remain.

#### FR-PDF-018: Write Isolation
- **Description:** The `PdfReportService` class SHALL be the ONLY writer to `/{project}/pdf/`. No other agent, service, or middleware SHALL write to this directory.
- **SRS Trace:** §12, §6
- **Priority:** Must
- **Acceptance Criteria:** Unauthorized write attempts to `pdf/` are rejected.

---

## 2. Non-Functional Requirements (NFR)

### NFR-PDF-001: Synchronous Blocking Execution
- **Description:** PDF generation SHALL block the UI thread (synchronous). The UI SHALL display a "Generating PDF..." spinner during generation.
- **SRS Trace:** §12
- **Metric:** UI is blocked during PDF generation; spinner is visible.

### NFR-PDF-002: Sequential Execution per Session
- **Description:** WeasyPrint is CPU-bound. The service SHALL ensure that `weasyprint.HTML(string).write_pdf()` is called strictly sequentially per user session to avoid CPU contention on the resource-constrained container.
- **SRS Trace:** §12
- **Metric:** No concurrent WeasyPrint processes per container instance.

### NFR-PDF-003: Disk Quota Pre-Check
- **Description:** Before generation, the service SHALL check the project disk usage. If the project exceeds its 500MB quota, the service SHALL fail gracefully with a "Disk Full" modal message.
- **SRS Trace:** §6.1
- **Metric:** A full project triggers the "Disk Full" error before any PDF bytes are written.

### NFR-PDF-004: OS Dependencies
- **Description:** The Docker image SHALL be based on `python:3.11-slim` (Debian) and include `libcairo2` and `libpango-1.0` (required by WeasyPrint) installed via `apt-get`.
- **SRS Trace:** §12
- **Metric:** `weasyprint.HTML(string='<h1>Test</h1>').write_pdf()` executes without missing library errors.

---

## 3. Interface Requirements (IR)

### IR-PDF-001: Input Interfaces
| Input | Source | Format |
|:--|:--|:--|
| ARLO Data | `arlo_output/*.toon` | TOON (JSON) — parsed by Jinja2 |
| RAA Data | `raa_output/*.toon` or `mcp_aggregator/raa_aggregated.toon` | TOON (JSON) |
| AGA Code | `aga_output/*.puml` or `mcp_aggregator/aga_aggregated.puml` | PlantUML text |
| AGA Diagram Image | PlantUML server (`POST /png/`) | PNG binary |
| SA Data | `sa_output/*.json` or `mcp_aggregator/sa_aggregated.json` | Evaluation JSON |

### IR-PDF-002: Output Interface
- **Target:** `/{project}/pdf/`
- **Naming:** `Report_{A|B}_{Agent}_{YYYYMMDD_HHMMSS}.pdf`
- **Consumer:** UI download button, Streamlit PDF viewer.

### IR-PDF-003: Class Interface
```python
class PdfReportService:
    def __init__(self, project_root: str):
        self.output_dir = os.path.join(project_root, "pdf")

    def generate_template_a(self, arlo_json_data: dict) -> str:
        """Renders ARLO report. Returns path to generated PDF."""
        pass

    def generate_template_b(
        self, raa_data, aga_data, sa_data, template_a_path
    ) -> str:
        """Renders RAA/AGA/SA report and merges with Template A."""
        pass
```

---

## 4. Disaster Recovery Requirements (DR)

### DR-PDF-001: WeasyPrint Rendering Failure
- **Failure Mode:** WeasyPrint throws an exception during HTML-to-PDF conversion (e.g., invalid CSS, missing fonts).
- **Recovery Action:** Log the exception. Return a "generation failed" status to the UI. Do not retry automatically (CSS issues require template fixes).
- **User-Facing Message:** 🛑 *"PDF generation failed due to a rendering error. Please contact support."*
- **SRS Trace:** §13

### DR-PDF-002: Missing Template A for Template B Merge
- **Failure Mode:** No Template A PDF exists when Template B generation is requested.
- **Recovery Action:** Auto-generate Template A first (if ARLO data is available) or generate Template B without the ARLO section (Part 2 only).
- **User-Facing Message:** ⚠️ *"No ARLO report found. The full report will include only RAA/AGA/SA sections."*
- **SRS Trace:** §12

### DR-PDF-003: Disk Full During Generation
- **Failure Mode:** `OSError: [Errno 28] No space left on device` during `write_pdf()`.
- **Recovery Action:** Delete temporary partial PDF. Trigger disk quota check. Display "Disk Full" modal.
- **User-Facing Message:** 🛑 *"Cannot generate PDF: Project has exceeded its disk quota. Please delete old runs or reports."*
- **SRS Trace:** §6.1

---

*End of PDF Report Service Requirements Document*
