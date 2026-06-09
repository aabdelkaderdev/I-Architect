# Product Requirements Document
## Architecture Generation Agent (AGA) — Phase 4: LangGraph Tool Adapter for `render_plantuml`
**Version:** 1.0
**Status:** Draft
**Scope:** A single `@tool`-decorated function that wraps `render_plantuml` from `aga/tools/planturl_render.py` for use by the LangGraph ReAct agent. Covers the adapter's interface, the temp-file lifecycle, error surfacing contract, and how the tool is registered with the agent.

---

## 1. Overview

The existing `render_plantuml` function in `aga/tools/planturl_render.py` operates on **file paths**: it reads a `.puml` source file from disk and writes the rendered output to a destination path. The ReAct agent, however, works with **in-memory strings**: the LLM produces PlantUML code as text and the agent must render it without an explicit file management step.

This phase bridges that gap by defining a `@tool`-decorated adapter that:

1. Accepts a PlantUML **code string** and an output path string.
2. Writes the code to a named temporary file.
3. Delegates to `render_plantuml`.
4. Cleans up the temp file.
5. Returns either a success payload or a structured error string that the agent can reason about.

---

## 2. Files Created in This Phase

| File | Purpose |
|------|---------|
| `aga/tools/render_tool.py` | `render_plantuml_tool` — the `@tool`-decorated LangGraph adapter |

`aga/tools/planturl_render.py` is **not modified**. It is used as an import-only dependency.

---

## 3. `aga/tools/render_tool.py`

### 3.1 Tool Signature

```python
from langchain_core.tools import tool

@tool
def render_plantuml_tool(
    puml_code: str,
    output_path: str,
    output_type: str = "png",
    base_url: str = "https://www.plantuml.com/plantuml",
) -> str:
    """
    Render a PlantUML diagram from a source code string.

    Writes the PlantUML source to a temporary file, invokes the planturl
    binary to render it via the PlantUML server, saves the result to
    output_path, and returns a result string.

    Parameters
    ----------
    puml_code : str
        Complete PlantUML source code, starting with @startuml and ending
        with @enduml.
    output_path : str
        Destination file path for the rendered image. The parent directory
        must already exist.
    output_type : str
        Image format: 'png', 'svg', or 'ascii'. Defaults to 'png'.
    base_url : str
        Base URL of the PlantUML rendering server.

    Returns
    -------
    str
        On success: "OK:{output_path}" — the agent parses the prefix to
        detect success and the path to record in CompletedDiagram.
        On failure: "ERROR:{error_message}" — the agent parses the prefix
        to enter the correction loop.
    """
```

### 3.2 Return Value Protocol

The tool returns a plain `str` in one of two formats:

| Prefix | Meaning | Agent action |
|--------|---------|-------------|
| `"OK:{path}"` | Rendering succeeded; PNG is at `path` | Record as `CompletedDiagram`, advance queue |
| `"ERROR:{message}"` | Rendering failed; `message` is human-readable | Agent may correct and retry while within the per-diagram render attempt limit |

Using a prefix string rather than a structured return type is intentional: the ReAct agent receives tool outputs as message text, so a simple prefix that the agent prompt explicitly teaches it to parse is more robust than a JSON-encoded object that may be truncated or misformatted in the message trace.

### 3.3 Internal Implementation

```
1. Validate puml_code starts with "@startuml" and ends with "@enduml".
   If not → return "ERROR:PlantUML code must begin with @startuml and end with @enduml."
   (Cheap early exit before any temp file is created.)

2. Write puml_code to a NamedTemporaryFile with suffix=".puml", delete=False.
   Record the temp file path.

3. Call render_plantuml(
       input_path=tmp_path,
       output_path=output_path,
       output_type=output_type,
       base_url=base_url,
   )

4. On success → delete temp file → return f"OK:{output_path}"

5. On PlantURLError (non-zero exit from planturl binary) →
       delete temp file →
       return f"ERROR:planturl exited {e.returncode}: {e.stderr.strip()[:500]}"
       (Truncate stderr to 500 chars to stay within agent context window.)

6. On FileNotFoundError (input or output path problem) →
       delete temp file (if it was created) →
       return f"ERROR:File path error: {e}"

7. On any other exception →
       delete temp file (if it was created) →
       return f"ERROR:Unexpected error: {type(e).__name__}: {str(e)[:300]}"

8. Temp file cleanup in steps 4–7 uses a try/finally block to guarantee
   deletion even if the return statement raises.
```

