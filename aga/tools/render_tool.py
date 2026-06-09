"""LangGraph @tool adapter for render_plantuml.

Bridges the gap between the file-path-based render_plantuml function and
the in-memory string-based ReAct agent. Manages temp file lifecycle and
returns a prefix-string protocol the agent prompt teaches the LLM to parse.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from langchain_core.tools import tool

from aga.tools.planturl_render import PlantURLError, render_plantuml

# Known byte-strings that appear inside PlantUML error PNGs.
# PlantUML embeds the error text as uncompressed Latin-1 inside the
# PNG data stream, so a simple byte scan is reliable.
_ERROR_SIGNATURES: list[bytes] = [
    b"Syntax Error",
    b"Cannot open URL",
    b"Assumed diagram type",
    b"Error line",
]

def _detect_error_image(output_path: str) -> str | None:
    """Return a human-readable hint if *output_path* looks like a PlantUML
    error image, or ``None`` if it appears healthy.

    Scans the raw bytes for known PlantUML error strings embedded in the
    rendered image.  This is reliable because PlantUML embeds error text
    as uncompressed Latin-1 inside the PNG/SVG data stream.

    Note: a previous size-based heuristic was removed because ALL PlantUML
    PNGs contain ``plantuml`` in their metadata chunks, causing false
    positives for any valid diagram under the threshold.
    """
    path = Path(output_path)
    if not path.exists():
        return "output file does not exist after render"

    raw = path.read_bytes()

    for sig in _ERROR_SIGNATURES:
        if sig in raw:
            return sig.decode("latin-1", errors="replace")

    return None


@tool
def render_plantuml_tool(
    puml_code: str,
    output_path: str,
    output_type: str = "png",
    base_url: str = "https://www.plantuml.com/plantuml",
) -> str:
    """Render a PlantUML diagram from a source code string.

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
    stripped = puml_code.strip()
    if not stripped.startswith("@startuml") or not stripped.endswith("@enduml"):
        return (
            "ERROR:PlantUML code must begin with @startuml"
            " and end with @enduml."
        )

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".puml",
            mode="w",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            tmp.write(puml_code)
            tmp_path = tmp.name

        render_plantuml(
            input_path=tmp_path,
            output_path=output_path,
            output_type=output_type,
            base_url=base_url,
        )

        # --- Post-render error-image detection ---
        # The planturl binary exits 0 even when the PlantUML server
        # renders a "Syntax Error?" image. Detect this by inspecting
        # the output file so the retry/correction loop can fire.
        error_hint = _detect_error_image(output_path)
        if error_hint:
            return f"ERROR:PlantUML rendered an error image: {error_hint}"

        return f"OK:{output_path}"

    except PlantURLError as e:
        stderr_text = e.stderr.strip()[:500]
        if len(e.stderr.strip()) > 500:
            stderr_text += "…"
        return f"ERROR:planturl exited {e.returncode}: {stderr_text}"

    except FileNotFoundError as e:
        return f"ERROR:File path error: {e}"

    except Exception as e:
        msg = str(e)[:300]
        if len(str(e)) > 300:
            msg += "…"
        return f"ERROR:Unexpected error: {type(e).__name__}: {msg}"

    finally:
        if tmp_path is not None:
            import os

            try:
                os.unlink(tmp_path)
            except OSError:
                pass
