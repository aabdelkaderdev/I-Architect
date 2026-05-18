# PDF Report Generation Agent (RGA) — Implementation Plan

## 0) Goal of this Portion

Generate a **polished, multi-page PDF report** that consolidates the entire I-Architect pipeline output — original requirements, ARLO classification results, RAA architecture model, AGA-rendered diagrams, SA scoring report, and ingestion filtering metadata — into a single, professionally formatted document suitable for stakeholder review, academic submission, or archival.

The RGA is the **final consumer** in the pipeline. It reads all upstream outputs but modifies none. Its sole responsibility is document assembly and rendering.

> **Pipeline position:** Ingestion → ARLO → RAA → AGA → SA → **RGA** → PDF file on disk.

---

## 1) Inputs and Assumptions

### Inputs from Upstream Agents

- **`arch_model` (`C4JsonModel`)** — the hierarchical architecture model from RAA (received through AGA/SA boundary). Type defined in AGA §1. Contains `systems`, `persons`, `external_systems`, `patterns`, `diagram_manifest`, `confidence_metadata`, `open_questions`.
- **`aga_output` (`AGAOutput`)** — AGA rendering results. Type defined in AGA §13. Contains `completed_diagrams` (list of `CompletedDiagram` with `png_bytes`, `plantuml_source`, `diagram_id`, `diagram_type`, `output_path`), `failed_diagrams`, and `session_report`.
- **`sa_report` (`SARReport`)** — SA scoring output. Type defined in SA §9. Contains `summary` (total score, grade, recommended action), `axis_scores`, `gap_analysis`, `executive_summary`, `feedback_summary`.
- **`requirements_data` (`dict`)** — packed by the orchestrator: `{"requirements": dict[str, str], "asrs": list[str], "non_asr": list[str], "quality_weights": dict[str, int]}`.
- **`filter_report` (`dict | null`)** — ingestion filtering summary from the RFA (Ingestion §8G). Null if filtering was bypassed.

### Inputs from Configuration

- **`report_config` (`ReportConfig`)** — user-configurable parameters for PDF generation: output path, logo path, colour theme, page size, whether to include appendices, maximum diagram scale factor.
- **`pipeline_metadata` (`PipelineMetadata`)** — orchestrator-provided run metadata: `pipeline_run_id`, `run_timestamp`, `pipeline_version`, per-subgraph LLM model names (`subgraph_llms`), total and per-subgraph wall-clock times (`subgraph_timings`).

### Assumptions

- RGA does not modify any upstream output. It is a pure rendering agent with no architecture or scoring logic.
- All diagram PNGs are already rendered by AGA and available as `png_bytes` in `completed_diagrams`. RGA does not call the PlantUML server.
- The RGA is implemented as a **standalone LangGraph StateGraph**, invoked by the orchestrator after SA completes. It is not composed as a subgraph inside SA.
- The pipeline is strictly sequential — no parallel fan-out is used within RGA.
- PDF generation uses **WeasyPrint** for HTML/CSS-to-PDF conversion. No LaTeX dependency. No browser-based conversion (WeasyPrint uses its own rendering engine, not a headless browser). WeasyPrint requires certain system libraries (see §15).
- The RGA contains **zero LLM calls**. All content — including the "Architectural Insights" section — is assembled deterministically from upstream structured data using Python string templates. No prompt files, no skill bundles, no generative reasoning.

### Integration Pattern

The orchestrator calls:

```python
rga_graph.invoke({
    "arch_model": raa_output_model,
    "aga_output": aga_output,
    "sa_report": sa_report,
    "requirements_data": requirements_data,
    "filter_report": filter_report,
    "report_config": report_config,
    "pipeline_metadata": pipeline_metadata,
}, config={"configurable": {"thread_id": computed_thread_id}})
```

---

## 2) Authoritative Source Register

### 2A — Source Register Table

| Source | URL | Retrieval Date | Governs |
|--------|-----|----------------|---------|
| C4 Model — Diagrams | https://c4model.com/diagrams | (set on retrieval) | Diagram caption labelling conventions |
| ISO/IEC 25010 | (internal reference via RAA `Quality_Attributes.md`) | Internal | Quality attribute names in the QA heatmap |
| WeasyPrint Documentation | https://doc.courtbouillon.org/weasyprint/stable/ | (set on retrieval) | HTML/CSS-to-PDF rendering engine API, CSS print media support, image embedding |

### 2B — Deterministic Content Policy

The RGA contains **no LLM calls**. All report content is assembled from upstream structured data via deterministic Python string templates. The following constraints govern the "Architectural Insights" section (§5J), which is the only section requiring interpretive assembly:

- The insights text references only entities, patterns, and quality attributes that exist in `arch_model` and `sa_report`. No invented entities.
- The insights text does not contradict the SA grade or scoring axis values.
- The insights text is assembled from three deterministic sub-sections: Architecture Overview (model statistics), QA Risk Assessment (top 2 ARLO-weighted quality attributes and their SA axis scores), and Completeness Summary (orphaned requirements, failed diagrams, open question counts).
- All values are extracted directly from upstream state channels — no generative reasoning is applied.

### 2C — Template Policy

- HTML templates are stored as Jinja2 `.html` files in `reporting/templates/`, with a base layout and per-section partial templates.
- CSS stylesheets are stored in `reporting/templates/css/` and referenced by the base HTML layout.
- Direction of authority: **Source Register → HTML/CSS Templates → WeasyPrint Render**.

---

## 3) High-Level Pipeline Overview

The RGA executes six sequential nodes:

1. **Data Collection & Validation:** Load and cross-reference all upstream outputs. Validate that required fields are present. Build internal lookup structures.
2. **Report Structure Planning:** Determine which sections to include based on data availability (e.g., skip filtering appendix if `filter_report` is null). Compute page estimates.
3. **Content Assembly:** Render all sections — cover page, requirements summary tables, scoring rubric breakdown, diagram gallery, gap analysis, architectural insights, appendices — as HTML fragments using Jinja2 templates populated with upstream data. All sections are deterministic.
4. **Deterministic Insights Assembly:** Build the "Architectural Insights" section from upstream structured data (SA scores, ARLO weights, model statistics, gap counts). No LLM call — pure template rendering.
5. **PDF Rendering:** Concatenate all HTML section fragments into a single HTML document using the base layout template. Inject CSS stylesheets. Pass the complete HTML to WeasyPrint for PDF rendering.
6. **Output & Validation:** Write the PDF to disk. Validate page count and file integrity. Record session metadata.

