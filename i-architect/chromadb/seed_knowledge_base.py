"""
ChromaDB Knowledge Base Seeder — Build-time population of vector collections.

Implements: FR-CHROMA-001–009.
This script runs during `docker build` (builder stage) to create
and populate the 4 immutable collections from PDF knowledge sources.
"""

from pathlib import Path
from typing import Any


KNOWLEDGE_SOURCE_DIR = Path("/knowledge_source")
CHROMA_DATA_DIR = Path("/chroma_data")

# Collection definitions (FR-CHROMA-001)
COLLECTIONS = {
    "architectural_patterns": {
        "description": "C4 and UML diagram templates, architectural pattern descriptions.",
        "metadata_fields": ["type", "pattern_name", "framework"],
    },
    "quality_attributes": {
        "description": "ISO 25010 quality attribute taxonomy and definitions.",
        "metadata_fields": ["qa_name", "category"],
    },
    "plantuml_syntax": {
        "description": "PlantUML syntax reference for C4 and UML diagrams.",
        "metadata_fields": ["diagram_type", "syntax_category"],
    },
    "scoring_rubrics": {
        "description": "SA evaluation criteria, example evaluations, and scoring rubrics.",
        "metadata_fields": ["pillar", "rubric_type"],
    },
}


def seed_all() -> None:
    """Run the full seeding pipeline.

    1. Parse PDFs from knowledge_source/ (FR-CHROMA-003).
    2. Chunk text using RecursiveCharacterTextSplitter (FR-CHROMA-005).
    3. Generate embeddings using sentence-transformers (FR-CHROMA-006).
    4. Create collections with metadata (FR-CHROMA-007).
    5. Insert documents/embeddings (FR-CHROMA-008).
    6. Persist to /chroma_data (FR-CHROMA-009).
    """
    raise NotImplementedError


def _parse_pdfs(directory: Path) -> list[dict[str, Any]]:
    """Extract text from PDFs using pypdf.

    Args:
        directory: Path containing PDF knowledge source files.

    Returns:
        List of {filename, pages: [{page_number, text}]} dicts.
    """
    raise NotImplementedError


def _chunk_text(text: str, chunk_size: int = 512, chunk_overlap: int = 64) -> list[str]:
    """Split text into overlapping chunks using RecursiveCharacterTextSplitter.

    Args:
        text: Raw text to chunk.
        chunk_size: Target chunk size in characters.
        chunk_overlap: Overlap between consecutive chunks.

    Returns:
        List of text chunks.
    """
    raise NotImplementedError


def _generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """Generate embeddings using sentence-transformers.

    Args:
        chunks: List of text chunks.

    Returns:
        List of embedding vectors.
    """
    raise NotImplementedError


if __name__ == "__main__":
    seed_all()
