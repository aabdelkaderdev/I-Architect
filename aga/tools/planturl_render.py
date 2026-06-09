"""
planturl_render.py
==================
A Python wrapper around the `planturl` CLI tool that auto-detects the correct
binary for the running platform and renders a PlantUML source file into an
output image (or encoded URL string) via a PlantUML server.

Supported platforms / binaries
-------------------------------
  linux-gnu   → x86_64 Linux with glibc  (Ubuntu, Debian, Fedora, …)
  linux-musl  → x86_64 Linux with musl   (Alpine, static builds)
  apple-darwin         → macOS Intel (x86_64)
  aarch64-apple-darwin → macOS Apple Silicon (arm64)
  windows-msvc         → Windows (planturl.exe)

CLI reference (planturl 0.4.4)
-------------------------------
  -s, --source <SOURCE>            Input file
  -u, --base-url <BASE_URL>        Base PlantUML server URL
  -d, --download                   Download the rendered image from the server
  -t, --type <IMAGE_TYPE>          Image type: ascii | png | svg  [default: svg]
  -f, --file <FILE>                Save result to this file (stdout if absent)
  -h, --help / -V, --version
"""

from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path
from typing import Literal

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Absolute path to the directory that contains this file.
_THIS_DIR = Path(__file__).resolve().parent

#: Root directory of all platform binaries.
_BIN_ROOT = _THIS_DIR / "planturl" / "Bin"

#: Supported output image types (mirrors the CLI's --type option).
ImageType = Literal["svg", "png", "ascii"]

#: Default PlantUML server base URL.
DEFAULT_BASE_URL: str = "https://www.plantuml.com/plantuml"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _detect_binary() -> Path:
    """
    Detect the host OS / architecture and return the path to the matching
    ``planturl`` binary.

    Raises
    ------
    RuntimeError
        If the current platform is not supported or the binary is missing.
    """
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "windows":
        subfolder = "windows-msvc"
        exe_name = "planturl.exe"
    elif system == "darwin":
        if machine in ("arm64", "aarch64"):
            subfolder = "aarch64-apple-darwin"
        else:
            subfolder = "apple-darwin"
        exe_name = "planturl"
    elif system == "linux":
        # Distinguish glibc (GNU) from musl by inspecting the C library
        # reported by the interpreter or by checking ldd output.
        libc_info = _detect_linux_libc()
        if libc_info == "musl":
            subfolder = "linux-musl"
        else:
            subfolder = "linux-gnu"
        exe_name = "planturl"
    else:
        raise RuntimeError(
            f"Unsupported operating system: {system!r}. "
            "Please add a matching binary under tools/planturl/Bin/."
        )

    binary_path = _BIN_ROOT / subfolder / exe_name
    if not binary_path.exists():
        raise RuntimeError(
            f"planturl binary not found at expected path: {binary_path}\n"
            f"Make sure the '{subfolder}' directory contains the '{exe_name}' binary."
        )

    return binary_path