---

## 4) State Schema

All reducers use default `overwrite` semantics (sequential graph).

| Channel | Type | Reducer | Description |
|---------|------|---------|-------------|
| `arch_model` | `C4JsonModel` | overwrite | Read-only input from RAA/AGA/SA boundary |
| `aga_output` | `AGAOutput` | overwrite | Read-only input from AGA |
| `sa_report` | `SARReport` | overwrite | Read-only input from SA |
| `requirements_data` | `dict` | overwrite | Read-only input from orchestrator |
| `filter_report` | `dict \| null` | overwrite | Read-only input from ingestion pipeline. Null if filtering was bypassed. |
| `report_config` | `ReportConfig` | overwrite | User-configurable PDF generation parameters |
| `pipeline_metadata` | `PipelineMetadata` | overwrite | Orchestrator-provided run metadata |
| `section_plan` | `list[SectionSpec]` | overwrite | Ordered list of report sections with inclusion flags. Produced by Node 2. |
| `static_sections` | `dict[str, SectionContent]` | overwrite | Rendered content for each deterministic section. Produced by Node 3. |
| `insights_html` | `str` | overwrite | Deterministic architectural insights HTML fragment, assembled from SA/ARLO/model data. Produced by Node 4. |
| `pdf_bytes` | `bytes \| null` | overwrite | The rendered PDF document. Produced by Node 5. |
| `output_report` | `RGAOutput` | overwrite | Final output metadata. Produced by Node 6. |

### Supporting Type Definitions

**`ReportConfig`:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `output_dir` | `str` | `"output/"` | Directory where the PDF is written |
| `output_filename` | `str \| null` | `null` | Override filename. If null, derived as `i-architect-report-{pipeline_run_id}.pdf` |
| `page_size` | `str` | `"A4"` | Page size: `"A4"` or `"LETTER"` |
| `include_appendices` | `bool` | `true` | Whether to include appendix sections (filtering report, open questions, full requirement list) |
| `include_plantuml_source` | `bool` | `false` | Whether to include raw PlantUML source code alongside diagrams |
| `max_diagram_width_ratio` | `float` | `0.85` | Maximum diagram width as fraction of page content width |
| `logo_path` | `str \| null` | `null` | Optional path to a logo image for the cover page |
| `colour_theme` | `str` | `"default"` | Colour theme for headings, tables, and score indicators: `"default"`, `"monochrome"`, `"dark"` |

**`PipelineMetadata`:**

| Field | Type | Description |
|-------|------|-------------|
| `pipeline_run_id` | `str` | The RAA thread_id that identifies this pipeline run |
| `run_timestamp` | `str` | ISO 8601 UTC timestamp of pipeline start |
| `pipeline_version` | `str` | Semantic version of the I-Architect pipeline |
| `total_wall_clock_seconds` | `float` | Total pipeline execution time |
| `subgraph_llms` | `dict[str, str]` | Per-subgraph LLM model names. Keys are canonical subgraph identifiers (see table below). Values are the fully-qualified model name string (e.g. `"gpt-4o-2024-08-06"`). Populated by the orchestrator before RGA invocation. |
| `subgraph_timings` | `dict[str, float]` | Per-subgraph wall-clock execution times in seconds. Same key space as `subgraph_llms`. Populated by the orchestrator after each subgraph completes. |

**Canonical Subgraph Keys for `subgraph_llms` and `subgraph_timings`:**

| Key | Subgraph / Agent | Description |
|-----|-----------------|-------------|
| `ingestion` | Data Ingestion & Requirement Filtering | File parsing, requirement extraction, and RFA filtering |
| `arlo` | ARLO Classification | Requirement classification into quality attributes |
| `raa` | Requirements-Aware Architect (RAA) | Architecture model generation from classified requirements |
| `aga` | Architecture Graph Agent (AGA) | PlantUML diagram rendering from the architecture model |
| `sa` | Scoring Agent (SA) | Architecture quality scoring and gap analysis |
| `rga` | Report Generation Agent (RGA) | PDF report assembly (this agent) |

**`SectionSpec`:**

| Field | Type | Description |
|-------|------|-------------|
| `section_id` | `str` | Canonical section identifier (e.g., `cover`, `toc`, `exec_summary`, `req_table`, `scoring`, `diagrams`, `gap_analysis`, `insights`, `appendix_filter`, `appendix_oq`, `appendix_reqs`) |
| `title` | `str` | Human-readable section title for the PDF heading |
| `included` | `bool` | Whether this section appears in the final PDF |
| `estimated_pages` | `int` | Rough page estimate for TOC planning |
| `order` | `int` | Render order (0-indexed) |

**`SectionContent`:**

| Field | Type | Description |
|-------|------|-------------|
| `section_id` | `str` | Matches `SectionSpec.section_id` |
| `html_fragment` | `str` | Rendered HTML fragment string for this section, produced by the corresponding Jinja2 partial template. Assembled into the final HTML document during Node 5. |

**`RGAOutput`:**

| Field | Type | Description |
|-------|------|-------------|
| `pdf_path` | `str` | Absolute path to the written PDF file |
| `pdf_size_bytes` | `int` | File size in bytes |
| `page_count` | `int` | Total number of pages in the rendered PDF |
| `sections_included` | `list[str]` | List of `section_id` values that were included |
| `diagrams_embedded` | `int` | Number of AGA diagrams embedded in the PDF |
| `diagrams_failed_omitted` | `int` | Number of AGA failed diagrams noted but not embedded |
| `generation_wall_clock_seconds` | `float` | RGA execution time |

---

## 5) PDF Document Structure

The report is organised into the following sections, rendered in order:

### 5A — Section Registry

