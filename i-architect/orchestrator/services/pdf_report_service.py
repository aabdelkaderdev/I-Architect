"""
PDF Report Service — WeasyPrint + Jinja2 PDF generation.

Implements: FR-PDF-001–018, IR-PDF-003.
"""

import os
from pathlib import Path
from typing import Any

from core.interfaces.base_pdf_renderer import BasePdfRenderer


class PdfReportService(BasePdfRenderer):
    """Generates Template A (ARLO) and Template B (Full Pipeline) PDF reports.

    Uses WeasyPrint for HTML→PDF conversion, Jinja2 for templating,
    and pypdf for document merging.
    """

    def __init__(self, project_root: str) -> None:
        """Initialize the PDF service.

        Args:
            project_root: Absolute path to the project directory.
        """
        self.project_root = Path(project_root)
        self.output_dir = self.project_root / "pdf"

    def render_html(self, template_name: str, context: dict[str, Any]) -> str:
        """Render a Jinja2 template to HTML (FR-PDF-002).

        Args:
            template_name: Template filename in templates/pdf/.
            context: Variables to inject.

        Returns:
            Rendered HTML string.
        """
        raise NotImplementedError

    def html_to_pdf(self, html_content: str) -> bytes:
        """Convert HTML to PDF via WeasyPrint (FR-PDF-001).

        Args:
            html_content: Rendered HTML string.

        Returns:
            PDF bytes.
        """
        raise NotImplementedError

    def merge_pdfs(self, pdf_paths: list[Path]) -> bytes:
        """Merge PDFs using pypdf (FR-PDF-003).

        Args:
            pdf_paths: Ordered list of PDF file paths.

        Returns:
            Merged PDF bytes.
        """
        raise NotImplementedError

    def generate_template_a(self, arlo_json_data: dict) -> str:
        """Generate ARLO Architectural Decision Report (FR-PDF-004–009).

        Auto-triggered at end of ARLO pipeline step.

        Args:
            arlo_json_data: ARLO TOON payload dictionary.

        Returns:
            Path to generated PDF file.
        """
        raise NotImplementedError

    def generate_template_b(
        self,
        raa_data: dict,
        aga_data: dict,
        sa_data: dict,
        template_a_path: str | None = None,
    ) -> str:
        """Generate Full Pipeline Report by merging Template A + Part 2 (FR-PDF-010–014).

        Part 2 includes RAA, AGA (code + rendered diagram), and SA sections.

        Args:
            raa_data: RAA TOON IR data.
            aga_data: AGA PlantUML code and rendered image.
            sa_data: SA evaluation JSON.
            template_a_path: Path to existing Template A PDF (auto-generated if None).

        Returns:
            Path to generated PDF file.
        """
        raise NotImplementedError

    def _enforce_retention(self) -> None:
        """Delete oldest PDF if count >= 5 (FR-PDF-017)."""
        raise NotImplementedError

    def _check_disk_quota(self) -> bool:
        """Pre-check disk quota before generation (NFR-PDF-003).

        Returns:
            True if within quota.
        """
        raise NotImplementedError
