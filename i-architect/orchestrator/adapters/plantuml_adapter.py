"""
PlantUML Adapter — Facade for the PlantUML rendering server.

Implements: FR-PUML-001–004, DR-PUML-001–003.
"""

from typing import Optional


class PlantUMLAdapter:
    """Facade for the PlantUML server HTTP API.

    Handles: SVG/PNG rendering, input sanitization, error parsing,
    and Redis-based render caching.
    """

    def __init__(self, base_url: str, timeout_seconds: int = 300) -> None:
        """Initialize adapter.

        Args:
            base_url: PlantUML server URL (e.g., "http://plantuml-server:8080").
            timeout_seconds: Render timeout (FR-PUML-003 default: 300s).
        """
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def render_svg(self, puml_source: str) -> bytes:
        """Render PlantUML source code to SVG via POST /svg/ (FR-PUML-001).

        Args:
            puml_source: Raw PlantUML code string.

        Returns:
            SVG image bytes.

        Raises:
            PlantUMLSyntaxError: If the server returns HTTP 400.
            PlantUMLServerCrashError: If the server returns HTTP 500.
            RenderTimeoutError: If rendering exceeds timeout.
        """
        raise NotImplementedError

    def render_png(self, puml_source: str) -> bytes:
        """Render PlantUML source code to PNG via POST /png/ (FR-PUML-002).

        Args:
            puml_source: Raw PlantUML code string.

        Returns:
            PNG image bytes.
        """
        raise NotImplementedError

    def get_syntax_error(self, puml_source: str) -> Optional[str]:
        """Check if PlantUML code has syntax errors without full render (FR-PUML-004).

        Uses the /check endpoint to quickly validate syntax.

        Args:
            puml_source: Raw PlantUML code string.

        Returns:
            Error message string if syntax error, None if valid.
        """
        raise NotImplementedError

    def _sanitize_input(self, puml_source: str) -> str:
        """Sanitize PlantUML input: strip !include, !pragma, restrict to safe commands.

        Args:
            puml_source: Raw PlantUML code.

        Returns:
            Sanitized PlantUML code.
        """
        raise NotImplementedError

    def health_check(self) -> bool:
        """Check if the PlantUML server is reachable.

        Returns:
            True if the server responds to a health probe.
        """
        raise NotImplementedError
