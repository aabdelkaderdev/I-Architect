# Phase 2 — Tools

> **Goal:** Build the three LangChain `@tool` utilities that the ReAct agent will use: OS/architecture detection for binary resolution, PlantUML encoding via the `planturl` binary, and PNG fetching with SVG-based error detection.
>
> **Depends on:** Phase 1 (folder scaffold, `__init__.py` files exist)
> **Produces:** `aga/tools/os_detection.py`, `aga/tools/encode_plantuml.py`, `aga/tools/fetch_plantuml_png.py`, `aga/tools/__init__.py`
> **Test fixture:** `arch_model_test_result-1.json`

---

## 10) Tools Specification

### 10A — `encode_plantuml`

| Attribute | Value |
|-----------|-------|
| **Signature** | `encode_plantuml(puml_code: str) → str` |
| **Behaviour** | Write code to temp `.puml` file → invoke planturl binary → return encoded URL |
| **Binary Args** | `-s <tmpfile> -u <server_url> -t png -c deflate` |
| **Error Surface** | `EncodingException` on non-zero exit; `IOError` on temp file failure |

### 10B — `fetch_plantuml_png`

| Attribute | Value |
|-----------|-------|
| **Signature** | `fetch_plantuml_png(encoded_url: str) → PngResult \| PlantumlErrorRecord` |
| **Step 1** | HEAD pre-check to server base URL (3s timeout) |
| **Step 2** | GET request to encoded URL (30s timeout) |
| **Step 3** | SVG-based error detection (substitute `/png/` with `/svg/`, parse for error strings) |
| **Transient Retries** | 2 retries with exponential backoff for network errors |

### 10C — OS Detection

| OS | Architecture | Binary Path |
|----|-------------|-------------|
| Windows | any | `tools/planturl/Bin/windows-msvc/planturl.exe` |
| macOS | ARM64 | `tools/planturl/Bin/aarch64-apple-darwin/planturl` |
| macOS | x86_64 | `tools/planturl/Bin/apple-darwin/planturl` |
| Linux | glibc | `tools/planturl/Bin/linux-gnu/planturl` |
| Linux | musl | `tools/planturl/Bin/linux-musl/planturl` |

---

## 7C — Tool Definitions (LangChain @tool)

Two LangChain-native tools are bound to the ReAct agent:

1. **`encode_plantuml`** — Wraps the planturl binary invocation
2. **`fetch_plantuml_png`** — HTTP fetch with SVG-based error detection

---

## Relevant Validation Criteria (from §15)

### Unit Tests
- OS detection returns correct binary path for all 5 targets
- `encode_plantuml` produces non-empty URL for valid input
- `fetch_plantuml_png` classifies SVG error responses correctly
