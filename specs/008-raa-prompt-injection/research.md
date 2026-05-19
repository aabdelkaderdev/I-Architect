# Research Report: Dynamic Excerpt Caching and Registry Design

This report documents caching and design decisions for prompt constraint injection.

## 1. Excerpt I/O Caching

### Decision
Store loaded prompt excerpts in an in-memory cache dict inside `raa/utils/prompts.py` using standard python decorators (e.g. `functools.lru_cache`).

### Rationale
During pipeline execution, multiple subgraphs (such as RAA-A, RAA-B, RAA-C) will call the prompt loader concurrently. Reading files from disk on every invocation introduces unnecessary I/O. In-memory caching ensures files are read once and served instantly thereafter.

### Alternatives Considered
- **Direct File Reads without caching**: Rejected because it increases disk I/O and could fail under high-concurrency file access.

---

## 2. Tag Registry Design

### Decision
Explicitly define the node-to-tag mapping in Python as a static constant dict inside the utility module.

### Rationale
Hardcoding the mapping registry guarantees alignment with the RAA Plan Section 21C, preventing runtime typos or configurations from requesting wrong/incomplete constraints.