### 3.4 Temp File Lifecycle

- Temp file is created with `tempfile.NamedTemporaryFile(suffix=".puml", mode="w", delete=False, encoding="utf-8")`.
- `delete=False` is required because `render_plantuml` opens the file by path after the `with` block closes it — a still-open `NamedTemporaryFile` with `delete=True` would be inaccessible on Windows and unreliable on Linux.
- Cleanup is unconditional: the temp file is always deleted in a `finally` block, regardless of success or failure.
- Temp files are written to the system temp directory (`tempfile.gettempdir()`), never to the AGA output directory.

### 3.5 Error Message Constraints

Error messages returned to the agent must be:

- **Human-readable**: the agent's prompt teaches it to reason from `svg_error_text` or binary stderr. The message must be parseable by an LLM reasoning step.
- **Bounded in length**: stderr is truncated to 500 characters to avoid overflowing the agent's context window. An ellipsis `"…"` is appended when truncation occurs.
- **No raw tracebacks**: Python tracebacks are not forwarded to the agent — only the exception type and message are included.

### 3.6 `base_url` and `output_type` Injection

The tool's `base_url` and `output_type` parameters have defaults but are designed to be overridden by the agent. In practice, the agent always calls the tool with the `base_url` from `AGAConfig.plantuml_base_url` — the agent prompt explicitly instructs it to pass this value on every tool call (see Phase 5).

Because the `@tool` decorator captures the function signature, these parameters appear in the tool's JSON schema that the LLM uses to produce tool call arguments. The agent prompt must include a clear instruction like:

> "Always pass `base_url=<plantuml_base_url from config>` and `output_type='png'` when calling `render_plantuml_tool`."

This is specified in the prompt template (Phase 5) and avoids the need for a partially-applied or curried tool variant.

### 3.7 Tool Registration

The tool is registered with the agent in `build_graph` (Phase 6) by passing it in the `tools` list to `create_react_agent`. No additional registration step is needed:

```python
from aga.tools.render_tool import render_plantuml_tool

agent = create_react_agent(
    model=config.llm,
    tools=[render_plantuml_tool],
    ...
)
```

---

## 4. What This Adapter Does NOT Do

| Concern | Where it is handled |
|---------|---------------------|
| SVG error detection (200 OK with error diagram) | NOT applicable — `render_plantuml` uses `--download` flag and the planturl binary handles the full render cycle including the server response. The binary's non-zero exit on failure surfaces the error through `PlantURLError`. |
| Server availability pre-check | Agent node startup guard (Phase 6) |
| Retry on transient network errors | `render_plantuml` / planturl binary handles transport; the tool does not add a retry layer on top |
| PNG bytes returned to agent | Not needed — the agent only needs to know the output path. Bytes are read by the output assembly node (Phase 6). |

### Note on SVG Error Detection

The original PRD described a two-request strategy (PNG + SVG) for detecting PlantUML syntax errors because the server returns HTTP 200 even for syntax errors. This is **not needed** in the current implementation because `render_plantuml` delegates to the `planturl` binary with `--download`, which handles the full render-and-detect cycle. The binary correctly exits non-zero when the server returns an error diagram. The adapter surfaces this through `PlantURLError`, which becomes an `"ERROR:..."` string for the agent.

---

## 5. Unit Test Criteria

- Given valid `@startuml\nBob -> Alice\n@enduml`, the tool returns a string starting with `"OK:"` and the output file exists at the returned path.
- Given `puml_code` that does not start with `"@startuml"`, the tool returns `"ERROR:PlantUML code must begin..."` without creating any temp file or calling `render_plantuml`.
- Given a `puml_code` that causes `render_plantuml` to raise `PlantURLError`, the tool returns `"ERROR:planturl exited..."` and the temp file is deleted.
- Given an `output_path` whose parent directory does not exist, the tool returns an `"ERROR:File path error:..."` string.
- The temp file is always deleted after the tool call, regardless of outcome (verified by asserting the temp path does not exist after the call).

---

## 6. Design Constraints Summary

| Constraint | Rule |
|------------|------|
| Return type | Always `str` — prefix `"OK:"` or `"ERROR:"` |
| Temp file | Created in system temp dir, always deleted in `finally` |
| Error truncation | stderr / exception messages capped at 500 / 300 chars respectively |
| No tracebacks to agent | Exception type + message only |
| `planturl_render.py` | Imported, never modified |
| Tool registration | Single tool in the agent's `tools` list |
