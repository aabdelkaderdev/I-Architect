# Data Model: RAA Prompt Resource Bundle

This document describes the structure and schemas of the prompt resource bundle files.

## 1. Prompt File Definitions

### source_register.md
A Markdown table with the following structure:
- `Source`: Text name of the authoritative document.
- `URL`: HTTPS/FTP location of the source document.
- `Retrieval Date`: Date on which the document content was fetched and parsed.
- `Governs`: List of pipeline components or rules governed by this source.

### c4_constraints.md & saam_constraints.md
Standard markdown documents detailing rules for:
- **C4**: Three C4 levels (Context, Container, Component), element types, description fields, parent system/container links, technology stack annotations, and relationship descriptions.
- **SAAM**: The 5 sequential steps of the Architecture Analysis Method.

---

## 2. Excerpt Mapping Matrix

The retrieval policy maps tags to specific text files in the `raa/prompts/excerpts/` directory:

| Tag | Filename | Description | Word Limit |
|-----|----------|-------------|------------|
| `c4:levels` | `c4_levels.txt` | C4 context/container/component level definitions | ≤25 words |
| `c4:notation` | `c4_notation.txt` | C4 element labeling and relationship notation | ≤25 words |
| `c4:technology` | `c4_technology.txt` | C4 technology annotation requirement | ≤25 words |
| `saam:steps` | `saam_steps.txt` | Summary of the 5 SAAM evaluation steps | ≤25 words |
| `saam:scenarios` | `saam_scenarios.txt` | Guidance for selecting test scenarios | ≤25 words |
