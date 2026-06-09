import os
import subprocess
import tempfile

from aga.tools.fetch_plantuml_png import fetch_plantuml_png_logic, PNG_SIGNATURE


class _FakeResult:
    """Simulates subprocess.run result."""
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_fetch_plantuml_png_logic_downloads_valid_png_via_planturl(monkeypatch, tmp_path):
    """planturl -d produces a valid PNG → success."""
    png = PNG_SIGNATURE + b"payload"
    puml_code = "@startuml\nAlice -> Bob : hello\n@enduml"

    def fake_run(cmd, **kwargs):
        # Find the -f argument (output file path)
        for i, arg in enumerate(cmd):
            if arg == "-f" and i + 1 < len(cmd):
                with open(cmd[i + 1], "wb") as f:
                    f.write(png)
                break
        return _FakeResult(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = fetch_plantuml_png_logic(
        "https://example.test/plantuml/png/abc",
        puml_code=puml_code,
        planturl_bin_path="/fake/planturl",
    )

    assert result["image_bytes"] == png


def test_fetch_plantuml_png_logic_rejects_non_png(monkeypatch, tmp_path):
    """planturl -d produces non-PNG content → error."""
    puml_code = "@startuml\n@enduml"

    def fake_run(cmd, **kwargs):
        for i, arg in enumerate(cmd):
            if arg == "-f" and i + 1 < len(cmd):
                with open(cmd[i + 1], "wb") as f:
                    f.write(b"not a png file")
                break
        return _FakeResult(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = fetch_plantuml_png_logic(
        "https://example.test/plantuml/png/abc",
        puml_code=puml_code,
        planturl_bin_path="/fake/planturl",
    )

    assert "error" in result


def test_fetch_plantuml_png_logic_reports_planturl_failure(monkeypatch):
    """planturl exits non-zero → error."""
    puml_code = "@startuml\n@enduml"

    def fake_run(cmd, **kwargs):
        return _FakeResult(returncode=1, stderr="some binary error")

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = fetch_plantuml_png_logic(
        "https://example.test/plantuml/png/abc",
        puml_code=puml_code,
        planturl_bin_path="/fake/planturl",
    )

    assert "error" in result
    assert "exit code" in result["error"]


def test_fetch_plantuml_png_logic_errors_without_puml_code():
    """No puml_code → immediate error."""
    result = fetch_plantuml_png_logic(
        "https://example.test/plantuml/png/abc",
        puml_code="",
    )

    assert "error" in result
    assert "No PlantUML source" in result["error"]