| # | Section ID | Title | Content Source | Conditional |
|---|-----------|-------|---------------|-------------|
| 1 | `cover` | Cover Page | `pipeline_metadata`, `report_config` | Always |
| 2 | `toc` | Table of Contents | Auto-generated via HTML heading anchors and a Jinja2 TOC partial that iterates `section_plan` | Always |
| 3 | `llm_config` | LLM Configuration Overview | `pipeline_metadata.subgraph_llms` | Always |
| 4 | `timing` | Subgraph Execution Timing | `pipeline_metadata.subgraph_timings`, `pipeline_metadata.total_wall_clock_seconds` | Always |
| 5 | `exec_summary` | Executive Summary | `sa_report.executive_summary.markdown`, `sa_report.summary` | Always |
| 6 | `req_table` | Requirements Overview | `requirements_data`, `filter_report` | Always |
| 7 | `scoring` | Architecture Scoring Report | `sa_report.summary`, `sa_report.axis_scores` | Always |
| 8 | `diagrams` | Architecture Diagrams | `aga_output.completed_diagrams`, `arch_model.diagram_manifest` | Always |
| 9 | `gap_analysis` | Gap Analysis | `sa_report.gap_analysis` | Always |
| 10 | `insights` | Architectural Insights | Deterministic template narrative (Node 4) — assembled from `sa_report`, `arch_model`, `requirements_data` | Always |
| 11 | `appendix_filter` | Appendix A: Filtering Report | `filter_report` | `filter_report` is non-null AND `include_appendices` is true |
| 12 | `appendix_oq` | Appendix B: Open Questions | `arch_model.open_questions` | `open_questions` is non-empty AND `include_appendices` is true |
| 13 | `appendix_reqs` | Appendix C: Full Requirement Listing | `requirements_data.requirements` | `include_appendices` is true |
| 14 | `appendix_patterns` | Appendix D: Pattern Rationales | `arch_model.patterns` | `patterns` is non-empty AND `include_appendices` is true |

### 5B — Cover Page Layout

- **Creation Date & Time:** Every generated report displays the report creation date and time prominently on the cover page. The value is rendered from `pipeline_metadata.run_timestamp` (ISO 8601 UTC), formatted as a human-readable local date/time string (e.g., *"Generated: 18 May 2026, 14:30:45 UTC"*).
- **Title:** "I-Architect — Architecture Analysis Report"
- **Subtitle:** Pipeline run ID and generation timestamp
- **Logo:** If `report_config.logo_path` is provided and the file exists, render it centred at the top (max height 80pt). Otherwise, skip.
- **Metadata block:** Pipeline version, total wall-clock time, page size. (Detailed per-subgraph LLM and timing information is in the dedicated §5C and §5D sections.)
- **Grade badge:** Large circular badge showing the SA letter grade (A/B/C/D/F) with colour coding: A=green, B=blue, C=amber, D=orange, F=red. Numerical score displayed below.

### 5C — LLM Configuration Overview Section

Renders a summary table showing which LLM model is used by each agent / subgraph in the pipeline. This gives stakeholders and reviewers immediate visibility into the models that produced the architectural outputs.

- **LLM Configuration table:** 3-column table with columns: Subgraph, Agent Name, LLM Model. One row per canonical subgraph key (see `PipelineMetadata.subgraph_llms`). Rows are ordered following the pipeline execution order: Ingestion → ARLO → RAA → AGA → SA → RGA.
- **Source:** `pipeline_metadata.subgraph_llms`.
- If a subgraph key is absent from `subgraph_llms` (e.g., the subgraph was skipped), the LLM Model cell displays "—" (em-dash).

### 5D — Subgraph Execution Timing Section

Renders a timing breakdown table showing the wall-clock execution time of each subgraph. This section is populated entirely by the orchestrator, which records start/end timestamps around each subgraph invocation.

- **Timing table:** 4-column table with columns: Subgraph, Agent Name, Wall-Clock Time (s), Percentage of Total. One row per canonical subgraph key, plus a **Total** footer row showing `pipeline_metadata.total_wall_clock_seconds`.
- **Percentage computation:** `(subgraph_time / total_wall_clock_seconds) × 100`, rendered to one decimal place.
- **Timing bar:** Below the table, an optional horizontal stacked bar chart showing the proportional time contribution of each subgraph (colour-coded by subgraph). Rendered as an inline CSS bar using `<div>` elements with percentage-based widths and subgraph-specific background colours.
- **Source:** `pipeline_metadata.subgraph_timings`, `pipeline_metadata.total_wall_clock_seconds`.
- If a subgraph key is absent from `subgraph_timings` (e.g., the subgraph was skipped), the time cell displays "—" and the subgraph is excluded from percentage calculation and bar chart.

### 5E — Executive Summary Section

Renders `sa_report.executive_summary.markdown` as formatted paragraphs. Below the narrative:

- **Scorecard table:** 3-column table showing Axis name, Points Awarded, Points Possible for each of the three SA axes plus a Total row.
- **Key findings:** Bulleted list of `sa_report.executive_summary.key_findings`.
- **Recommended action:** Highlighted callout box showing `sa_report.summary.recommended_action` with colour-coded background (green for `accept`, amber for `regenerate_diagrams`, red for `rerun_raa`).

### 5F — Requirements Overview Section

- **Summary statistics table:** Total requirements, ASR count, non-ASR count, orphaned count. If `filter_report` is non-null: total input, signal count, noise dropped count, noise kept count, confidence threshold used.
- **Quality attribute weight distribution:** Horizontal bar chart rendered as styled HTML `<div>` elements with percentage-based widths, showing ARLO `quality_weights` sorted descending. Each bar is labelled with the attribute name and raw count.
- **ASR vs Non-ASR breakdown:** Stacked bar rendered as inline HTML `<div>` elements showing the proportion.

### 5G — Scoring Report Section

- **Overall grade banner:** Letter grade and numerical score with colour-coded background.
- **Axis 1 — Functional Traceability (40 pts):** Sub-rubric breakdown table. Explicit mapping score, depth score with distribution percentages, orphan penalty.
- **Axis 2 — Quality Attributes (40 pts):** Sub-rubric breakdown table. ASR traceability, high-risk mitigation score, top risk attributes listed, technology confidence score, contradiction penalties.
- **Axis 3 — Diagram Accuracy (20 pts):** Sub-rubric breakdown table. Per-diagram scores rendered as a multi-row table with columns: Diagram ID, Type, Render Success, Sub-tree Complete, Unverified Count, Open Question Conflict, Score.
- **Score composition bar:** Stacked horizontal bar chart showing the three axis contributions to the 100-point total.

