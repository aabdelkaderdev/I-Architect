"""
Ingestion Service — Coordinates file parsing, strategy selection, and UID generation.

Implements: FR-ING-001–006, orchestrates extraction strategies.
"""

from pathlib import Path
from typing import Any

from core.interfaces.base_extraction_strategy import BaseExtractionStrategy


class IngestionService:
    """Orchestrates document ingestion, parsing, and requirement extraction.

    Delegates to concrete extraction strategies via the Strategy pattern.
    Handles CSV bypass (FR-ING-003), UID generation (FR-ING-005), and
    format-specific parsing (FR-ING-001).
    """

    def __init__(self, strategy: BaseExtractionStrategy | None = None) -> None:
        """Initialize the ingestion service.

        Args:
            strategy: The extraction strategy to use. Can be set later via set_strategy().
        """
        self._strategy = strategy

    def set_strategy(self, strategy: BaseExtractionStrategy) -> None:
        """Set or change the extraction strategy at runtime.

        Args:
            strategy: The new extraction strategy to use.
        """
        self._strategy = strategy

    def parse_file(self, file_path: Path, file_extension: str) -> str:
        """Parse an uploaded file into raw text or DataFrame.

        Supports: .pdf (PyMuPDF), .docx (python-docx), .txt, .xls/.xlsx (pandas),
        .csv (pandas). See FR-ING-001 for format-specific strategies.

        Args:
            file_path: Path to the uploaded file.
            file_extension: File extension (e.g., ".pdf").

        Returns:
            Raw text string extracted from the document.

        Raises:
            ValueError: If file extension is not supported.
        """
        raise NotImplementedError

    def check_csv_bypass(self, file_path: Path) -> bool:
        """Check if a CSV file matches the target schema for bypass (FR-ING-003).

        If columns match {Requirement ID, Description} (case-insensitive),
        extraction is skipped entirely.

        Args:
            file_path: Path to the CSV file.

        Returns:
            True if the CSV matches the bypass schema.
        """
        raise NotImplementedError

    def generate_uid(self, file_content: bytes, incremental_id: int) -> str:
        """Generate a unique requirement ID: REQ-[FILE_HASH_PREFIX]-[INCR_ID] (FR-ING-005).

        Args:
            file_content: Binary content of the uploaded file.
            incremental_id: Sequential counter for this extraction session.

        Returns:
            Formatted UID string.
        """
        raise NotImplementedError

    def extract_requirements(
        self,
        file_path: Path,
        strategy_name: str | None = None,
    ) -> dict[str, Any]:
        """Full extraction pipeline: parse → extract → validate → return.

        Args:
            file_path: Path to the uploaded document.
            strategy_name: Optional strategy override. If None, uses the set strategy.

        Returns:
            ExtractionResult dictionary containing extracted requirements.
        """
        raise NotImplementedError

    def handle_excel_restructuring(self, file_path: Path) -> Any:
        """Heuristic restructuring for .xls/.xlsx files (FR-ING-002).

        Scans first 10 rows for header keywords, normalizes structure.

        Args:
            file_path: Path to the Excel file.

        Returns:
            Normalized pandas DataFrame.
        """
        raise NotImplementedError
