"""
test_planturl_render.py
=======================
Unit and integration tests for :mod:`tools.planturl_render`.

Test categories
---------------
* **Unit** – mock subprocess so no real network calls are made.
* **Integration** – actually invoke the CLI against the real PlantUML server
  using the C4 container diagram sample.  These are skipped when the marker
  ``--skip-integration`` is passed or when the environment variable
  ``PLANTURL_SKIP_INTEGRATION=1`` is set.

Run all tests
~~~~~~~~~~~~~
    cd <repo-root>/aga
    pytest tools/test_planturl_render.py -v

Run only unit tests (no network)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pytest tools/test_planturl_render.py -v -m "not integration"

Run with verbose integration output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pytest tools/test_planturl_render.py -v -m integration
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Ensure the tools package is importable regardless of working directory
# ---------------------------------------------------------------------------
_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from planturl_render import (  # noqa: E402
    DEFAULT_BASE_URL,
    PlantURLError,
    _detect_binary,
    render_plantuml,
)

# ---------------------------------------------------------------------------
# Paths used in tests
# ---------------------------------------------------------------------------
_REPO_ROOT = _TOOLS_DIR.parent
_SAMPLE_PUML = (
    _REPO_ROOT / "test_example" / "c4-model-container-diagram.plantuml"
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _make_successful_proc(stdout: str = "", stderr: str = "") -> MagicMock:
    """Return a mock CompletedProcess that looks like a successful run."""
    mock = MagicMock()
    mock.returncode = 0
    mock.stdout = stdout
    mock.stderr = stderr
    return mock


def _make_failing_proc(returncode: int, stderr: str, stdout: str = "") -> MagicMock:
    """Return a mock CompletedProcess that looks like a failed run."""
    mock = MagicMock()
    mock.returncode = returncode
    mock.stdout = stdout
    mock.stderr = stderr
    return mock


# ---------------------------------------------------------------------------
# Pytest markers
# ---------------------------------------------------------------------------

def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "integration: marks tests that call the real PlantUML server")


def _skip_integration() -> bool:
    return os.environ.get("PLANTURL_SKIP_INTEGRATION", "").strip() in ("1", "true", "yes")


integration = pytest.mark.skipif(
    _skip_integration(),
    reason="Integration tests disabled (set PLANTURL_SKIP_INTEGRATION=0 to enable)",
)


# ===========================================================================
# 1. Argument validation (pure Python – no subprocess)
# ===========================================================================

class TestArgumentValidation:
    """render_plantuml raises the right exceptions before touching the CLI."""

    def test_invalid_output_type_raises_value_error(self, tmp_path: Path) -> None:
        dummy_input = tmp_path / "diagram.puml"
        dummy_input.write_text("@startuml\n@enduml\n")
        with pytest.raises(ValueError, match="Invalid output_type"):
            render_plantuml(dummy_input, tmp_path / "out.xyz", output_type="pdf")  # type: ignore[arg-type]

    def test_missing_input_file_raises_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="Input file not found"):
            render_plantuml(tmp_path / "nonexistent.puml", tmp_path / "out.svg")

    def test_input_path_is_directory_raises_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="not a file"):
            render_plantuml(tmp_path, tmp_path / "out.svg")

    def test_missing_output_directory_raises_file_not_found(self, tmp_path: Path) -> None:
        dummy_input = tmp_path / "diagram.puml"
        dummy_input.write_text("@startuml\n@enduml\n")
        with pytest.raises(FileNotFoundError, match="Output directory does not exist"):
            render_plantuml(dummy_input, tmp_path / "ghost_dir" / "out.svg")


# ===========================================================================
# 2. CLI error propagation (mocked subprocess)
# ===========================================================================

class TestCLIErrorPropagation:
    """PlantURLError is raised and carries the right metadata."""

    @pytest.fixture()
    def sample_input(self, tmp_path: Path) -> Path:
        p = tmp_path / "diagram.puml"
        p.write_text("@startuml\nBob -> Alice : hello\n@enduml\n")
        return p

    def _patch_and_run(
        self,
        sample_input: Path,
        tmp_path: Path,
        mock_proc: MagicMock,
        output_type: str = "svg",
    ) -> None:
        with patch("planturl_render.subprocess.run", return_value=mock_proc):
            render_plantuml(sample_input, tmp_path / "out.svg", output_type=output_type)

    # --- Exit code 101: source / target file not found (CLI panic) ----------

    def test_exit_101_source_not_found_raises_planturl_error(
        self, sample_input: Path, tmp_path: Path
    ) -> None:
        stderr = "thread 'main' panicked at src/bin/main.rs:110:33:\nsource file /nonexistent.puml not found!"
        mock_proc = _make_failing_proc(101, stderr)
        with patch("planturl_render.subprocess.run", return_value=mock_proc):
            with pytest.raises(PlantURLError) as exc_info:
                render_plantuml(sample_input, tmp_path / "out.svg")
        err = exc_info.value
        assert err.returncode == 101
        assert "not found" in err.stderr
        assert err.cmd  # non-empty list

    def test_exit_101_target_not_found_raises_planturl_error(
        self, sample_input: Path, tmp_path: Path
    ) -> None:
        stderr = "thread 'main' panicked at src/bin/main.rs:142:37:\ntarget file /bad/path/out.svg not found!"
        mock_proc = _make_failing_proc(101, stderr)
        with patch("planturl_render.subprocess.run", return_value=mock_proc):
            with pytest.raises(PlantURLError) as exc_info:
                render_plantuml(sample_input, tmp_path / "out.svg")
        assert exc_info.value.returncode == 101

    # --- Exit code 2: invalid CLI argument (clap error) --------------------

    def test_exit_2_invalid_type_raises_planturl_error(
        self, sample_input: Path, tmp_path: Path
    ) -> None:
        stderr = "error: invalid value 'pdf' for '--type <IMAGE_TYPE>': Unknown image-type pdf"
        mock_proc = _make_failing_proc(2, stderr)
        with patch("planturl_render.subprocess.run", return_value=mock_proc):
            with pytest.raises(PlantURLError) as exc_info:
                render_plantuml(sample_input, tmp_path / "out.svg")
        assert exc_info.value.returncode == 2
        assert "invalid value" in exc_info.value.stderr

    # --- Exit code 1: network / HTTP error ---------------------------------

    def test_exit_1_network_error_raises_planturl_error(
        self, sample_input: Path, tmp_path: Path
    ) -> None:
        stderr = (
            "Error: error sending request for url (http://bad-host/plantuml/svg/...)\n\n"
            "Caused by:\n"
            "    0: client error (Connect)\n"
            "    1: dns error: failed to lookup address information: Name or service not known"
        )
        mock_proc = _make_failing_proc(1, stderr)
        with patch("planturl_render.subprocess.run", return_value=mock_proc):
            with pytest.raises(PlantURLError) as exc_info:
                render_plantuml(
                    sample_input,
                    tmp_path / "out.svg",
                    base_url="http://bad-host/plantuml",
                )
        err = exc_info.value
        assert err.returncode == 1
        assert "dns error" in err.stderr.lower() or "connect" in err.stderr.lower()

    # --- OSError launching the binary --------------------------------------

    def test_os_error_launching_binary_raises_planturl_error(
        self, sample_input: Path, tmp_path: Path
    ) -> None:
        with patch(
            "planturl_render.subprocess.run",
            side_effect=OSError("Permission denied"),
        ):
            with pytest.raises(PlantURLError) as exc_info:
                render_plantuml(sample_input, tmp_path / "out.svg")
        assert exc_info.value.returncode == -1
        assert "Permission denied" in exc_info.value.stderr

    # --- Successful mock run returns resolved Path -------------------------

    def test_successful_run_returns_output_path(
        self, sample_input: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "result.svg"
        # Simulate the CLI creating the file
        output.write_bytes(b"<svg/>")
        mock_proc = _make_successful_proc()
        with patch("planturl_render.subprocess.run", return_value=mock_proc):
            returned = render_plantuml(sample_input, output)
        assert returned == output.resolve()

    # --- PlantURLError str representation ----------------------------------

    def test_planturl_error_str_contains_key_info(
        self, sample_input: Path, tmp_path: Path
    ) -> None:
        stderr = "thread 'main' panicked: something went wrong"
        mock_proc = _make_failing_proc(101, stderr)
        with patch("planturl_render.subprocess.run", return_value=mock_proc):
            with pytest.raises(PlantURLError) as exc_info:
                render_plantuml(sample_input, tmp_path / "out.svg")
        err_str = str(exc_info.value)
        assert "101" in err_str
        assert "something went wrong" in err_str
        assert "planturl" in err_str


# ===========================================================================
# 3. Platform / binary detection (mocked platform)
# ===========================================================================

class TestBinaryDetection:
    """_detect_binary() selects the right subfolder for each platform."""

    @pytest.mark.parametrize(
        "system, machine, expected_subfolder",
        [
            ("Linux",   "x86_64",  "linux-gnu"),
            ("Darwin",  "x86_64",  "apple-darwin"),
            ("Darwin",  "arm64",   "aarch64-apple-darwin"),
            ("Darwin",  "aarch64", "aarch64-apple-darwin"),
            ("Windows", "AMD64",   "windows-msvc"),
        ],
    )
    def test_correct_subfolder_selected(
        self, system: str, machine: str, expected_subfolder: str
    ) -> None:
        from planturl_render import _BIN_ROOT

        with (
            patch("platform.system", return_value=system),
            patch("platform.machine", return_value=machine),
            patch("planturl_render._detect_linux_libc", return_value="gnu"),
        ):
            binary = _detect_binary()

        assert expected_subfolder in str(binary)
        assert binary.parent == _BIN_ROOT / expected_subfolder

    def test_unsupported_os_raises_runtime_error(self) -> None:
        with (
            patch("platform.system", return_value="FreeBSD"),
            patch("platform.machine", return_value="amd64"),
        ):
            with pytest.raises(RuntimeError, match="Unsupported operating system"):
                _detect_binary()

    def test_missing_binary_raises_runtime_error(self, tmp_path: Path) -> None:
        """If the binary file doesn't exist, RuntimeError is raised."""
        with (
            patch("platform.system", return_value="Linux"),
            patch("platform.machine", return_value="x86_64"),
            patch("planturl_render._detect_linux_libc", return_value="gnu"),
            patch("planturl_render._BIN_ROOT", tmp_path),  # empty dir
        ):
            with pytest.raises(RuntimeError, match="not found at expected path"):
                _detect_binary()