### 5H — Architecture Diagrams Section

For each entry in `arch_model.diagram_manifest`:
- If `diagram_id` is in `aga_output.completed_diagrams`: embed the PNG image scaled to fit `max_diagram_width_ratio` of page content width while preserving aspect ratio. Below the image, render a caption: `"{label} ({diagram_type})"`. If `include_plantuml_source` is true, render the PlantUML source in a monospaced code block below the diagram.
- If `diagram_id` is in `aga_output.failed_diagrams`: render a placeholder box with the text "Diagram generation failed" and the `final_error.error_type` from the `FailedDiagram` record.

Diagrams are ordered following the manifest order (context → container → component, as defined by RAA §16).

### 5I — Gap Analysis Section

- **Orphaned requirements table:** Columns: Req ID, Is ASR, Quality Attributes, Text Snippet (120 chars). Sourced from `sa_report.gap_analysis.orphaned_requirements`.
- **Failed diagrams table:** Columns: Diagram ID, Type, Error Type, Retry Count. Sourced from `sa_report.gap_analysis.failed_diagrams`.
- **Incomplete diagrams table:** Columns: Diagram ID, Focus Entity, Missing Entity IDs. Sourced from `sa_report.gap_analysis.incomplete_diagrams`.
- **Open questions affecting scores:** Columns: Entity ID, Type, Description, Affected Diagram IDs. Sourced from `sa_report.gap_analysis.open_questions_flagged`.

### 5J — Architectural Insights Section

Deterministic template-rendered section (see §6, Node 4). Assembled from upstream structured data with no LLM involvement. Rendered with a distinctive header style to differentiate it from the executive summary. Contains three sub-sections:

- **Architecture Overview:** Model statistics — number of systems, containers, components, external systems. Selected architectural patterns with rationale summaries.
- **Quality Attribute Risk Assessment:** Top 2 quality attributes by ARLO weight, their SA axis scores, and whether they are adequately addressed. Sources: `requirements_data.quality_weights`, `sa_report.axis_scores.quality_attributes.top_risk_attributes`.
- **Completeness Summary:** Number of orphaned requirements, failed diagrams, incomplete diagrams, and open questions. Provides a deterministic "health check" snapshot of the architecture model.

---

## 6) Node Definitions

### Node 1: Data Collection & Validation (Deterministic)

* **Task:** Load all upstream outputs, validate required fields, build lookup structures.
* **Action:**
  1. Validate `arch_model` is non-null and contains `systems`, `diagram_manifest`.
  2. Validate `sa_report` is non-null and contains `summary`, `axis_scores`, `executive_summary`.
  3. Validate `aga_output` is non-null and contains `completed_diagrams`.
  4. Build `completed_diagram_map`: dict mapping `diagram_id` → `CompletedDiagram`.
  5. Build `failed_diagram_ids`: set of `diagram_id` values from `aga_output.failed_diagrams`.
  6. Validate `requirements_data` contains `requirements`, `asrs`, `non_asr`, `quality_weights`.
  7. If any critical validation fails, raise `ReportInputError` with a descriptive message. The pipeline halts — a report cannot be generated from incomplete data.
* **Output:** Validated inputs in state channels, lookup structures.

### Node 2: Report Structure Planning (Deterministic)

* **Task:** Determine which sections to include and compute page estimates.
* **Action:**
  1. Iterate the Section Registry (§5A). For each section, evaluate the conditional inclusion rule.
  2. Compute `estimated_pages` per section: cover=1, TOC=1, llm_config=1, timing=1, exec_summary=1–2, req_table=1–2 (depends on requirement count), scoring=2–3, diagrams=⌈completed_count/2⌉ (2 diagrams per page), gap_analysis=1–2, insights=1, each appendix=1–⌈item_count/30⌉.
  3. Build the ordered `section_plan` list.
* **Output:** `section_plan`.

### Node 3: Content Assembly (Deterministic)

* **Task:** Render all report sections as HTML fragment strings using Jinja2 partial templates.
* **Action:**
  1. **Cover page:** Render `cover.html` partial with title, subtitle, metadata block, and grade badge. If `logo_path` is provided and file exists, embed the image as a base64-encoded `<img>` tag.
  2. **Table of contents:** Render `toc.html` partial by iterating `section_plan` and generating anchor links to each included section's heading ID.
  3. **LLM configuration overview:** Render `llm_config.html` partial with a 3-column HTML `<table>` from `pipeline_metadata.subgraph_llms`. Iterate canonical subgraph keys in pipeline order.
  4. **Subgraph execution timing:** Render `timing.html` partial with a 4-column HTML `<table>` from `pipeline_metadata.subgraph_timings`. Compute percentage-of-total. Append total footer row. Render horizontal stacked bar as CSS `<div>` elements.
  5. **Executive summary:** Render `exec_summary.html` partial. Convert SA markdown to HTML using Python's `markdown` library. Build scorecard table, key findings list, recommended action callout.
  6. **Requirements overview:** Render `req_table.html` partial with statistics table and CSS-styled bar charts for quality attribute weights and ASR/non-ASR breakdown.
  7. **Scoring report:** Render `scoring.html` partial with overall banner, per-axis breakdown tables, per-diagram scoring table, score composition bar.
  8. **Diagrams:** Render `diagrams.html` partial. For each manifest entry, embed `png_bytes` as a base64-encoded `<img>` tag or render a placeholder `<div>` for failed diagrams. Add captions. Optionally add PlantUML source in `<pre><code>` blocks.
  9. **Gap analysis:** Render `gap_analysis.html` partial with orphaned requirements table, failed diagrams table, incomplete diagrams table, open questions table. Zero-row tables display a "No issues found" placeholder.
  10. **Appendices:** If included, render the appropriate appendix partials: filtering report, open questions listing, full requirements listing, pattern rationales.
