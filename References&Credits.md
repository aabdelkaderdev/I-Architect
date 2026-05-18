# I-Architect — References & Credits

> **Project:** I-Architect — Generative AI for Software Engineering Architecture Diagrams  
> **Version:** 1.0  
> **Pipeline:** ARLO → RAA → AGA (Architectural Reasoning via LangGraph Orchestration)

---

## Table of Contents

1. [Core Frameworks & Libraries](#1-core-frameworks--libraries)
2. [Embedding Model](#2-embedding-model)
3. [Machine Learning & Scientific Computing](#3-machine-learning--scientific-computing)
4. [Optimization Solver](#4-optimization-solver)
5. [Template Engine](#5-template-engine)
6. [Diagram Generation & Rendering](#6-diagram-generation--rendering)
7. [Architecture Evaluation Methodologies](#7-architecture-evaluation-methodologies)
8. [Architecture Modelling Standards](#8-architecture-modelling-standards)
9. [Datasets](#9-datasets)
10. [Build & Packaging Tools](#10-build--packaging-tools)
11. [Testing Frameworks](#11-testing-frameworks)
12. [Utility Tools](#12-utility-tools)
13. [Runtime & Language](#13-runtime--language)
14. [Academic & Research References](#14-academic--research-references)
15. [Third-Party Skills & Plugins](#15-third-party-skills--plugins)

---

## 1. Core Frameworks & Libraries

### LangGraph

- **Package:** `langgraph==1.2.0`
- **Author:** LangChain, Inc.
- **License:** MIT
- **Repository:** <https://github.com/langchain-ai/langgraph>
- **Documentation:** <https://langchain-ai.github.io/langgraph/>
- **Usage:** Core orchestration framework for the ARLO pipeline. Provides `StateGraph`, `Send` API for parallel fan-out of concern workers, `@task` for durable checkpointing, private-state channels via `add_sequence`, and conditional edges for graph routing. All three experiment graphs (BasicArlo, InfluentialSets, VaryingRequirements) are built on LangGraph's state machine model.

### LangChain

- **Package:** `langchain==1.3.0`
- **Author:** LangChain, Inc.
- **License:** MIT
- **Repository:** <https://github.com/langchain-ai/langchain>
- **Documentation:** <https://docs.langchain.com>
- **Usage:** Provides LLM abstraction (`ChatOpenAI` and compatible models), structured output parsing via `llm.with_structured_output()`, `HumanMessage` / `SystemMessage` message types, and `RunnableConfig` for parent pipeline integration.

### LangGraph Checkpoint — SQLite

- **Package:** `langgraph-checkpoint-sqlite==3.0.3`
- **Author:** LangChain, Inc.
- **License:** MIT
- **Repository:** <https://github.com/langchain-ai/langgraph>
- **Usage:** SQLite-based persistence backend for crash-resilient checkpointing of ARLO graph state in production. Enables resume-from-checkpoint after process restarts without re-executing completed nodes or `@task` batches.

### Pydantic

- **Package:** `pydantic==2.13.0`
- **Author:** Samuel Colvin and contributors
- **License:** MIT
- **Repository:** <https://github.com/pydantic/pydantic>
- **Documentation:** <https://docs.pydantic.dev>
- **Usage:** Defines structured LLM output models (`ParsedRequirement`, `ParsedBatch`, `SatGroup`, `MetricTrigger`, `EquivalenceResult`) used with LangChain's `with_structured_output()` to enforce schema compliance in LLM responses. Also used for data validation throughout the pipeline.

### python-dotenv

- **Package:** `python-dotenv==1.2.2`
- **Author:** Saurabh Kumar and contributors
- **License:** BSD-3-Clause
- **Repository:** <https://github.com/theskumar/python-dotenv>
- **Usage:** Environment variable management for API keys and configuration (e.g., LLM endpoint URLs, API keys for OpenAI-compatible providers).

### PySide6

- **Package:** `PySide6`
- **Author:** The Qt Company
- **License:** LGPL-3.0 / GPL-2.0 / Commercial
- **Repository:** <https://code.qt.io/cgit/pyside/pyside-setup.git/>
- **Documentation:** <https://doc.qt.io/qtforpython-6/>
- **Usage:** Qt for Python bindings providing the core desktop application framework. Supplies the main window shell, layout managers, signal/slot event system, `QThread` concurrency for pipeline execution, `QStackedWidget` for view swapping, and `QWebEngineView` for the embedded Monaco editor in the AGA view.

### QFluentWidgets (PyQt-Fluent-Widgets)

- **Package:** `PySide6-Fluent-Widgets`
- **Author:** zhiyiYo
- **License:** GPLv3 (non-commercial); Commercial license required for commercial distribution — <https://qfluentwidgets.com/price>
- **Repository:** <https://github.com/zhiyiYo/PyQt-Fluent-Widgets>
- **Documentation:** <https://qfluentwidgets.com>
- **Usage:** Fluent Design widget library for PySide6 providing all primary UI components: `FluentWindow` (frameless window chrome with navigation panel), `CardWidget`/`ElevatedCardWidget` (content cards), `TableWidget` (data grids), `ComboBox`, `LineEdit`, `PasswordLineEdit`, `SpinBox`, `Slider`, `ProgressBar`, `SwitchButton`, `MessageBox`/`MessageBoxBase` (dialogs), `InfoBar` (toast notifications), `InfoBadge` (status badges), `Pivot`/`TabWidget` (tabbed views), and built-in light/dark theme support via `setTheme()`.

---

## 2. Embedding Model

### mixedbread-ai/mxbai-embed-large-v1

- **Model Name:** `mixedbread-ai/mxbai-embed-large-v1`
- **Author:** Mixedbread AI (mixedbread.ai)
- **Dimensions:** 1024
- **License:** Apache-2.0
- **Hugging Face:** <https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1>
- **Paper:** Li et al., "AnglE-optimized Text Embeddings," arXiv:2309.12871, 2024.
- **Usage:** Dense semantic embeddings for ASR condition texts. Runs locally on CPU via FastEmbed. Embedded vectors drive K-Means clustering for condition-group formation and are reused as batch anchors for ANN search in the RAA pipeline. Model files are cached in `arlo/models/` on first run.

### FastEmbed

- **Package:** `fastembed==0.8.0`
- **Author:** Qdrant
- **License:** Apache-2.0
- **Repository:** <https://github.com/qdrant/fastembed>
- **Documentation:** <https://qdrant.github.io/fastembed/>
- **Usage:** Lightweight, CPU-optimized embedding inference runtime. Wraps the mxbai-embed-large-v1 ONNX model for local embedding generation without GPU dependencies or external API calls. Provides the `TextEmbedding` class used in the embedding node.

---

## 3. Machine Learning & Scientific Computing

### scikit-learn

- **Package:** `scikit-learn==1.8.0`
- **Author:** scikit-learn developers (F. Pedregosa, G. Varoquaux, A. Gramfort, et al.)
- **License:** BSD-3-Clause
- **Repository:** <https://github.com/scikit-learn/scikit-learn>
- **Documentation:** <https://scikit-learn.org>
- **Citation:** Pedregosa, F., Varoquaux, G., Gramfort, A., et al. "Scikit-learn: Machine Learning in Python." *Journal of Machine Learning Research*, 12, pp. 2825–2830, 2011.
- **Usage:** Provides `KMeans` clustering algorithm for grouping ASR embeddings by condition similarity. Used with `random_state=42` for reproducibility. The elbow method (WCSS sweep from `n//10` to `n//5`) determines optimal cluster count.

### NumPy

- **Dependency of:** scikit-learn, FastEmbed
- **Author:** NumPy Developers
- **License:** BSD-3-Clause
- **Repository:** <https://github.com/numpy/numpy>
- **Usage:** Array operations for embedding vectors, WCSS computation, and K-Means data preparation.

---

## 4. Optimization Solver

### Python-MIP (Mixed Integer Programming)

- **Package:** `mip>=1.17`
- **Author:** Haroldo Gambini Santos, Túlio A. M. Toffolo, et al.
- **License:** EPL-2.0
- **Repository:** <https://github.com/coin-or/python-mip>
- **Documentation:** <https://www.python-mip.com>
- **Citation:** Santos, H. G., Toffolo, T. A. M. "Mixed Integer Linear Programming with Python." *Journal of Open Source Software*, 5(48), 2366, 2020.
- **Usage:** Integer Linear Programming (ILP) optimizer for architectural pattern selection. Maximizes weighted quality-attribute coverage subject to one-per-group constraints. Used as the default optimizer (`optimizer="ILP"`) in the concern worker. An alternative greedy optimizer is also provided for comparison experiments.

---

## 5. Template Engine

### Chevron (Mustache for Python)

- **Package:** `chevron==0.14`
- **Author:** Noah Morales (noahmorales)
- **License:** MIT
- **Repository:** <https://github.com/noahmorales/chevron>
- **Usage:** Mustache template rendering engine for LLM prompt construction. Loads `.md` template files from `arlo/prompts/` and renders them with dynamic context (requirement lists, quality attribute definitions, condition texts). Supports conditional sections (`{{#stringent}}`/`{{^stringent}}`) for mode-dependent prompt variations.

### Mustache Specification

- **Specification:** <https://mustache.github.io/mustache.5.html>
- **Usage:** The prompt templates (`asr_classification.md`, `condition_equivalence.md`, `satisfiable_grouping.md`, `metric_extraction.md`) conform to the Mustache specification for logic-less templates.

---

## 6. Diagram Generation & Rendering

### PlantUML

- **Author:** Arnaud Roques
- **License:** GPL-2.0 / LGPL / Apache-2.0 / MIT (multiple licenses)
- **Website:** <https://plantuml.com>
- **Server:** <http://www.plantuml.com/plantuml>
- **Repository:** <https://github.com/plantuml/plantuml>
- **Usage:** Server-side rendering engine for architecture diagrams in the AGA (Architecture Generation Agent). The agent generates PlantUML source code, encodes it via the `planturl` binary, submits it to the PlantUML server, and receives rendered PNG diagrams.

### C4-PlantUML Library

- **Author:** Adrian Voß (plantuml-stdlib)
- **License:** MIT
- **Repository:** <https://github.com/plantuml-stdlib/C4-PlantUML>
- **Usage:** PlantUML macro library for C4 model diagrams. Provides element macros (`Person`, `System`, `Container`, `Component`, `System_Ext`), boundary grouping (`System_Boundary`, `Container_Boundary`), relationship macros (`Rel`, `Rel_D`, `Rel_U`, `Rel_L`, `Rel_R`), and layout utilities (`LAYOUT_WITH_LEGEND()`). Referenced in the AGA's code-generation skill and normative constraints.

### planturl (PlantUML URL Encoder)

- **Author:** migmedia (Micha Glave)
- **Language:** Rust
- **License:** MIT
- **Repository:** <https://github.com/migmedia/planturl>
- **Location:** `tools/planturl/Bin/` (precompiled binaries for 5 OS/architecture targets)
- **Supported Targets:**
  - `aarch64-apple-darwin` — macOS on Apple Silicon
  - `apple-darwin` — macOS on Intel x86_64
  - `linux-gnu` — Linux with glibc
  - `linux-musl` — Linux with musl libc (Alpine, static environments)
  - `windows-msvc` — Windows
- **Usage:** Local binary tool for encoding PlantUML source code into compressed URL strings compatible with the PlantUML server's `/png/` and `/svg/` endpoints. Used by the `encode_plantuml` tool in the AGA.

---

## 7. Architecture Evaluation Methodologies

### SAAM (Software Architecture Analysis Method)

- **Authors:** Rick Kazman, Len Bass, Gregory Abowd, Mike Webb
- **Institution:** Carnegie Mellon University, Software Engineering Institute (SEI)
- **Year:** 1994
- **Citation:** Kazman, R., Bass, L., Abowd, G., Webb, M. "SAAM: A Method for Analyzing the Properties of Software Architectures." *Proceedings of the 16th International Conference on Software Engineering (ICSE '94)*, pp. 81–90, IEEE, 1994.
- **SEI Technical Report:** <https://sei.cmu.edu/documents/150/2007_019_001_29297.pdf>
- **SEI Library:** <https://www.sei.cmu.edu/library/saam-a-method-for-analyzing-the-properties-of-software-architectures/>
- **Usage:** The 5-step SAAM evaluation process is applied in the RAA Judge Node for scoring and ranking parallel RAA subgraph outputs. SAAM scenario coverage, weighted by ARLO quality weights, drives the merge algorithm for selecting the best architectural fragment per batch. A full SAAM Analysis Skill is implemented for post-generation evaluation of C4 diagrams against requirements.

### SAAM Five-Step Process (as applied)

1. Canonical partitioning of the architecture
2. Map requirements to architectural structures
3. Choose quality attributes (informed by ARLO quality weights)
4. Define evaluation scenarios per quality attribute
5. Evaluate architectural structures against scenarios

---

## 8. Architecture Modelling Standards

### C4 Model

- **Author:** Simon Brown
- **License:** Creative Commons Attribution 4.0
- **Website:** <https://c4model.com>
- **Diagrams Reference:** <https://c4model.com/diagrams>
- **Notation Reference:** <https://c4model.com/diagrams/notation>
- **Usage:** The C4 model's four-level abstraction (Context, Container, Component, Code) is the target output schema for the RAA and the rendering framework for the AGA. All architectural entities carry C4-compliant type labels, descriptions, technology annotations, and directed relationships.

### ISO/IEC 25010 (Software Quality Attributes)

- **Standard:** ISO/IEC 25010:2011 — Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE)
- **Publisher:** International Organization for Standardization (ISO)
- **Usage:** The eight quality attributes used in ASR classification and quality-weight inference are derived from ISO/IEC 25010:
  - Performance Efficiency
  - Compatibility
  - Usability
  - Reliability
  - Security
  - Maintainability
  - Portability
  - Cost Efficiency (project-specific extension)

---

## 9. Datasets

### PROMISE NFR Dataset

- **File:** `data/KaggleReq.json` (555 requirements, `REQ-1` through `REQ-555`)
- **Author:** Jane Cleland-Huang (<jhuang@cti.depaul.edu>)
- **Institution:** DePaul University, College of Computing and Digital Media
- **Year:** 2007
- **Source:** PROMISE Software Engineering Repository — `nfr` relation
- **Repository:** <http://promisedata.org/repository>
- **License:** Creative Commons Attribution-Share Alike 3.0 (CC BY-SA 3.0) — <http://creativecommons.org/licenses/by-sa/3.0/>
- **Source Format:** Originally in PROMISE/ARFF plain-text format (`requirements_examples/KaggleReq.txt`), converted to JSON via `requirements_examples/convert_to_json.sh`
- **Domain:** Mixed — includes requirements from dispatch systems, dispute management systems, insurance collision estimating, conference room reservation systems, movie streaming platforms, lead management systems, battleship games, teleservicing scheduling, nursing program management, real estate MLS systems, budget forecasting systems, and fantasy football applications.
- **Citation:** Cleland-Huang, J. "Non-Functional Requirements (NFR) Dataset." *PROMISE Software Engineering Repository*, 2007. Available at: <http://promisedata.org/repository>
- **Acknowledgment:** This dataset is made publicly available by the PROMISE Software Engineering Repository to encourage repeatable, verifiable, refutable, and/or improvable predictive models of software engineering.
- **Usage:** Large-scale evaluation dataset for testing ARLO pipeline scalability and ASR classification across diverse requirement domains.

### Custom Requirements Dataset

- **File:** `data/requirements.json` (30 requirements, `R1` through `R30`)
- **Domain:** Law enforcement dispatch and field operations system
- **Usage:** Primary development and integration testing dataset. Contains requirements spanning all eight quality attributes with diverse condition texts for clustering and grouping validation.

### Quality-Architecture Pattern Matrix

- **File:** `data/matrix.json`
- **Content:** 16 architectural patterns × 8 quality attributes, with integer scores (−1, 0, +1)
- **Patterns:** Monolith, Microservices, Peer-to-Peer, Always On, Offline First, API-Call, Message-Based, WebSocket, Central, Hot-Hot, Hot-Cold, SQL, NoSQL, Proactive, Reactive, Real-time Sync, Batch Processing
- **Quality Attributes:** Performance Efficiency, Compatibility, Usability, Reliability, Security, Maintainability, Portability, Cost Efficiency
- **Usage:** Input to the ILP and Greedy optimizers for architectural pattern selection. Defines the trade-off space between quality attributes and candidate patterns.

---

## 10. Build & Packaging Tools

### setuptools

- **Package:** `setuptools>=75.0`
- **Author:** Python Packaging Authority (PyPA)
- **License:** MIT
- **Repository:** <https://github.com/pypa/setuptools>
- **Usage:** Build backend specified in `pyproject.toml` for packaging the `arlo` Python package.

### uv

- **Author:** Astral (Charlie Marsh et al.)
- **License:** Apache-2.0 / MIT
- **Repository:** <https://github.com/astral-sh/uv>
- **Usage:** Fast Python package installer and resolver. Used for dependency management (`uv.lock`).

### gdown

- **Author:** Kentaro Wada
- **License:** MIT
- **Repository:** <https://github.com/wkentaro/gdown>
- **Usage:** Google Drive file downloader used in `download_model.sh` and `download_model.bat` to fetch the pre-trained embedding model archive (`models.7z`).

### 7-Zip / p7zip

- **Author:** Igor Pavlov
- **License:** LGPL-2.1 / BSD-3-Clause (unRAR)
- **Website:** <https://www.7-zip.org>
- **Usage:** Archive extraction tool for the `models.7z` embedding model package.

---

## 11. Testing Frameworks

### pytest

- **Package:** `pytest>=8.2`
- **Author:** Holger Krekel and pytest contributors
- **License:** MIT
- **Repository:** <https://github.com/pytest-dev/pytest>
- **Usage:** Unit and integration testing framework for the ARLO pipeline.

### pytest-asyncio

- **Package:** `pytest-asyncio>=0.25`
- **Author:** pytest-asyncio contributors
- **License:** Apache-2.0
- **Repository:** <https://github.com/pytest-dev/pytest-asyncio>
- **Usage:** Async test support for LangGraph and LangChain async invocations.

---

## 12. Utility Tools

### SQLite

- **Author:** D. Richard Hipp
- **License:** Public Domain
- **Website:** <https://www.sqlite.org>
- **Usage:** Embedded database for LangGraph checkpoint persistence in production mode (`checkpoints/arlo.db`). Accessed via Python's `sqlite3` standard library module with `check_same_thread=False` for concurrent fan-out checkpointing.

---

## 13. Runtime & Language

### Python

- **Required Version:** `>=3.11`
- **Author:** Python Software Foundation
- **License:** PSF License
- **Website:** <https://www.python.org>
- **Usage:** Primary implementation language for the entire ARLO pipeline.

---

## 14. Academic & Research References

### Architecture-Related

| # | Reference | Relevance |
|---|-----------|-----------|
| 1 | Kazman, R., Bass, L., Abowd, G., Webb, M. "SAAM: A Method for Analyzing the Properties of Software Architectures." *ICSE '94*, pp. 81–90, IEEE, 1994. | SAAM methodology used in Judge node scoring and SAAM Analysis Skill |
| 2 | Brown, S. "The C4 Model for Visualising Software Architecture." <https://c4model.com>, 2018–present. | C4 modelling standard — target output schema for RAA and AGA |
| 3 | Bass, L., Clements, P., Kazman, R. *Software Architecture in Practice*, 4th ed. Addison-Wesley, 2021. | Foundational reference for quality attributes, architectural tactics, and evaluation methods |
| 4 | ISO/IEC 25010:2011. "Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models." ISO, 2011. | Quality attribute taxonomy used in ASR classification |
| 5 | IEEE 830 — Recommended Practice for Software Requirements Specifications. <https://standards.ieee.org/standard/830-1998.html> | Requirement characteristics: clear, complete, consistent, verifiable, traceable. Used for the Signal_Noise_Taxonomy.md skill. |

### Machine Learning & NLP

| # | Reference | Relevance |
|---|-----------|-----------|
| 5 | Li, X., et al. "AnglE-optimized Text Embeddings." *arXiv:2309.12871*, 2024. | Underlying methodology for the mxbai-embed-large-v1 embedding model |
| 6 | Pedregosa, F., et al. "Scikit-learn: Machine Learning in Python." *JMLR*, 12, pp. 2825–2830, 2011. | K-Means clustering implementation for condition-group formation |
| 7 | Santos, H. G., Toffolo, T. A. M. "Mixed Integer Linear Programming with Python." *JOSS*, 5(48), 2366, 2020. | python-mip library for ILP architectural pattern optimization |

### LLM & Agent Frameworks

| # | Reference | Relevance |
|---|-----------|-----------|
| 8 | LangChain, Inc. "LangGraph: Build resilient language agents as graphs." <https://github.com/langchain-ai/langgraph>, 2024–present. | Core orchestration framework for the ARLO pipeline |
| 9 | LangChain, Inc. "LangChain: Build context-aware reasoning applications." <https://github.com/langchain-ai/langchain>, 2022–present. | LLM abstraction layer and structured output parsing |

---

## 15. Third-Party Skills & Plugins

### PlantUML Syntax — Claude Code Skill

- **Author:** Kyle Sexton (kyle-sexton) / Melodic Software
- **License:** See repository
- **Repository:** <https://github.com/melodic-software/claude-code-plugins/tree/main/plugins/visualization/skills/plantuml-syntax>
- **Usage:** PlantUML syntax skill adapted for the AGA (Architecture Generation Agent). Provides C4 diagram syntax reference, element macros, and rendering conventions used in C4 PlantUML code generation within the I-Architect LangGraph pipeline.

---

## License Summary

| Component | License |
|-----------|---------|
| LangGraph | MIT |
| LangChain | MIT |
| langgraph-checkpoint-sqlite | MIT |
| Pydantic | MIT |
| python-dotenv | BSD-3-Clause |
| FastEmbed | Apache-2.0 |
| mxbai-embed-large-v1 (model) | Apache-2.0 |
| scikit-learn | BSD-3-Clause |
| NumPy | BSD-3-Clause |
| Python-MIP | EPL-2.0 |
| Chevron | MIT |
| PlantUML | GPL-2.0 / LGPL / Apache / MIT |
| C4-PlantUML | MIT |
| setuptools | MIT |
| uv | Apache-2.0 / MIT |
| gdown | MIT |
| 7-Zip | LGPL-2.1 |
| pytest | MIT |
| pytest-asyncio | Apache-2.0 |
| SQLite | Public Domain |
| PySide6 | LGPL-3.0 / GPL-2.0 / Commercial |
| QFluentWidgets | GPLv3 (non-commercial) / Commercial |
| Python | PSF License |

---

*Document generated for the I-Architect graduation project.*  
*Last updated: 2026-05-15*