# ===========================================================================
# 4. Integration tests — real CLI + real PlantUML server
# ===========================================================================

@integration
class TestIntegration:
    """
    These tests actually invoke the planturl binary and reach out to the
    public PlantUML server.  They are skipped when PLANTURL_SKIP_INTEGRATION=1.

    Requires:
        - A working internet connection
        - The sample file at test_example/c4-model-container-diagram.plantuml
    """

    def test_sample_file_exists(self) -> None:
        assert _SAMPLE_PUML.exists(), (
            f"Sample PlantUML file not found: {_SAMPLE_PUML}\n"
            "Make sure you are running tests from within the 'aga' workspace."
        )

    def test_render_svg(self, tmp_path: Path) -> None:
        output = tmp_path / "diagram.svg"
        result = render_plantuml(_SAMPLE_PUML, output, output_type="svg")
        assert result == output
        assert output.exists()
        assert output.stat().st_size > 0
        # SVG files start with either <?xml or <svg
        content = output.read_text(encoding="utf-8", errors="replace")
        assert "<svg" in content or "<?xml" in content

    def test_render_png(self, tmp_path: Path) -> None:
        output = tmp_path / "diagram.png"
        result = render_plantuml(_SAMPLE_PUML, output, output_type="png")
        assert result == output
        assert output.exists()
        assert output.stat().st_size > 100  # a real PNG is always larger than this
        # PNG magic bytes: \x89PNG
        assert output.read_bytes()[:4] == b"\x89PNG"

    def test_render_ascii(self, tmp_path: Path) -> None:
        output = tmp_path / "diagram.txt"
        result = render_plantuml(_SAMPLE_PUML, output, output_type="ascii")
        assert result == output
        assert output.exists()
        assert output.stat().st_size > 0

    def test_custom_base_url_is_passed_to_cli(self, tmp_path: Path) -> None:
        """
        Using a bogus base URL should cause a network/connection error which
        surfaces as a PlantURLError (proves the URL is actually forwarded).
        """
        output = tmp_path / "diagram.svg"
        with pytest.raises(PlantURLError) as exc_info:
            render_plantuml(
                _SAMPLE_PUML,
                output,
                output_type="svg",
                base_url="http://totally-invalid-host-xyz.fake/plantuml",
            )
        assert exc_info.value.returncode != 0

    def test_invalid_output_type_raises_value_error_before_cli(
        self, tmp_path: Path
    ) -> None:
        """ValueError is raised in Python before the CLI is ever called."""
        with pytest.raises(ValueError, match="Invalid output_type"):
            render_plantuml(_SAMPLE_PUML, tmp_path / "out.xyz", output_type="gif")  # type: ignore[arg-type]