* **Output:** `static_sections` dict keyed by `section_id`, each containing an `html_fragment` string.

### Node 4: Deterministic Insights Assembly (Deterministic)

* **Task:** Build the "Architectural Insights" section from upstream structured data. No LLM call.
* **Data extraction:**
  - SA total score, grade, recommended action from `sa_report.summary`.
  - Top 2 quality attributes by ARLO weight from `requirements_data.quality_weights`. Cross-reference with `sa_report.axis_scores.quality_attributes.top_risk_attributes` for mitigation status.
  - Model statistics: count of systems, containers, components, external systems from `arch_model`.
  - Selected patterns: names and rationale summaries from `arch_model.patterns`.
  - Gap counts: orphaned requirements, failed diagrams, incomplete diagrams, open questions from `sa_report.gap_analysis`.
* **Template rendering:** Render `insights.html` Jinja2 partial with the extracted data. The template produces three sub-sections: Architecture Overview, QA Risk Assessment, Completeness Summary.
* **Output:** `insights_html` (HTML fragment string).

### Node 5: PDF Rendering (Deterministic)

* **Task:** Assemble all HTML fragments into a single HTML document and convert to PDF using WeasyPrint.
* **Action:**
  1. Load the base layout template (`base.html`) which defines the full HTML document structure: `<html>`, `<head>` (with `<link>` to the theme CSS), `<body>` with header, content area, and footer.
  2. Build the body content by iterating `section_plan` in order. For each included section, insert its `html_fragment` from `static_sections`. Insert `insights_html` at the `insights` position.
  3. The CSS stylesheet (selected by `report_config.colour_theme`) handles all styling: page margins via `@page` rules, headers/footers via `@page` margin boxes with CSS `content` properties, page breaks between sections via `page-break-before: always`, and running headers via `string-set` / `string()` CSS constructs.
  4. Pass the complete HTML string and the resolved CSS to `weasyprint.HTML(string=html_string).write_pdf()`. WeasyPrint renders the document, handles pagination, and produces the PDF bytes.
  5. Capture the returned bytes.
* **Output:** `pdf_bytes`.

### Node 6: Output & Validation (Deterministic)

* **Task:** Write the PDF to disk and validate.
* **Action:**
  1. Determine output path: `{output_dir}/{output_filename}` or `{output_dir}/i-architect-report-{pipeline_run_id}.pdf`.
  2. Create `output_dir` if it does not exist.
  3. Write `pdf_bytes` to the output path.
  4. Validate: file exists, file size > 0, first 5 bytes match `%PDF-` magic bytes.
  5. Count pages by re-reading the PDF with `PdfReader` from `PyPDF2`.
  6. Build `RGAOutput` with all metadata fields.
* **Output:** `output_report` (`RGAOutput`).

---

## 7) Skills vs Static Templates

### Use Skills For
- **None.** The RGA contains zero LLM calls. No skill resource bundles are required.

### Use Static Templates For
- **Data validation (Node 1):** deterministic field presence checks.
- **Section planning (Node 2):** deterministic conditional evaluation and page estimation.
- **All content assembly (Node 3):** cover page layout, table construction, chart rendering, diagram embedding, gap analysis tables, appendix formatting — all are mechanical Jinja2 template fills with no ambiguity.
- **Insights assembly (Node 4):** deterministic extraction of model statistics, QA risk data, and gap counts into a structured Jinja2 template.
- **PDF rendering (Node 5):** WeasyPrint HTML-to-PDF conversion is fully deterministic given the assembled HTML and CSS.
- **Output validation (Node 6):** file write, magic byte check, page count — all deterministic.

### Rationale
Following the same principle as RAA, AGA, SA, and Ingestion: LLM reasoning is applied only where interpretation or generation is required. The RGA requires no interpretation — all data is already structured by upstream agents. This makes the RGA fully reproducible with zero LLM token cost.

---

## 8) Checkpointing

### Purpose
The RGA is typically short-lived (3–20 seconds). The PDF rendering (Node 5) is the most expensive step. Checkpointing protects against crashes during this step, particularly for reports with many diagrams where HTML-to-PDF conversion may take several seconds.

### 8A — Checkpointer Configuration
Use `SqliteSaver` from `langgraph-checkpoint-sqlite`. The checkpoint database path is **received from the orchestrator at runtime** — the orchestrator passes a project-scoped path `projects/{project_name}/checkpoints/rga.db` when calling `compile_for_production(db_path=...)` (see Orchestrator Plan §6C). The RGA module's `compile_for_production()` accepts `db_path` as a **required parameter** with no default.

### 8B — Graph Compilation
Pass the checkpointer at compile time. LangGraph automatically persists state at every super-step boundary.

### 8C — Thread Identity & Run Configuration
Each RGA execution is identified by a `thread_id`:

```
thread_id = "rga-" + sha256(pipeline_run_id + rga_run_timestamp)[:16]
```

The `rga-` prefix distinguishes RGA checkpoint threads from other agents. The thread ID is passed via `{"configurable": {"thread_id": "<computed_id>"}}`.

### 8D — Resume Semantics
At startup, query the checkpointer for existing state. If a snapshot exists and `pdf_bytes` is already populated (Node 5 completed), skip directly to Node 6. If `insights_html` is populated but `pdf_bytes` is not, resume from Node 5. LangGraph handles replay automatically.

### 8E — Checkpoint Lifecycle
Checkpoint databases follow the same 7-day retention policy as other agents. After a successful run, the checkpoint is retained for debugging and traceability, then eligible for cleanup by the orchestrator.

### 8F — Failure Mode Coverage

| Failure | Checkpoint State | Recovery |
|---------|-----------------|----------|
| Process killed mid-insights-assembly (Node 4) | Checkpoint at Node 3 boundary. `static_sections` present, `insights_html` absent. | Resume: re-execute Node 4. Idempotent — deterministic. |
| Process killed mid-PDF-render (Node 5) | Checkpoint at Node 4 boundary. `insights_html` present, `pdf_bytes` absent. | Resume: re-execute Node 5. Idempotent — deterministic given HTML sections + insights. |
| Process killed mid-file-write (Node 6) | Checkpoint at Node 5 boundary. `pdf_bytes` present. | Resume: re-execute Node 6. File write is idempotent (overwrite). |
| Checkpoint DB corrupted | `SqliteSaver` raises on read. | Fatal — restart from scratch with new thread ID. |