def _detect_linux_libc() -> str:
    """
    Return ``'musl'`` when running under a musl libc, ``'gnu'`` otherwise.

    Strategy
    --------
    1. Check ``platform.libc_ver()`` — works for glibc.
    2. Inspect ``/proc/self/exe`` via ``ldd`` for the string ``"musl"``.
    3. Fall back to ``'gnu'`` (safest default on mainstream distros).
    """
    libc_name, _version = platform.libc_ver()
    if libc_name:
        # e.g. libc_name == 'glibc' on GNU systems
        return "musl" if "musl" in libc_name.lower() else "gnu"

    # Fallback: run ldd on the Python interpreter itself
    try:
        result = subprocess.run(
            ["ldd", sys.executable],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if "musl" in result.stdout.lower() or "musl" in result.stderr.lower():
            return "musl"
    except Exception:
        pass

    return "gnu"


def _ensure_executable(binary: Path) -> None:
    """Make sure the binary has execute permission (Unix only)."""
    if platform.system().lower() != "windows":
        current_mode = binary.stat().st_mode
        # Add execute bits for owner, group, others (chmod +x)
        binary.chmod(current_mode | 0o111)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class PlantURLError(RuntimeError):
    """
    Raised when the ``planturl`` CLI exits with a non-zero return code.

    Attributes
    ----------
    returncode : int
        The exit code returned by the process.
    stderr : str
        The full text written to stderr by the CLI tool.
    stdout : str
        The full text written to stdout by the CLI tool (may be empty).
    cmd : list[str]
        The exact command list that was executed.
    """

    def __init__(
        self,
        message: str,
        *,
        returncode: int,
        stderr: str,
        stdout: str,
        cmd: list[str],
    ) -> None:
        super().__init__(message)
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = stdout
        self.cmd = cmd

    def __str__(self) -> str:
        lines = [
            super().__str__(),
            f"  Return code : {self.returncode}",
            f"  Command     : {' '.join(self.cmd)}",
        ]
        if self.stderr.strip():
            lines.append(f"  Stderr      :\n    " + self.stderr.strip().replace("\n", "\n    "))
        if self.stdout.strip():
            lines.append(f"  Stdout      :\n    " + self.stdout.strip().replace("\n", "\n    "))
        return "\n".join(lines)


def render_plantuml(
    input_path: str | Path,
    output_path: str | Path,
    output_type: ImageType = "svg",
    base_url: str = DEFAULT_BASE_URL,
) -> Path:
    """
    Render a PlantUML source file to an output image using the ``planturl``
    CLI tool.  The appropriate binary is chosen automatically based on the
    current OS and CPU architecture.

    Parameters
    ----------
    input_path : str | Path
        Path to the ``.puml`` / ``.plantuml`` source file.
    output_path : str | Path
        Destination path for the rendered output file.
        The parent directory must already exist.
    output_type : {'svg', 'png', 'ascii'}
        The image format to generate.  Defaults to ``'svg'``.
    base_url : str
        Base URL of the PlantUML rendering server.
        Defaults to ``'https://www.plantuml.com/plantuml'``.

    Returns
    -------
    Path
        The resolved absolute path of the written output file.

    Raises
    ------
    ValueError
        If ``output_type`` is not one of the accepted values.
    FileNotFoundError
        If ``input_path`` does not exist.
    PlantURLError
        If the ``planturl`` CLI exits with a non-zero return code.  The
        exception carries ``returncode``, ``stderr``, ``stdout``, and ``cmd``
        attributes for programmatic inspection.
    RuntimeError
        If the current platform is unsupported or the binary is missing.
    """
    # --- Validate arguments ------------------------------------------------
    valid_types: tuple[str, ...] = ("svg", "png", "ascii")
    if output_type not in valid_types:
        raise ValueError(
            f"Invalid output_type {output_type!r}. "
            f"Must be one of: {', '.join(valid_types)}"
        )

    input_path = Path(input_path).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if not input_path.is_file():
        raise FileNotFoundError(f"Input path is not a file: {input_path}")

    output_path = Path(output_path).resolve()
    if not output_path.parent.exists():
        raise FileNotFoundError(
            f"Output directory does not exist: {output_path.parent}"
        )

    # --- Locate and prepare the binary ------------------------------------
    binary = _detect_binary()
    _ensure_executable(binary)

    # --- Build the command ------------------------------------------------
    cmd: list[str] = [
        str(binary),
        "--source", str(input_path),
        "--base-url", base_url,
        "--type", output_type,
        "--download",           # always download the actual rendered file
        "--file", str(output_path),
    ]

    # --- Execute -----------------------------------------------------------
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise PlantURLError(
            f"Failed to launch planturl binary: {exc}",
            returncode=-1,
            stderr=str(exc),
            stdout="",
            cmd=cmd,
        ) from exc

    if proc.returncode != 0:
        # Compose a human-readable message from stderr (the CLI always writes
        # errors there) and raise with full context attached.
        stderr_text = proc.stderr.strip()
        raise PlantURLError(
            f"planturl exited with code {proc.returncode}: {stderr_text}",
            returncode=proc.returncode,
            stderr=proc.stderr,
            stdout=proc.stdout,
            cmd=cmd,
        )

    return output_path
