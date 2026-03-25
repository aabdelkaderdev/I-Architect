"""
BasePdfRenderer — Abstract Base Class for PDF rendering.

Defines the interface for the PDF Report Service (FR-PDF-001–018).
Uses WeasyPrint + Jinja2 under the hood.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BasePdfRenderer(ABC):
    """Abstract interface for PDF report generation."""

    @abstractmethod
    def render_html(self, template_name: str, context: dict[str, Any]) -> str:
        """Render a Jinja2 template to an HTML string.

        Args:
            template_name: Name of the Jinja2 template file.
            context: Dictionary of variables to inject into the template.

        Returns:
            Rendered HTML string.
        """
        raise NotImplementedError

    @abstractmethod
    def html_to_pdf(self, html_content: str) -> bytes:
        """Convert an HTML string to PDF bytes using WeasyPrint.

        Args:
            html_content: Rendered HTML string.

        Returns:
            PDF file content as bytes.
        """
        raise NotImplementedError

    @abstractmethod
    def merge_pdfs(self, pdf_paths: list[Path]) -> bytes:
        """Merge multiple PDF files into a single document using pypdf.

        Args:
            pdf_paths: Ordered list of paths to PDF files to merge.

        Returns:
            Merged PDF file content as bytes.
        """
        raise NotImplementedError