---

## 9) Styling & Theming

### 9A — Colour Themes

The RGA supports three colour themes, selectable via `report_config.colour_theme`:

| Theme | Headings | Table Headers | Score Badge (A) | Score Badge (F) | Body Text |
|-------|----------|--------------|-----------------|-----------------|-----------|
| `default` | `#1a237e` (dark indigo) | `#283593` (indigo) | `#2e7d32` (green) | `#c62828` (red) | `#212121` (near-black) |
| `monochrome` | `#000000` | `#424242` | `#616161` | `#212121` | `#000000` |
| `dark` | `#90caf9` (light blue) | `#1565c0` (blue) | `#66bb6a` (green) | `#ef5350` (red) | `#e0e0e0` (light grey) |

The `dark` theme uses a dark page background (`#121212`) with light text. The `default` and `monochrome` themes use a white background.

### 9B — Typography

- **Headings:** System sans-serif font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif`). H1=18pt, H2=14pt, H3=12pt. Defined via CSS `h1`, `h2`, `h3` selectors.
- **Body text:** Same sans-serif stack, 10pt, `line-height: 1.4`.
- **Code blocks:** `"Courier New", Courier, monospace`, 8pt, light grey background via CSS `background-color`.
- **Table cells:** Same sans-serif stack, 9pt. Header row bold with coloured background via `thead th` CSS selector.
- **Captions:** Same sans-serif stack italic, 9pt, `text-align: center`.

> **Note on fonts:** WeasyPrint uses system fonts. The CSS font stack ensures broad compatibility across Linux, macOS, and Windows. No custom font files are bundled. If a specific font is required, it can be installed as a system font and referenced in the theme CSS.

### 9C — Page Layout

- **Margins:** Defined via CSS `@page` rule: `@page { margin: 2cm; }` (A4) or `@page { margin: 1in; }` (LETTER). The page size is set via `@page { size: A4; }` or `@page { size: letter; }`.
- **Header:** Report title (left) and current section name (right) rendered via `@page` margin boxes: `@top-left { content: "I-Architect Report"; }` and `@top-right { content: string(section-title); }`. Thin bottom border on the header area.
- **Footer:** Page number (centre) and `pipeline_run_id` (right) rendered via `@bottom-center { content: counter(page); }` and `@bottom-right { content: string(run-id); }`.
- **Section breaks:** Each major section `<section>` element uses `page-break-before: always` in the CSS.

### 9D — Grade Badge Rendering

The grade badge on the cover page is rendered as a CSS-styled `<div>`: circular shape via `border-radius: 50%`, diameter ~72pt (96px), letter grade centred inside via `display: flex; align-items: center; justify-content: center;` with 36pt bold white text. The numerical score is rendered below in a separate `<div>` with 14pt bold text. Colour is determined by grade via CSS classes: `.grade-a { background-color: #2e7d32; }`, `.grade-b { background-color: #1565c0; }`, etc. (exact hex values per theme).

### 9E — Chart Rendering

All charts (quality attribute bar chart, score composition bar, ASR/non-ASR breakdown, timing bar) are rendered as **CSS-styled HTML `<div>` elements** — no JavaScript charting library, no SVG generation. Each bar is a `<div>` with a percentage-based `width`, a solid `background-color` from the theme palette, and a text label inside or beside it. This approach is fully supported by WeasyPrint’s CSS rendering engine and produces clean, deterministic output.

### 9F — Table Cell Text Truncation

Long text values in table cells are truncated to prevent layout overflow and page breaks within a single row. The following truncation rules apply globally to all tables rendered by the RGA:

| Column Category | Max Characters | Truncation Indicator | Examples |
|----------------|---------------|---------------------|----------|
| Requirement text / description | 120 | `…` (ellipsis appended) | Orphaned requirements table (§5I), Full Requirement Listing appendix |
| Entity / pattern name | 60 | `…` | Pattern rationales table, open questions table |
| Error message / reason | 80 | `…` | Failed diagrams table, filtering report dropped reasons |
| LLM model name | 50 | `…` | LLM Configuration Overview table (§5C) |
| Generic identifier (IDs, paths) | 40 | `…` (truncate from the left, keeping the tail) | Diagram IDs, entity IDs, file paths |
| Numeric / short label | No limit | — | Scores, percentages, grades, counts |

**Implementation rules:**

1. Truncation is applied via a custom Jinja2 template filter (`truncate_text(value, max_chars)`) registered on the Jinja2 `Environment`. The filter is applied inline within HTML templates wherever long text values are rendered into table cells.
2. Truncation cuts at the last word boundary before the character limit, then appends `…` (U+2026). If no word boundary exists within the limit, hard-cut at the limit.
3. Appendix C (Full Requirement Listing) uses a wider column layout (single requirement per row, full page width) and applies the 120-character limit only to the table rendering. If `include_appendices` is true, this is the only place the full text could theoretically appear — but truncation still applies for layout safety.
4. The truncation limits are defined as constants in `reporting/styles/themes.py` alongside typography and colour definitions, so they can be overridden per-theme if needed.

---

## 10) Performance & Cost Profile

| Operation | Complexity / Cost |
|-----------|-------------------|
| Node 1 (data validation) | O(E + D) where E = entities, D = diagrams. No LLM cost. |
| Node 2 (section planning) | O(S) where S = section count (fixed at 14). No LLM cost. |
| Node 3 (content assembly) | O(R + D + G) where R = requirements, D = diagrams, G = gap items. No LLM cost. Dominated by diagram base64 encoding for large diagram counts. |
| Node 4 (deterministic insights) | O(1). No LLM cost — pure data extraction and template rendering. |
| Node 5 (PDF rendering) | O(H) where H = total HTML size. Dominated by WeasyPrint CSS layout and image embedding. |
| Node 6 (output validation) | O(1). No LLM cost. |
| **Total LLM calls** | **0 per RGA run** |
| **Wall-clock estimate** | ~3–20 seconds. WeasyPrint rendering with 8+ embedded PNGs is the bottleneck. |
| **Total RGA runs per pipeline** | 1 (RGA runs once after the final SA pass) |

---

## 11) Failure Modes & Mitigations

| Risk | Mitigation |
|------|------------|
| Upstream input missing or null | Node 1 validates all required fields at startup; raises `ReportInputError` with the specific missing field. Pipeline halts cleanly. |
| AGA produced zero completed diagrams | Diagrams section renders with placeholder boxes for each manifest entry. Report is still generated — it documents the failure. |
| Diagram PNG too large for page | `max_diagram_width_ratio` caps width via CSS `max-width`; aspect ratio preserved via `height: auto`. Very tall diagrams are scaled to fit page height minus margins. WeasyPrint handles pagination automatically. |
| WeasyPrint rendering fails | Catch `weasyprint.errors` exceptions, log the error with the offending HTML section context. If a specific section causes the failure, attempt to exclude it and re-render. Record skipped section in `RGAOutput`. |
| Output directory does not exist | Node 6 creates it via `os.makedirs(exist_ok=True)`. |
| Disk full during PDF write | `IOError` is caught. In-memory `pdf_bytes` remain in graph state for the orchestrator to retrieve. `RGAOutput.pdf_path` is set to null. |
| Process killed mid-render | SQLite checkpoint (§8) persists state after each node. Resume skips completed nodes. |
| `filter_report` is null (filtering was bypassed) | Appendix A is excluded from `section_plan`. No error raised. |
| `open_questions` is empty | Appendix B is excluded. Gap analysis "Open Questions" sub-table shows "No issues found". |
| Markdown in executive summary contains unsupported formatting | Convert markdown to HTML using Python `markdown` library which handles bold, italic, bullet lists, code spans. Unsupported elements are passed through as plain text. |
| WeasyPrint system library missing | At RGA startup (Node 1), verify WeasyPrint can be imported. If system libraries are missing, raise a clear error message listing the required packages (see §15). |

---

## 12) Validation & Testing Criteria

### Unit Tests

- **Node 1 validation:** provide inputs with a missing `sa_report.summary` field. Assert `ReportInputError` is raised with a message naming the missing field.
- **Node 2 section planning:** provide a null `filter_report`. Assert that `appendix_filter` section has `included = false`.
- **Node 2 section planning:** provide non-empty `open_questions`. Assert that `appendix_oq` section has `included = true`.
- **Node 3 cover page:** provide a `ReportConfig` with a valid `logo_path`. Assert the HTML fragment contains a `<img` tag with the base64-encoded logo.
- **Node 3 scoring table:** provide mocked `sa_report` with known axis scores. Assert the HTML fragment contains the correct values in `<td>` cells.
- **Node 3 diagram embedding:** provide 2 completed and 1 failed diagram. Assert the HTML fragment contains 2 `<img` tags with base64 data and 1 placeholder `<div>` with "Diagram generation failed".
- **Node 4 insights:** provide mocked upstream data. Assert `insights_html` contains the correct model statistics, top QA risks, and gap counts — all sourced from the input data, no fabrication.
- **Node 5 PDF validity:** build a minimal HTML document. Assert the rendered bytes start with `%PDF-`.
- **Node 6 output metadata:** assert `RGAOutput.page_count` is > 0 and `pdf_size_bytes` matches the file on disk.
- **Grade badge colour:** for each grade (A, B, C, D, F), assert the correct CSS class is applied in the HTML fragment.

### Integration Tests

- **End-to-end with synthetic data:** provide a complete mocked pipeline output (2 systems, 4 containers, 8 components, 8 diagrams, known SA scores). Assert the PDF is generated, file exists, page count ≥ 10, all 8 diagram images are embedded.
- **End-to-end with zero diagrams:** provide `aga_output` with all failed diagrams. Assert the PDF is still generated with placeholder boxes and the gap analysis section lists all failures.
- **End-to-end with filtering report:** provide a non-null `filter_report`. Assert Appendix A is included in the PDF and contains the dropped requirements table.

### Functional Tests

- **PDF structural integrity:** rendered file opens in a standard PDF reader (validated by PyPDF2 `PdfReader` without errors).
- **TOC correctness:** each section title in the TOC corresponds to a heading rendered in the PDF.
- **Diagram count:** `RGAOutput.diagrams_embedded` equals the count of `completed_diagrams` in `aga_output`.
- **Score consistency:** the total score displayed on the cover page badge, in the executive summary scorecard, and in the scoring section banner all match `sa_report.summary.total_score`.
- **No data fabrication:** every entity name, pattern name, and score value in the PDF is traceable to a specific field in the upstream inputs. No generated content appears anywhere — all content is deterministic template rendering.

---

## 13) Deliverables for Spec Kit

1. **State schema** — all channels, types, and reducers (§4), including `ReportConfig`, `PipelineMetadata`, `SectionSpec`, `SectionContent`, and `RGAOutput`.
2. **Node implementations** — six sequential nodes: data validation, section planning, content assembly, deterministic insights, PDF rendering, output validation (§6).
3. **PDF document structure** — section registry with conditional inclusion rules, layout specifications for each section (§5).
4. **Styling system** — three colour themes as CSS files, typography definitions, page layout via `@page` rules, grade badge rendering, chart rendering (§9).
5. **HTML template set** — Jinja2 base layout (`base.html`) and per-section partial templates in `reporting/templates/` (§14).
6. **CSS theme files** — `default.css`, `monochrome.css`, `dark.css` in `reporting/templates/css/` (§9A).
7. **Checkpointing configuration** — `SqliteSaver` setup with orchestrator-provided `db_path` (project-scoped per Orchestrator Plan §6C), thread ID derivation, resume semantics (§8).
8. **Project structure** — `reporting/` package layout with `templates/` subdirectory (§14).

---

## 14) Project Structure & Directory Layout

### 14A — Code & Template Directory (`reporting/`)

```
reporting/
├── __init__.py
├── runner.py                  # Entry point, checkpointer init, graph compilation
├── graph.py                   # StateGraph definition, edge wiring
├── state/
│   ├── __init__.py
│   └── schema.py              # RGAState TypedDict, ReportConfig, PipelineMetadata, SectionSpec, SectionContent, RGAOutput
├── nodes/
│   ├── __init__.py
│   ├── validation.py          # Node 1: Data Collection & Validation
│   ├── planning.py            # Node 2: Report Structure Planning
│   ├── assembly.py            # Node 3: Content Assembly (largest module — Jinja2 template rendering)
│   ├── insights.py            # Node 4: Deterministic Insights Assembly
│   ├── renderer.py            # Node 5: PDF Rendering (WeasyPrint HTML-to-PDF)
│   └── output.py              # Node 6: Output & Validation
├── templates/
│   ├── base.html              # Base layout: <html>, <head>, <body>, header/footer structure
│   ├── cover.html             # Cover page partial
│   ├── toc.html               # Table of contents partial
│   ├── llm_config.html        # LLM configuration overview partial
│   ├── timing.html            # Subgraph execution timing partial
│   ├── exec_summary.html      # Executive summary partial
│   ├── req_table.html         # Requirements overview partial
│   ├── scoring.html           # Scoring report partial
│   ├── diagrams.html          # Architecture diagrams partial
│   ├── gap_analysis.html      # Gap analysis partial
│   ├── insights.html          # Architectural insights partial
│   ├── appendix_filter.html   # Appendix A: Filtering report partial
│   ├── appendix_oq.html       # Appendix B: Open questions partial
│   ├── appendix_reqs.html     # Appendix C: Full requirement listing partial
│   ├── appendix_patterns.html # Appendix D: Pattern rationales partial
│   └── css/
│       ├── default.css        # Default colour theme (white background, indigo headings)
│       ├── monochrome.css     # Monochrome theme (black/grey)
│       └── dark.css           # Dark theme (dark background, light text)
├── styles/
│   ├── __init__.py
│   └── themes.py              # Theme selection logic, truncation limit constants, grade badge colour mappings
└── utils/
    ├── __init__.py
    ├── filters.py             # Custom Jinja2 filters: truncate_text, format_percentage, markdown_to_html
    └── images.py              # Diagram PNG-to-base64 encoding, aspect ratio calculation
```

### 14B — Skills Resource Bundle

The RGA has no LLM calls and therefore **no skill resource bundle**. No `Skills/Reporting/` directory is created. This is consistent with the RGA’s fully deterministic design.

### 14C — Checkpoint Storage

Checkpoint databases are **project-scoped** (per Orchestrator Plan §6C). The orchestrator creates and manages the directory at `projects/{project_name}/checkpoints/` and passes the full path to each agent's `compile_for_production(db_path=...)` call:

```
projects/{project_name}/checkpoints/
├── orchestrator.db           # Orchestrator's own checkpoint
├── ingestion.db              # Ingestion pipeline checkpoints
├── arlo.db                   # ARLO checkpoints
├── raa_graph.db              # RAA checkpoints
├── aga.db                    # AGA checkpoints
├── sa.db                     # SA checkpoints
└── rga.db                    # RGA checkpoints
```

The RGA module does **not** create or assume a shared `checkpoints/` directory at the project root. Directory creation is the orchestrator's responsibility.

### 14D — Convention

The `reporting/templates/` subdirectory stores all Jinja2 HTML templates and CSS stylesheets. This replaces the `prompts/` convention used by other agents (e.g., `arlo/prompts/`, `raa/prompts/`) because the RGA has no LLM prompts — only rendering templates. The separation of templates (HTML/CSS) from code (Python) follows standard web development conventions.

---

## 15) Dependencies

| Package | Purpose | Version Constraint |
|---------|---------|-------------------|
| `weasyprint` | HTML/CSS-to-PDF rendering engine. Converts the assembled Jinja2 HTML document into a paginated PDF with full CSS print media support (`@page` rules, margin boxes, page breaks). | `>=60.0` |
| `Jinja2` | Template engine for rendering HTML section fragments from upstream data. Used for base layout, per-section partials, and custom filters (truncation, formatting). | `>=3.1.0` |
| `markdown` | Converts SA executive summary markdown to HTML for embedding in the Jinja2 templates. | `>=3.5.0` |
| `PyPDF2` | Post-render page count validation and PDF integrity check | `>=3.0.0` |
| `Pillow` | PNG image processing for diagram aspect ratio calculation before base64 embedding | `>=10.0.0` |
| `pydantic` | Structured data models (`ReportConfig`, `PipelineMetadata`, `RGAOutput`) | Already in project |
| `langgraph` | `StateGraph` API for sequential node execution | Already in project |
| `langgraph-checkpoint-sqlite` | `SqliteSaver` for checkpoint persistence (path provided by orchestrator at runtime per §6C) | Already in project |

> **Note on WeasyPrint system dependencies:** WeasyPrint requires certain system-level libraries to be installed: `libpango`, `libcairo`, `libgdk-pixbuf`, and `libffi`. On Ubuntu/Debian: `sudo apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libcairo2 libffi-dev`. On macOS: `brew install pango cairo gdk-pixbuf libffi`. These are documented in the [WeasyPrint installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation).

---

## 16) Open Design Decisions

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| 1 | Should the report include a watermark for draft/regenerated runs? | (a) No watermark, (b) "DRAFT" watermark on regeneration runs, (c) Configurable | **(c) Configurable** — add `watermark_text: str | null` to `ReportConfig`. Default null (no watermark). Implemented via a CSS pseudo-element overlay. |
| 2 | Should the PlantUML source code be included by default? | (a) Always include, (b) Never include, (c) Configurable | **(c) Configurable** — `include_plantuml_source` defaults to `false` to keep report compact. |
| 3 | Should the report support multi-file input (multiple ingestion runs)? | (a) Single pipeline run per report, (b) Comparative multi-run report | **(a) Single run** for v1. Comparative reports can be added in a future version. |
| 4 | Should the RGA produce additional output formats (HTML, DOCX)? | (a) PDF only, (b) PDF + HTML, (c) PDF + DOCX | **(a) PDF only** for v1. However, since the intermediate format is already HTML, producing a standalone HTML report is trivially achievable by saving the assembled HTML string before WeasyPrint conversion. This can be added as a low-cost option in v2. |
